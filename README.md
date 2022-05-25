# Lab Server Python

Python 3.10 required Tinker
```
brew install python-tk@3.10
```

Create random
```
openssl rand -base64 20 > /tmp/lab-python-server.key
```

# Python package and Poetry

python -m venv .env

# Docker in Development

.dockerignore file
multiple env files

# Dokcer in Production

Multi staged builds
https://docs.docker.com/develop/develop-images/multistage-build/

gunicorn vs uvicorn
https://www.uvicorn.org/deployment/

# Resources

https://traefik.io/resources/traefik-fastapi-kuberrnetes-ai-ml/

Debugging
https://www.howtogeek.com/devops/how-to-inspect-a-docker-images-content-without-starting-a-container/


https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#using-find-namespace-or-find-namespace-packages