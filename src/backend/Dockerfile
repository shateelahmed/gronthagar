# pull the official docker image
FROM python:3.12.0-slim

ARG GID=1000
ARG UID=1000

# create user and group for application
RUN groupadd --gid ${GID} www && \
    useradd --uid ${UID} --create-home --home-dir /home/www --system --comment "Container User" --shell /bin/bash --gid www www

# add the following director to path to be able to run the installed packages eg. uvicorn
ENV PATH /home/www/.local/bin:${PATH}

USER ${GID}

# set work directory
WORKDIR /src/backend

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY src/backend/requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .