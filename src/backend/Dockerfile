# pull the official docker image
FROM python:3.12.0-slim

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