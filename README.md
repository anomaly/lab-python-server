# Lab - Containerised Python server

This lab aims to outline a recipe for building a standardised Python server that can be run in a container. Our major aims are to be able to:
- [X] Expose an API that will eventually sit behind a reverse proxy
- [X] A Postgres server for development
- [X] A Redis server for development
- [ ] Healthcheck endpoint that will validate that the API can get to the database
- [ ] Worker processes that will process tasks in the background (using Celery)
- [ ] Provide `Dockerfile` for development and production
- [ ] Log aggregation and monitoring (fluentd)
- [X] CSRF protection
- [ ] Basic endpoints for authentication

In production (see [Terraform lab project](https://github.com/anomaly/lab-tf-linode)) we will use `Terraform` and `Helm` provision infrastructure and deploy the app in pods. Ideally `Postgres` and `Redis` would be provisioned as a hosted products (Linode is yet to offer this), in the short term they will be installed from official `Charts`.

TODO:
- [ ] Convert the project to be a [Cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/) template

> The approach taken in this guide is to document the tools and commands are they are and not build additional tooling or abstractions. The aim is to educate the user on the tools and how to use them.

Ultimately the output of this lab will be consumed as the `app` and `worker` for the [Terramform Lab](https://github.com/anomaly/lab-tf-linode).

## General notes

Python 3.10 requires the Tinker package to be installed, not sure why this is the case and why the the base Docker image does not contain this. Take a look at the `Dockerfile` where we install this package via `apt`.

On macOS we manage this via Homebrew:
```
brew install python-tk@3.10
```

Handy commands and tools, which we use to help with the infrastructure: 

Use `openssl` to generate a random `base64` string where the `20` is th length:
```
openssl rand -base64 20
```
> This can be used to generate secrets which the application uses, folllow more notes on how to cycle secrets in this guide.

## Python packages

The following Python packages make the standard set of tools for our projects:

- **SQLAlchemy** - A Python object relational mapper (ORM)
- **alembic** - A database migration tool
- **fastapi-csrf-protect** - A fastapi middleware that protects against cross-site request forgery
- **FastAPI** - A fast, simple, and flexible framework for building HTTP APIs
- **Celery** - A task queue
- **fluent-logger** - A Python logging library that supports fluentd
- **pendulum** - A timezone aware datetime library

Packages are managed using `poetry`, docs available [here](https://python-poetry.org/docs/).

## App directory structure

Directory structure for our application:
```
 src/
 ├─ tests/
 ├─ labs
 |   └─ routers/
 |   └─ tasks/
 |   └─ models/
 |   └─ schema/
 |   └─ alembic/
 |   └─ __init__.py
 ├─ pyproject.toml
 ├─ poetry.lock  

```

### API

FastAPI is a Python framework for building HTTP APIs. It is a simple, flexible, and powerful framework for building APIs and builds upon the popular `pydantic` and `typing` libraries. Our general design for API end points is to break them into packages.

Each submodule must defined a `router` where the handlers defined in the submodule are mounted on. This router should then be bubbled up to the main `router` in the `__init__.py` file and so on until we reach the top of the `routers` package.

In the `routers` package we import the top level routers as `router_modulename` e.g:

```
from .auth import router as router_auth
```

finally the `api.py` imports all the top level routers and mounts them with a prefix:

```python
from .routers import router_auth, router_ext

app = FastAPI(
    .... # other config
    )

app.include_router(router_auth, prefix="/auth")
app.include_router(router_ext, prefix="/ext")
```

> FastAPI camel cases the method name as the short description and uses the docstring as documentation for each endpoint. Markdown is allowed in the docstring.

### Celery based workers

The projects use `Celery` to manage a queue backed by `redis` to schedule and process background tasks. The celery app is run a separate container. In development we use [watchdog](https://github.com/gorakhargosh/watchdog) to watch for changes to the Python files, this is obviously uncessary in production.

The celery app is configured in `celery.py` which reads from the `redis` configuration in `config.py`.

Each task is defined in the `tasks` package with appropriate subpackages. 

To schedule tasks, the API endpoints need to import the task
```python
from ...tasks.email import verification_email
```
and call the `delay` method on the task:
```python
verification_email.delay()
```

A pieced together example of scheduling a task:

```python
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import session_context, session_context
from ...tasks.email import verification_email
from ...config import config

router = APIRouter()

@router.get("/verify")
async def log(request: Request):
    """Verify an account
    """
    verification_email.delay()
    return {"message": "hello world"}
```

> We recommend reading design documentation for the `Celery` project [here](https://docs.celeryproject.org/en/latest/userguide/tasks.html), the general principle is send meta data that the task can use to complete the task not complete, heavy objects. i.e send an ID with some context as opposed to a fully formed object.
### Schema migrations

To initialise `alembic` activate the virtualenv created by `poetry`:

```sh
cd src/
poetry shell
```

and run the initialiser script for async mode:

```sh
alembic init -t async alembic
```

In `alembic.ini` the first parameter is the location of the alembic script, set to the following by default:

```ini
script_location = alembic
```

change this to be relative to the project:

```init
script_location = labs:alembic
```

Since we want the `alembic` to configure itself dynamically (e.g Development container, Production container) we need to drop empty out the value set in `alembic.ini`

```ini
# From
sqlalchemy.url = driver://user:pass@localhost/dbname

# to, as it will be configured in env.py
sqlalchemy.url =
```

you need to import the following in `env.py`, relative imports don't seem to be allowed (pending investigation):

```python
# App level imports
from labs.config import config as app_config
from labs.db import Base
```

and then in `env.py` import the application configuration and set the environment variable, I've decided to do this just after the `config` variable is assigned:

```python
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Read the app config and set sqlalchemy.url
config.set_main_option("sqlalchemy.url", app_config.postgres_dsn)
```

lastly you have to assign your `declerative_base` to the `target_metadata` varaible in `env.py`, so find the line:

```python
target_metadata = None
```

and change it to:

```python
target_metadata = Base.metadata
```

> Note that the `Base` comes from the above imports

And finally you should be able to run your initial migration:

```sh
docker compose exec api sh -c "alembic -c /opt/labs/alembic.ini revision --autogenerate -m 'init db'"
```
producing the following output:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
  Generating /opt/labs/alembic/versions/4b2dfa16da8f_init_db.py ...  done
```
followed by upgrading to the latest revision:
```sh
docker compose exec api sh -c "alembic -c /opt/labs/alembic.ini upgrade head" 
```
producing the following output
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 4b2dfa16da8f, init db
```

## Docker in Development

There are two `Dockerfiles` that are used in Development.  We've decided to name the `Dockerfile` suffixed by their purpose e.g `Dockerfile.api` and `Dockerfile.worker`.

It's important that we put files that should not be copied across into the containers in the `.dockerignore` file. Please try and to keep this up to date as your projects grow. The best security is the absence of files that are not required.

Our current standard image is `python:3.10-slim-buster` this should be updated as the infrastructure changes.

> While it is possible to pass multiple environment files to a container, we are trying to see if it's possible to keep it down to a single file.

The `Dockerfile` for the API simply copies the contents of the `src` directory and then uses `poetry` to install the packages including the application itself.

> The `virtualenvs.create` is set to `false` for containers as `virtualenv` are not required

We run the application using `uvicorn` and pass in `--root-path=/api` for FastAPI to work properly when behind a reverse proxy. FastAPI [recommends](https://fastapi.tiangolo.com/advanced/behind-a-proxy/) setting this at the server level, setting the flag in FastAPI is the last resort. 

## Docker in Production

Multi staged builds
https://docs.docker.com/develop/develop-images/multistage-build/

gunicorn vs uvicorn
https://www.uvicorn.org/deployment/

Providing root path --root-path on unicorn

## Distribution

```
docker build -t anomalyhq/python-lab-server-api:v0.1.0 -f Dockerfile.api .
```

```
docker push anomalyhq/python-labe-server-api:v0.1.0
```

## Resources

- [Deploying FastAPI apps with HTTPS powered by Traefik](https://traefik.io/resources/traefik-fastapi-kuberrnetes-ai-ml/) by Sebastián Ramírez
- [How to Inspect a Docker Image’s Content Without Starting a Container](https://www.howtogeek.com/devops/how-to-inspect-a-docker-images-content-without-starting-a-container/) by James Walker
- [Poetry sub packages](https://github.com/python-poetry/poetry/issues/2270), an open issue to support sub packages in Poetry, which will be handy in splitting up our code base further.
- [Using find namespaces or find namespace package](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#using-find-namespace-or-find-namespace-packages)

## License
Contents of this repository are licensed under the Apache 2.0 license.
