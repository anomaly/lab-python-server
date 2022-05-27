# Lab - Containerised Python server

This lab aims to outline a recipe for building a standardised Python server that can be run in a container. Our major aims are to be able to:
- [ ] Expose an API that will eventually sit behind a reverse proxy
- [ ] A Postgres server for development
- [ ] A Redis server for development
- [ ] Healthcheck endpoint that will validate that the API can get to the database
- [ ] Worker processes that will process tasks in the background (using Celery)
- [ ] Provide `Dockerfile` for development and production
- [ ] Log aggregation and monitoring (fluentd)

In production (see [Terraform lab project](https://github.com/anomaly/lab-tf-linode)) we will use `Terraform` and `Helm` provision infrastructure and deploy the app in pods. Ideally `Postgres` and `Redis` would be provisioned as a hosted products (Linode is yet to offer this), in the short term they will be installed from official `Charts`.

TODO:
- [ ] Convert the project to be a [Cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/) template

## FastAPI based server

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

## Worker

Python 3.10 required Tinker
```
brew install python-tk@3.10
```

Create random
```
openssl rand -base64 20 > /tmp/lab-python-server.key
```

## Python package and Poetry

python -m venv .env

## Docker in Development

.dockerignore file
multiple env files

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