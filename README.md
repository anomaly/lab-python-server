# Lab - Containerised Python server

This lab aims to outline a recipe for building a standardised Python server that can be run in a container. Our major aims are to be able to:
- [X] Expose an API that will eventually sit behind a reverse proxy
- [X] A Postgres server for development
- [X] A Redis server for development
- [ ] Healthcheck endpoint that will validate that the API can get to the database
- [ ] Worker processes that will process tasks in the background (using Celery)
- [ ] Provide `Dockerfile` for development and production
- [ ] Log aggregation and monitoring (fluent-bit)
- [X] CSRF protection
- [ ] Basic endpoints for authentication

In production (see [Terraform lab project](https://github.com/anomaly/lab-tf-linode)) we will use `Terraform` and `Helm` provision infrastructure and deploy the app in pods. Ideally `Postgres` and `Redis` would be provisioned as a hosted products (Linode is yet to offer this), in the short term they will be installed from official `Charts`.

TODO:
- [ ] Convert the project to be a [Cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/) template

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
> This can be used to generate secrets

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
 |   └─ api/
 |   └─ core/
 |   └─ worker
 |   └─ __init__.py
 ├─ pyproject.toml
 ├─ poetry.lock  

```

### API

### Worker

### Schema migrations


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

## Resources

- [Deploying FastAPI apps with HTTPS powered by Traefik](https://traefik.io/resources/traefik-fastapi-kuberrnetes-ai-ml/) by Sebastián Ramírez
- [How to Inspect a Docker Image’s Content Without Starting a Container](https://www.howtogeek.com/devops/how-to-inspect-a-docker-images-content-without-starting-a-container/) by James Walker
- [Poetry sub packages](https://github.com/python-poetry/poetry/issues/2270), an open issue to support sub packages in Poetry, which will be handy in splitting up our code base further.
- [Using find namespaces or find namespace package](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#using-find-namespace-or-find-namespace-packages)

## License
Content of this repository are licensed under the Apache 2.0 license.
