# While optional this tells the Docker builder of the version
# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.12-bookworm

# Base image for Python applications
# This image is particularly for a web server using uvicorn
FROM python:${PYTHON_VERSION}

# Expose ports which is proxied via traefik
EXPOSE 80

# Update the based image to latest versions of packages
# python 3.10 seems to want python3-tk installed
RUN apt update \
    && apt -y upgrade \
    && apt install -y --no-install-recommends gcc python3-dev \
    build-essential libpq-dev python3-tk postgresql-client curl \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

# Install task from their servers, not this requires curl
# so you must only have this tkas post the apt updates
RUN sh -c "$(curl --location https://taskfile.dev/install.sh)" \
    -- -d -b /usr/local/bin

# Copy the files in the src directory which is the app package
# and the dependency matrix dedescribed by pyproject.toml
WORKDIR /opt/${PROJ_NAME}
COPY ./src/. .
COPY Taskfile.prod.yml Taskfile.yml

# Ask poetry to install all packages including the app
# not in virtual machine as we are in a container
# In prodduction add --no-dev to poetry installation
RUN pip3 install --upgrade pip
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

# The app package will be located in /opt/appname so run
# uvicorn at this level so it sees the package
WORKDIR /opt/

# Labels are used to identify the image
LABEL org.opencontainers.image.source="https://github.com/anomaly/${PROJ_NAME}"
LABEL org.opencontainers.image.description="A Python web server using FastAPI and Uvicorn"
LABEL org.opencontainers.image.licenses="Apache-2.0"
