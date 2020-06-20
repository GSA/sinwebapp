FROM python

WORKDIR /home/
RUN mkdir /sinwebapp/
WORKDIR /home/sinwebapp/
RUN mkdir ./authentication/ && mkdir ./core/ && mkdir ./static/

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

COPY /sinwebapp/authentication/ /home/sinwebapp/authentication/
COPY /sinwebapp/core/ /home/sinwebapp/core/
COPY /sinwebapp/static/ /home/sinwebapp/static/
COPY /sinwebapp/requirements.txt /home/sinwebapp/requirements.txt
COPY /sinwebapp/manage.py /home/sinwebapp/
COPY init-sinwebapp.sh /home/sinwebapp/

RUN pip install -r ./requirements.txt

EXPOSE 8000

CMD ["bash","./init-sinwebapp.sh","local"]