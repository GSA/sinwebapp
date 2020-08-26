# META DATA
FROM python:3.7.7-slim-stretch
LABEL application="CCDA : Core Contract Data Automation"
LABEL maintainers=["Grant Moore <grant.moore@gsa.gov>","Pramod Ganore <pgnaore@gsa.gov>","Theodros Desta <theodros.desta@gsa.gov>"
LABEL version="prototype-1.0.0"
LABEL description="Internal GSA application for managing SIN data"

## ENVIRONMENT VARIABLES
    ## VCAP_SERVICES: CloudFoundry delivers the application the database credentials through a VCAP_SERVICES environment variable. 
    ## Mimic that configuration in the Docker image for minimal differences in the codebase.
ENV VCAP_SERVICES='{ "aws-rds": [{ \
    "credentials": { \
     "db_name": "sinwebapp", \
     "host": "database", \
     "password": "root", \
     "port": "5432", \
     "username": "postgres" \ 
    }}]}'

## DEPENDENCIES
RUN apt-get update -y && apt-get install -y curl wait-for-it
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get install -y nodejs
RUN npm install -g @angular/cli@8.2.0
WORKDIR /home/
RUN mkdir /sinwebapp/ && mkdir /frontend/
COPY /frontend/package.json /home/frontend/package.json
WORKDIR /home/frontend/
RUN npm install
WORKDIR /home/sinwebapp/
COPY /sinwebapp/requirements.txt /home/sinwebapp/requirements.txt
RUN pip install -r ./requirements.txt

## CREATE PROJECT DIRECTORY STRUCTURE
WORKDIR /home/
RUN mkdir /scripts/
WORKDIR /home/sinwebapp/
RUN mkdir ./authentication/ && mkdir ./core/ && \
    mkdir ./static/ && mkdir ./api/ && mkdir /db/

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

# START UP SCRIPT
COPY /scripts/init-app.sh /home/scripts/init-app.sh
COPY /scripts/util/logging.sh /home/scripts/util/logging.sh
WORKDIR /home/scripts/

# LOCALHOST PORT
EXPOSE 8000

# START UP COMMAND
CMD ["bash","./init-app.sh","container"]