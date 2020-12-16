# META DATA
## TODO: replace version with ARG
## provide env var as ARGS in build-container.sh

FROM python:3.7.7-slim-stretch
LABEL application="CCDA : Core Contract Data Automation"
LABEL maintainers=["Grant Moore <grant.moore@gsa.gov>","Pramod Ganore <pganore@gsa.gov>","Theodros Desta <theodros.desta@gsa.gov>"]
LABEL version="prototype-1.0.0"
LABEL description="Internal GSA application for managing SIN data"

## OS DEPENDENCIES
    ## TODO: replace version with ARG
        ## NOTE: provider env var as ARGS in build-container.sh
RUN apt-get update -y && apt-get install -y curl wait-for-it
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get install -y nodejs
RUN npm install -g @angular/cli@10.1.1

## CREATE PROJECT DIRECTORY STRUCTURE
WORKDIR /home/
RUN mkdir ./sinwebapp/ && mkdir ./frontend/ && mkdir ./scripts

# APPLICATION DEPENDENCIES
COPY /frontend/package.json /home/frontend/package.json
WORKDIR /home/frontend/
RUN npm install

WORKDIR /home/sinwebapp/
COPY /sinwebapp/requirements.txt /home/sinwebapp/requirements.txt
RUN pip install -r ./requirements.txt

## BUILD FRONTEND
WORKDIR /home/frontend/
COPY /frontend/  /home/frontend/
RUN ng build --prod --output-hashing none

COPY /scripts/ /home/scripts/
VOLUME /home/sinwebapp/ /home/frontend/ /home/scripts/

# PRODUCTION SERVER / DEVELOPMENT SERVER PORT
EXPOSE 8000 4200

# START UP COMMAND
WORKDIR /home/scripts/
CMD ["bash","./init-app.sh","container"]