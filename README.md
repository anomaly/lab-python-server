# Lab - Containerised Python server

This lab aims to outline a recipe for building a standardised Python server that can be run in a container. Our major aims are to be able to:
- [X] Expose an API that will eventually sit behind a reverse proxy
- [X] A Postgres server for development
- [X] A Redis server for development
- [ ] Healthcheck endpoint that will validate that the API can get to the database
- [X] Worker processes that will process tasks in the background (using Celery)
- [ ] Provide `Dockerfile` for development and production
- [ ] Log aggregation and monitoring ([parseable](https://github.com/parseablehq/parseable))
- [X] ~~CSRF protection~~ see [#52](https://github.com/anomaly/lab-python-server/issues/52), also see [official guide](https://fastapi.tiangolo.com/tutorial/cors/)
- [X] Basic endpoints for authentication (JWT and OTP based) - along with recommendations for encryption algorithms

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
- `PROJ_FQDN` is the domain name of the application, this can be set
- `ORG_NAME` is the organisation for your Docker registry; Anomaly defaults to using Github

## General notes

Python 3.10 requires the Tinker package to be installed, not sure why this is the case and why the the base Docker image does not contain this. Take a look at the `Dockerfile` where we install this package via `apt`.

On macOS we manage this via Homebrew:
```
brew install python-tk@3.10
```

Handy commands and tools, which we use to help with the infrastructure: 

Use `openssl` to generate a random `hex` string where the `20` is th length:
```
openssl rand -hex 20
```
> This can be used to generate secrets which the application uses, folllow more notes on how to cycle secrets in this guide.

The above is wrapped up as a `Task` endpoints, you need to supply the length of the hash as a parameter:

```sh
task crypt:hash -- 32
```

## Python packages

The following Python packages make the standard set of tools for our projects:

- [**SQLAlchemy**](https://www.sqlalchemy.org) - A Python object relational mapper (ORM)
- [**alembic**](https://alembic.sqlalchemy.org/en/latest/) - A database migration tool
- [**FastAPI**](http://fastapi.tiangolo.com) - A fast, simple, and flexible framework for building HTTP APIs
- **fluent-logger** - A Python logging library that supports fluentd
- [**pendulum**](https://pendulum.eustace.io) - A timezone aware datetime library
- [**pyotp**](https://pyauth.github.io/pyotp/) - A One-Time Password (OTP) generator

Packages are managed using `poetry`, docs available [here](https://python-poetry.org/docs/).

### Keeping up to date

Python packages should be moved up manually to ensure that there aren't any breaking changes.

Use `poetry` to list a set of outdated packages:

```sh
cd src/
poetry show -o
```

this will produce a list of outdated packages. Some of these will be dependencies of our dependencies, so start by upgrading the top level project dependencies (e.g FastAPI or SQLAlchemy):

```sh
poetry add SQLAlchemy@latest
```

If you haven't installed a particular package e.g. `starlette` then be wary of forcefully upgrading it as it might break it's parent dependency e.g. `FastAPI`.

> Note: It's a very good habit not to have packages that you don't use. Please review the package list for every project. This also applies to any handlers e.g `stripe`, if your application does not use payments then please disable these.

## App directory structure

Directory structure for our application:
```
 src/
 ├─ tests/
 ├─ labs
 |   └─ routers/         -- FastAPI routers
 |   └─ tasks/           -- TaskIQ 
 |   └─ models/          -- SQLAlchemy models
 |   └─ schema/          -- Pydantic schemas
 |   └─ alembic/         -- Alembic migrations
 |   └─ __init__.py
 |   └─ api.py
 |   └─ config.py
 |   └─ db.py
 |   └─ utils.py
 ├─ pyproject.toml
 ├─ poetry.lock  

```

## Building your API

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

When running behind a Reverse Proxy (which would almost always be the case for our applications), FastAPI can accept the root path in numerous ways. This tells FastAPI where to mount the application i.e how the requests are going to be forwarded to the top router so it can stripe away the prefix before routing the requests. So for example the `root` FastAPI application might be mounted on `/api` and the FastAPI will need to strip away the `/api` before handling the request.

FastAPI's [Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/) document describes how to set this up. Where possible the recommend way is to pass this in via the `uvicorn` invocation, see `Dockerfile` for the `api` container:

```Dockerfile
ENTRYPOINT ["uvicorn", "labs.api:app", "--host=0.0.0.0", "--port=80", "--root-path=/api", "--reload"]
```

> Failing everything you can pass the argument in the FastAPI constructor.

There are times that you don't want the endpoint to be included in the documentation, which in turns makes client code generators to ignore the endpoint. FastAPI has `include_in_schema` parameter in the `decorator`, which is set to `True` by default. This can be set to `False` to exclude the endpoint from the documentation.

### Routers and Endpoints

FastAPI provides a really nice, clean way to build out endpoints. We recommend that each endpoint must:

- Explicitly define the `status_code` it will return for positive responses
- Throw `HTTPException` on errors with the proper HTTP Error Code and a descriptive message (see `status` package provided by FastAPI)
- Provide a `pydantic` schema for the request and response body (where appropriate)
- Provide a summary of the operation (no matter how trivial) which will make for better documentation

```python
from fastapi import APIRouter, Depends,\
    HTTPException, Query, status

@router.get(
    "/{id}", 
    summary="Get a particular user",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
async def get_user_by_id(
    id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    """ Get a user by their id 
    
    
    """
    user = await User.get(session, id)
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "User not found"
        )

    return user
```

> Ensure that handlers never have unreferenced or variables

### Standards based Design

Anomaly puts great emphasis on code readability and standards. These circle around the following design principles proposed by the languages and the others around protocols (e.g RESTful responses, JSON, etc). We recommend strictly following:

- [**PEP8**](https://www.python.org/dev/peps/pep-0008/) - Python style guide
- [**PEP257**](https://www.python.org/dev/peps/pep-0257/) - Python docstring conventions

Our [web-client](https://github.com/anomaly/lab-web-client) defines the standards for the front end. It's important to note the differences that both environments have and the measure to translate between them. For example:

Python snake case is translated to camel case in JavaScript. So `my_var` becomes `myVar` in JavaScript. This is done by the `pydantic` library when it serialises the data to JSON. 

```python
from pydantic import BaseModel
from humps import camelize

def to_camel(string):
    return camelize(string)

class User(BaseModel):
    first_name: str
    last_name: str = None
    age: float

    class Config:
        alias_generator = to_camel
```

> Source: [CamelCase Models with FastAPI and Pydantic](https://medium.com/analytics-vidhya/camel-case-models-with-fast-api-and-pydantic-5a8acb6c0eee) by Ahmed Nafies

It is important to pay attention to such detail, and doing what is right for the environment and language.

To assist with this `src/labs/schema/utils.py` provides the class `AppBaseModel` which inherits from `pydantic`'s `BaseModel` and configures it to use `humps`'s `camelize` function to convert snake case to camel case. To use it simply inherit from `AppBaseModel`:

```python
from .utils import AppBaseModel

class MyModel(AppBaseModel):
    first_name: str
    last_name: str = None
    age: float
```

> **WARNING:** `humps` is published as `pyhumps` on `pypi`

As per [this issue](https://github.com/anomaly/lab-python-server/issues/27) we have wrapped this


FastAPI will try and generate an `operation_id` based on the path of the router endpoint, which usually ends up being a convoluted string. This was originally reported in [labs-web-client](https://github.com/anomaly/lab-web-client/issues/6). You can provide an `operation_id` in the `decorator` e.g:

```python
@app.get("/items/", operation_id="some_specific_id_you_define")
```

which would result in the client generating a function like `someSpecificIdYouDefine()`.

For consistenty FastAPI docs shows a wrapper function that [globally re-writes](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/?h=operation_id#using-the-path-operation-function-name-as-the-operationid) the `operation_id` to the function name. This does put the onus on the developer to name the function correctly.

# TaskIQ based tasks

To be filled in once we figure out how TaskIQ works.

## SQLAlchemy wisdom

SQLAlchemy is making a move towards their `2.0` syntax, this is available as of `v1.4` which is what we currently target as part of our template. This also brings the use of `asyncpg` which allows us to use `asyncio` with `SQLAlchemy`. 

First and foremost we use the `asyncpg` driver to connect to PostgreSQL. Refer to the property `postgres_async_dsn` in `config.py`.

`asyncio` and the new query mechanism affects the way you write queries to load objects referenced by `relationships`. Consider the following models and relationships:

```python
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column,\
    DeclarativeBase

# Used by the ORM layer to describe models
class Base(DeclarativeBase):
    """
    SQLAlchemy 2.0 style declarative base class
    https://bit.ly/3WE3Srg
    """
    pass

class Catalogue(Base):
    __tablename__ = "catalogue"

    name: Mapped[str]
    description: Mapped[Optional[str]]

    # Catalogues are made of one or more products
    products = relationship("Product",
        back_populates="catalogue",
        lazy="joined"
    )

class Product(Base):
    __tablename__ = "product"

    name: Mapped[str]
    description: Mapped[Optional[str]]

    # Products have one or more prices
    prices = relationship("Price",
        primaryjoin="and_(Product.id==Price.product_id, Price.active==True)",
        back_populates="product"
    )

class Price(Base):
    __tablename__ = "price"

    name: Mapped[str]
    description: Mapped[Optional[str]]
    amount: Mapped[float]
```

For you to be able to access the `Products` and then related `Prices` you would have to use the `selectinload` option to ensure that SQLAlchemy is able to load the related objects. This is because the `asyncio` driver does not support `joinedload` which is the default for `SQLAlchemy`.


```python
from sqlalchemy.orm import selectinload

query = select(cls).options(selectinload(cls.products).\
    selectinload(Product.prices)).\
        where(cls.id == id)
results = await async_db_session.execute(query)
```
> **Note:** how the `selectinload` is chained to the `products` relationship and then the `prices` relationship.

Our base project provides serveral `Mixin`, a handy one being the `ModelCRUDMixin` (in `src/labs/models/utils.py`). It's very likely that you will want to write multiple `getters` for your models. To facilitate this we encourage each Model you have overrides `_base_get_query` and returns a `query` with the `selectinload` options applied. 

```python
@classmethod
def _base_get_query(cls):
    query = select(cls).options(selectinload(cls.products).\
        selectinload(Product.prices))
    return query
```

This is then used by the `get` method in the `ModelCRUDMixin` to load the related objects and apply any further conditions, or orders:
    
```python
@classmethod
async def get(cls, async_db_session, id):
    query = cls._base_get_query()
    results = await async_db_session.execute(query)
    (result,) = results.one()
    return result
```

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

> **Note:** that the `Base` comes from the above imports and we import everything from our models package so alembic tracks all the models in the application.

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

- `task db:revision -- "commit message"` - creates a new revision in the database and uses the parameter as the commit message
- `task db:migrate` - migrates the schema to the latest version
- `task dev:psql` - 	postgres shell in the database container
- `task dev:pyshell` - 	get a `python` session on the api container which should have access to the entire application

## Docker in Development

It's important that we put files that should not be copied across into the containers in the `.dockerignore` file. Please try and to keep this up to date as your projects grow. The best security is the absence of files that are not required.

Our current standard image is `python:3.10-slim-buster` this should be updated as the infrastructure changes.

> While it is possible to pass multiple environment files to a container, we are trying to see if it's possible to keep it down to a single file.

The `Dockerfile` for the API simply copies the contents of the `src` directory and then uses `poetry` to install the packages including the application itself.

> The `virtualenvs.create` is set to `false` for containers as `virtualenv` are not required

We run the application using `uvicorn` and pass in `--root-path=/api` for FastAPI to work properly when behind a reverse proxy. FastAPI [recommends](https://fastapi.tiangolo.com/advanced/behind-a-proxy/) setting this at the server level, setting the flag in FastAPI is the last resort. 

`Dockerfile` is the configuration referenced by `docker-compose.yml` for development and `Dockerfile.prod` is the configuration referenced by `docker-compose.prod.yml` for production. For Kubernetes based deployment please reference `Dockerfile.prod`.

## Docker in Production

Multi staged builds
https://docs.docker.com/develop/develop-images/multistage-build/

gunicorn vs uvicorn
https://www.uvicorn.org/deployment/


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

- [Deploying FastAPI apps with HTTPS powered by Traefik](https://traefik.io/resources/traefik-fastapi-kuberrnetes-ai-ml/) by Sebastián Ramírez
- [How to Inspect a Docker Image’s Content Without Starting a Container](https://www.howtogeek.com/devops/how-to-inspect-a-docker-images-content-without-starting-a-container/) by James Walker
- [Poetry sub packages](https://github.com/python-poetry/poetry/issues/2270), an open issue to support sub packages in Poetry, which will be handy in splitting up our code base further.
- [Using find namespaces or find namespace package](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#using-find-namespace-or-find-namespace-packages)

SQLAlchemy speciific resources:

- [FastAPI with Async SQLAlchemy, SQLModel, and Alembic](https://testdriven.io/blog/fastapi-sqlmodel/) by [Michael Herman](https://testdriven.io/authors/herman/)
- [SQLAlchemy Async ORM is Finally Here!](https://ahmed-nafies.medium.com/sqlalchemy-async-orm-is-finally-here-d560dfaa335d) by [Ahmed Nafies](https://ahmed-nafies.medium.com/)


## Developer Tools

- [Better Jinja](https://marketplace.visualstudio.com/items?itemName=samuelcolvin.jinjahtml) - Jinja syntax highlighting for [VS Code](https://github.com/samuelcolvin/jinjahtml-vscode) by @SamuelColvin (accepted as part of PAP [#47](https://github.com/anomaly/lab-python-server/issues/47)

## License
Contents of this repository are licensed under the Apache 2.0 license.
