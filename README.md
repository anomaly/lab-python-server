# Lab - Containerised Python server

This lab aims to outline a recipe for building a standardised Python server that can be run in a container. Our major aims are to be able to:
- [X] Expose an API that will eventually sit behind a reverse proxy
- [X] A Postgres server for development
- [X] A Redis server for development
- [ ] Healthcheck endpoint that will validate that the API can get to the database
- [X] Worker processes that will process tasks in the background (using Celery)
- [ ] Provide `Dockerfile` for development and production
- [ ] Log aggregation and monitoring (fluentd)
- [X] CSRF protection
- [ ] Basic endpoints for authentication (JWT and OTP based) - along with recommendations for encryption algorithms

Additionally, we provide:
- [ ] Examples of working with Stripe for payments including handling webhooks
- [ ] Provide a pattern on separating the API endpoints for the hooks for scale

In production (see [Terraform lab project](https://github.com/anomaly/lab-tf-linode)) we will use `Terraform` and `Helm` provision infrastructure and deploy the app in pods. Ideally `Postgres` and `Redis` would be provisioned as a hosted products (Linode is yet to offer this), in the short term they will be installed from official `Charts`.

TODO:
- [ ] Convert the project to be a [Cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/) template

> The approach taken in this guide is to document the tools and commands are they are and not build additional tooling or abstractions. The aim is to educate the user on the tools and how to use them.

Ultimately the output of this lab will be consumed as the `app` and `worker` for the [Terramform Lab](https://github.com/anomaly/lab-tf-linode).

## Using this template

All `docker-compose` files depend on the following environment variables, which can be set by either exporting them before you run the commands or by declaring them in your `.env` file.

- `PROJ_NAME` is a prefix that is used to label resources, object stores
- `PROJ_DOMAIN` is the domain name of the application, this can be set

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

- [**SQLAlchemy**](https://www.sqlalchemy.org) - A Python object relational mapper (ORM)
- [**alembic**](https://alembic.sqlalchemy.org/en/latest/) - A database migration tool
- [**fastapi-csrf-protect**](https://github.com/aekasitt/fastapi-csrf-protect) - A fastapi middleware that protects against cross-site request forgery
- [**FastAPI**](http://fastapi.tiangolo.com) - A fast, simple, and flexible framework for building HTTP APIs
- [**Celery**](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) - A task queue
- **fluent-logger** - A Python logging library that supports fluentd
- [**pendulum**](https://pendulum.eustace.io) - A timezone aware datetime library
- [**pyotp**](https://pyauth.github.io/pyotp/) - A One-Time Password (OTP) generator

Packages are managed using `poetry`, docs available [here](https://python-poetry.org/docs/).

## App directory structure

Directory structure for our application:
```
 src/
 ?????? tests/
 ?????? labs
 |   ?????? routers/         -- FastAPI routers
 |   ?????? tasks/           -- Celery tasks
 |   ?????? models/          -- SQLAlchemy models
 |   ?????? schema/          -- Pydantic schemas
 |   ?????? alembic/         -- Alembic migrations
 |   ?????? __init__.py
 |   ?????? api.py
 |   ?????? celery.py
 |   ?????? config.py
 |   ?????? db.py
 |   ?????? utils.py
 ?????? pyproject.toml
 ?????? poetry.lock  

```

## API

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

## Celery based workers

The projects use `Celery` to manage a queue backed by `redis` to schedule and process background tasks. The celery app is run a separate container. In development we use [watchdog](https://github.com/gorakhargosh/watchdog) to watch for changes to the Python files, this is obviously uncessary in production.

The celery app is configured in `celery.py` which reads from the `redis` configuration in `config.py`.

Each task is defined in the `tasks` package with appropriate subpackages. 

To schedule tasks, the API endpoints need to import the task
```python
from ...tasks.email import verification_email
```
and call the `apply_async` method on the task:
```python
verification_email.apply_async()
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
    verification_email.apply_async()
    return {"message": "hello world"}
```

You can send position arguments to the task, for example:

```python
verification_email.apply_async(args=[user_id])
```

which would be recieved by the task as `user_id` as a positional argument.

> We recommend reading design documentation for the `Celery` project [here](https://docs.celeryproject.org/en/latest/userguide/tasks.html), the general principle is send meta data that the task can use to complete the task not complete, heavy objects. i.e send an ID with some context as opposed to a fully formed object.
## Schema migrations

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
from labs.models import *
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

> Note that the `Base` comes from the above imports and we import everything from our models package so alembic tracks all the models in the application.

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

## Taskfile

[Task](https://taskfile.dev) is a task runner / build tool that aims to be simpler and easier to use than, for example, GNU Make. Wile it's useful to know the actual commands it's easy to use a tool like task to make things easier on a daily basis:

- `task db-revision -- "commit message"` - creates a new revision in the database and uses the parameter as the commit message
- `task db-migrate` - migrates the schema to the latest version

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

When running behind a Reverse Proxy (which would almost always be the case for our applications), FastAPI can accept the root path in numerous ways. This tells FastAPI where to mount the application i.e how the requests are going to be forwarded to the top router so it can stripe away the prefix before routing the requests. So for example the `root` FastAPI application might be mounted on `/api` and the FastAPI will need to strip away the `/api` before handling the request.

FastAPI's [Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/) document describes how to set this up. Where possible the recommend way is to pass this in via the `uvicorn` invocation, see `Dockerfile` for the `api` container:

```Dockerfile
ENTRYPOINT ["uvicorn", "labs.api:app", "--host=0.0.0.0", "--port=80", "--root-path=/api", "--reload"]
```

> Failing everything you can pass the argument in the FastAPI constructor.

## Distribution

We recommend the use of a registry such as [Docker Hub](https://hub.docker.com) to host your images. Assuming you are using Docker Hub, you can build your images using the following command:

```sh
docker build -t anomalyhq/python-lab-server-api:v0.1.0 -f Dockerfile.api .
```

where `v0.1.0` is the version of the image and `Docker.api` is the the `Dockerfile` to use. `python-lab-server` is the the name of the package that will be published on Docker Hub. To publish the image use the following command:

```sh
docker push anomalyhq/python-lab-server-api:v0.1.0
```

where `anomalyhq` is the organisation on Docker Hub and `v0.1.0` is the version of the image.

> Ensure you tag the release on your version control system and write thorough release notes.

## Resources

- [Deploying FastAPI apps with HTTPS powered by Traefik](https://traefik.io/resources/traefik-fastapi-kuberrnetes-ai-ml/) by Sebasti??n Ram??rez
- [How to Inspect a Docker Image???s Content Without Starting a Container](https://www.howtogeek.com/devops/how-to-inspect-a-docker-images-content-without-starting-a-container/) by James Walker
- [Poetry sub packages](https://github.com/python-poetry/poetry/issues/2270), an open issue to support sub packages in Poetry, which will be handy in splitting up our code base further.
- [Using find namespaces or find namespace package](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#using-find-namespace-or-find-namespace-packages)

SQLAlchemy speciific resources:

- [FastAPI with Async SQLAlchemy, SQLModel, and Alembic](https://testdriven.io/blog/fastapi-sqlmodel/) by [Michael Herman](https://testdriven.io/authors/herman/)
- [SQLAlchemy Async ORM is Finally Here!](https://ahmed-nafies.medium.com/sqlalchemy-async-orm-is-finally-here-d560dfaa335d) by [Ahmed Nafies](https://ahmed-nafies.medium.com/)

## License
Contents of this repository are licensed under the Apache 2.0 license.
