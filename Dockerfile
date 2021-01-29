# META DATA
FROM python:3.7.7-slim-stretch
LABEL application="CCDA : Core Contract Data Automation"
LABEL maintainers=["Grant Moore <grant.moore@gsa.gov>","Pramod Ganore <pganore@gsa.gov>","Theodros Desta <theodros.desta@gsa.gov>"]
LABEL version="prototype-1.0.0"
LABEL description="Internal GSA application for managing SIN data"

## OS DEPENDENCIES
RUN apt-get update -y && apt-get install -y curl wait-for-it build-essential\ 
    python-dev default-libmysqlclient-dev

## CREATE PROJECT DIRECTORY STRUCTURE
WORKDIR /home/
RUN mkdir ./sinwebapp/ && mkdir ./frontend/ && mkdir ./scripts

# APPLICATION DEPENDENCIES
COPY /sinwebapp/requirements.txt /home/sinwebapp/requirements.txt
WORKDIR /home/sinwebapp/
RUN pip install -r ./requirements.txt
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get install -y nodejs
RUN npm install -g @angular/cli@10.1.1

# DEFINE VOLUMES
VOLUME /home/sinwebapp/ /home/frontend/

# PRODUCTION / DEVELOPMENT SERVER PORT
EXPOSE 8000 4200

# START UP SCRIPTS
WORKDIR /home/scripts/
COPY /scripts/ /home/scripts/
CMD ["bash","./init-app.sh","container"]