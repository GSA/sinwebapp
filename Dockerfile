FROM python

WORKDIR /home/
RUN mkdir /sinwebapp/
WORKDIR /home/sinwebapp/
RUN mkdir ./authentication/ && mkdir ./sinapp/ && mkdir ./static/

# Configured to mimic CloudFoundry deployment for minimal changes 
# between local and cloud deployments.
ENV VCAP_SERVICES='{ "aws-rds": [{ \
    "credentials": { \
     "db_name": "sinwebapp", \
     "host": "sin_postgres", \
     "password": "root", \
     "port": "5432", \
     "username": "postgres" \ 
    }}]}'
# Edit these ENVs to correspond to Cloud.Gov service credentials
ENV UAA_CLIENT_ID='client id goes here'
ENV UAA_CLIENT_SECRET='client secret goes here'

COPY /authentication/ /home/sinwebapp/authentication/
COPY /sinapp/ /home/sinwebapp/sinapp/
COPY /static/ /home/sinwebapp/static/
COPY requirements.txt /home/sinwebapp/requirements.txt
COPY manage.py /home/sinwebapp/
COPY init-sinwebapp.sh /home/sinwebapp/

RUN pip install -r ./requirements.txt

EXPOSE 8000

CMD ["bash","./init-sinwebapp.sh","local"]