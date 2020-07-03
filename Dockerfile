FROM python:3.7.7-slim-stretch

## ENVIRONMENT VARIABLES
    ## VCAP_SERVICES: Delivers Database Credentials to App
    # Configured to mimic CloudFoundry deployment for minimal
    # changes between local and cloud deployments.
ENV VCAP_SERVICES='{ "aws-rds": [{ \
    "credentials": { \
     "db_name": "sinwebapp", \
     "host": "database", \
     "password": "root", \
     "port": "5432", \
     "username": "postgres" \ 
    }}]}'

## DEPENDENCIES
RUN apt-get update -y && apt-get install -y curl

## CREATE PROJECT DIRECTORY STRUCTURE
WORKDIR /home/
RUN mkdir /sinwebapp/ && mkdir /frontend/
WORKDIR /home/sinwebapp/
RUN mkdir ./authentication/ && mkdir ./core/ && mkdir ./static/

## BUILD FRONTEND
WORKDIR /home/frontend/
COPY /frontend/  /home/frontend/
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get install -y nodejs
RUN npm install -g @angular/cli@8.2.0
RUN npm install
RUN ng build --prod --output-hashing none

## BUILD BACKEND
WORKDIR /home/sinwebapp/
COPY /sinwebapp/authentication/ /home/sinwebapp/authentication/
COPY /sinwebapp/core/ /home/sinwebapp/core/
COPY /sinwebapp/debug.py /home/sinwebapp/
COPY /sinwebapp/manage.py /home/sinwebapp/
COPY /sinwebapp/scripts/init-sinwebapp.sh /home/sinwebapp/
COPY /sinwebapp/requirements.txt /home/sinwebapp/requirements.txt
RUN pip install -r ./requirements.txt

EXPOSE 8000

CMD ["bash","./init-sinwebapp.sh","container"]