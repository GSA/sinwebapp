# ARGUMENTS
## docker-compose will automatically provide the arguments specified in the
## docker-composer.yml. If building the image manually, make sure to pass
## in the appropriate values of these arguments via
##
##      docker build --build-arg ANGULAR_VERSION=10.1.1. --build-arg PYTHON_VERSION=3.7.7

ARG ANGULAR_VERSION
ARG PYTHON_VERSION

# META DATA
## TODO: replace version with ARG
## provide env var as ARGS in build-container.sh

FROM python:${PYTHON_VERSION}-slim-stretch
LABEL application="CCDA : Core Contract Data Automation"
LABEL maintainers=["Grant Moore <grant.moore@gsa.gov>","Pramod Ganore <pganore@gsa.gov>","Theodros Desta <theodros.desta@gsa.gov>"]
LABEL version="prototype-1.0.0"
LABEL description="Internal GSA application for managing SIN data"

## DEPENDENCIES
RUN apt-get update -y && apt-get install -y curl wait-for-it
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get install -y nodejs
## TODO: replace version with ARG
## provider env var as ARGS in build-container.sh
RUN npm install -g @angular/cli@${ANGULAR_VERSION}
WORKDIR /home/
RUN mkdir ./sinwebapp/ && mkdir ./frontend/
COPY /frontend/package.json /home/frontend/package.json
WORKDIR /home/frontend/
RUN npm install
WORKDIR /home/sinwebapp/
COPY /sinwebapp/requirements.txt /home/sinwebapp/requirements.txt
RUN pip install -r ./requirements.txt

## CREATE PROJECT DIRECTORY STRUCTURE
WORKDIR /home/
RUN mkdir ./scripts/
WORKDIR /home/sinwebapp/
RUN mkdir ./authentication/ && mkdir ./core/ && \
    mkdir ./static/ && mkdir ./api/ && mkdir ./db/ && \
    mkdir ./files/ && mkdir ./notification/ && mkdir ./tests/

## BUILD FRONTEND
WORKDIR /home/frontend/
COPY /frontend/  /home/frontend/
RUN ng build --prod --output-hashing none

## BUILD BACKEND
WORKDIR /home/sinwebapp/
COPY /sinwebapp/authentication/ /home/sinwebapp/authentication/
COPY /sinwebapp/api/ /home/sinwebapp/api/
COPY /sinwebapp/core/ /home/sinwebapp/core/
COPY /sinwebapp/debug.py /home/sinwebapp/
COPY /sinwebapp/manage.py /home/sinwebapp/
COPY /sinwebapp/db/ /home/sinwebapp/db/
COPY /sinwebapp/files/ /home/sinwebapp/files/
COPY /sinwebapp/tests/ /home/sinwebapp/tests/
COPY /sinwebapp/static/ /home/sinwebapp/static/

# START UP SCRIPT & ASSETS
COPY /scripts/init-migrations.sh /home/scripts/init-migrations.sh
COPY /scripts/init-app.sh /home/scripts/init-app.sh
COPY /scripts/util/logging.sh /home/scripts/util/logging.sh
WORKDIR /home/scripts/

# LOCALHOST PORT
EXPOSE 8000

# START UP COMMAND
CMD ["bash","./init-app.sh","container"]