# <b>SIN Web App: A Work In Progress</b>

This is a sample application that integrates an Angular frontend with a Django WSGI application deployed onto a <i>gunicorn</i> web server. It uses a <b>cloud.gov</b> OAuth2 client and a pre-configured python library specifically for that client, <i>cg-django-uaa</i>, to authenticate users, in addition to regular authentication Django backend plugins. The application has been containerized through a <i>Dockerfile</i> that creates an image of the application.

Note the <i>manifest.yml</i> for CloudFoundry names this app <b>sinweb</b>, so when it is pushed to the cloud, it will live at [https://sinweb.app.cloud.gov](https://sinwebapp.app.cloud.gov). Edit the application name accordingly, if you need another domain route. 

The application is built from source on the cloud, not the Docker image. The Docker image is soley for ease of local development. 

## Quickstart Pointers

1. After logging into the <i>cf cli</i> and making changes to the code, use <i>/scripts/push-to-cf.sh</i> to install and build the application proplery before pushing to the cloud. The Angular Frontend needs rebuilt and the artifacts deployed to the cloud in order for changes in code to be reflected in the deployment.  

2. <i>docker-compose up</i> will create a local image of the application and run it on a container exposed at <i>localhost:8000</i>. Use <i>docker-compose down</i> to remove the containers running the application locally.

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)
- [Git For Windows](https://git-scm.com/download/win)
- [cf cli](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html)

## Local Environment

### Additional Prerequisites For Local Development

<b>Note you must be using a Linux distro to develop locally!</b> The python web server <i>gunicorn</i> is Unix based and incompatible with Windows!

- [Python](https://www.python.org/downloads/)
- [NodeJs](https://nodejs.org/en/download/)
- [PostgreSQL](https://www.postgresql.org/download/)

Before you build the application, you will need to ensure <i>postgres</i> is running on port 5432 and has an empty database the application can connect to. By default, the application searches for a database named <i>sinwebapp</i>. You can edit <b>db_creds</b> variable in <i>/sinwebapp/core/settings.py</i> to configure you database connection. The models and migrations from Django will take care of the actual schema of the database, but you must ensure the database atleast exists first.

You can build the application from source. First create a virtual Python environment in the project's root folder

> python -m venv .venv

Then activate it,

> source ./.venv/Scripts/activate

Navigate to the <i>/sinwebapp/</i> project and install the project requirements,

> pip install -r requirements.txt

Next, you will need to build the frontend. Navigate to the <i>/scripts/</i> directory and execute the BASH script,

> bash build-frontend.sh

This will install all of the frontend dependencies and build the frontend project and output it in the <i>/sinwebapp/static/</i> directory so the project can be statically served. You can then start the app from the <i>/scripts/</i> directory with another script, providing it an argument of "local"

> bash init-app.sh local

## Container Environment

1. The <i>docker-compose.yml</i> sets up the local application automatically. It reads in the <i>local.env</i> file and sets the environment for the application. Open the <i>local.env</i> file in project's root directory and verify the following variable is set,

> ENVIRONMENT=container

This will be loaded into the <i>settings.py</i> configuration file and allow certain settings to be parsed for their respective environments, <i>container</i> or <i>cloud</i>. Note in the <i>manifest.yml</i> for CloudFoundry, an environment variable is set,

> env: ENVIRONMENT: cloud

You will also find two other environment variables in the <i>local.env</i> file, <b>UAA_CLIENT_ID</b> and <b>UAA_CLIENT_SECRET</b>. The <b>UAA_CLIENT_ID</b> and <b>UAA_CLIENT_SECRET</b> do not matter for local docker deployments; they are only there to maintain minimal differences in the codebase for cloud and local docker deployments. In other words, they make life easier. 

You will also need to set the superuser for the program; this user will be able to add and delete users from the database. The environment variables <b>DJANGO_SUPERUSER_USERNAME</b>, <b>DJANGO_SUPERUSER_EMAIL</b> and <b>DJANGO_SUPERUSER_PASSWORD</b> set the credentials for this user. 

2. From project's root directory, run 

> docker-compose up  
    
This will build the <b><b>sinwebapp</b></b> locally from the <i>Dockerfile</i> and orchestrate it with a <b>postgres</b> image. The database credentials are set up in the <i>docker-compose.yml</i> file for the database image, but are also hard-coded into the <i>Dockerfile</i> through an environment variable <b>VCAP_SERVICES</b> in order to mimic how a CloudFoundry deployment will pass in database credentials.

You can execute

> docker-compose up -d

To run the containers as detached, i.e. in the background.

3. Remove the containers with the following command,

> docker-compose stop<br>
> docker-compose down

## CloudFoundry Environment

This section gives a brief overview on how to setup the environment for this application on cloud.gov implementation of CloudFoundry. The BASH script in <i>/scripts/setup/setup-cloud-env.sh</i> will take care of all of the steps given below, provided you are logged into the the <i>cf cli</i> and have targetted the correct organization and space. For documentation's sake, the contents of this script are described:

1. Stage the app without starting it

> cf push --no-start

2. Create cloud-gov identity provider service and service key and then bind it to app (replace BASE_URL with web app URL),

> cf create-service cloud-gov-identity-provider oauth-client sin-oauth <br>
> cf create-service-key sin-oauth sin-key -c '{"redirect_uri": ["BASE_URL/auth","BASE_URL/logout"]}'<br>
> cf bind-service sinwebapp sin-oauth -c '{"redirect_uri": ["BASE_URL/auth","BASE_URL/logout"]}'<br>

The first line is of the form <i>'cf create-service <b>SERVICE_PLAN</b> <b>SERVICE_INSTANCE</b> <b>APP_INSTANCE</b>'</i>, where <b>SERVICE_PLAN</b> is the type of service being implemented, <b>SERVICE_INSTANCE</b> is the name of the particular service created and the <b>APP_INSTANCE</b> is the application space is which the service in made available.

The second line generates a key so that the application instance can leverage this service. The third line binds the application instance to the service instance.

3. Retrieve client ID and client secret from service key,

> cf service-key sin-oauth sin-key

4. Django reads the client ID and client secret from Environment Variables. In the local setup, these are contained in the <i>local.env</i>. To set them on CloudFoundry, execute these commands,

> cf set-env sinwebapp UAA_CLIENT_ID "client id goes here"<br>
> cf set-env sinwebapp UAA_CLIENT_SECRET "client secret goes here"

5. Create a PostgresSql service,

> cf create-service aws-rds medium-psql sin-sql 

Again, this command uses the form <i>'cf create-service <b>SERVICE_PLAN</b> <b>SERVICE_INSTANCE</b> <b>APP_INSTANCE</b>'</i> just like in step 2, since we are creating a service in an application space. No need to bind the <i>sin-sql</i> service to app, since it is included in the manifest. Note: the cloud-gov-identity-provider cannot be specified in the manifest since the application must first be configured with the client ID and client secret that is provided in the service key. 

6. You will need to set up environment variables for the superuser of the Django database service. This will be the user in charge of adding users and managing permissions. Use the commands

>cf set-env sinwebapp DJANGO_SUPERUSER_NAME /put/name/here<br>
>cf set-env sinwebapp DJANGO_SUPERUSER_EMAIL /put/email/here

Since the authentication is taken care of by the <i>cg-django-uaa</i> library, you do not need to set a password. The password will be the same password set within the cloud.gov domain.

7. Restage and start the app

> cf restage<br>
> cf start

## Frontend

### Environment

In the <i>/frontend/environments/</i> directory, there is a TypeScript file that controls the Angular Service HTTP routing. When the variable <b>production</b> is set to true, Angular services will direct their HTTP calls to the backend on the cloud. When <b>production</b> is set to false, Angulars services will direct their HTTP calls to the localhost backend. Be sure to set this variable to the proper value during development and when pushing to production!

### Context

The <b>production</b> environment variable for the Angular application affects the <i>ContextService</i>. The <i>ContextService</i> is injected into other service instances to provide application-wide configuration, such as URLs to the backend API and other application properties that change based on the type of the deployment: <b>local</b> or <b>production</b>. 

## Building and Pushing

Currently, there is no build pipeline that will automatically compile and deploy the Angular frontend to the cloud. For the time being, when deploying the application to the cloud, you will need to manually build the frontend with the <i>build-frontend.sh</i> BASH script contained in the <i>/scripts/</i> folder before pushing. The Angular build is configured to output its artifacts into the <i>/sinwebapp/static/frontend/</i> directory, which is statically served through the Django framework. 

Once the frontend is built, you can push the application to CloudFoundry.

In other words, if you add code to the frontend, be sure to run this command from the project's root directory:

> bash ./scripts/build-frontend.sh

Before pushing to the cloud,

> cf push

These commands are so frequent they have been further condensed into another BASH script. The BASH script, <i>/scripts/push-to-cf.sh</i>, takes care of installing and building the frontend for you, as long as you already logged into the <i>cf cli</i>.

> bash ./scripts/push-to-cf.sh

## Work Flows

The artifacts from the Angular build are outputted into the <i>/sinwebapp/static/</i> directory, where the Django web framework serves them up through <b>gunicorn</b>. The HTML templates in the Django backend are configured to load in these artifacts; since the Angular app enters through these Django templates, there is no <i>index.html</i> in the <i>/frontend/</i> folder. In other words, each Angular app launched from a different Django template is an entirely distinct instance of a separate Angular application.

## Database Configuratoin

The file <i>/sinwebapp/authentication/db_init.py</i> creates Groups, Permissions and Users within three separate functions, using Django's built-in class models. These functions are added to the Migration queue within <i>/sinwebapp/authentication/migrations/</i>. The initialization script that starts up both container and cloud instances of the application applies these migrations to the host database. 

## Routes & Endpoints

Listed below are the current routes used by each component of the application, the Angular frontend and the Django backend,

Django Static HTML Endpoint
- /
- /logout
- /success

Application API Endpoints
- /api/user

Third Party Endpoints
- /auth/login
- /auth/callback
- /fake/oauth/authorize
- /fake/oauth/token

Frontend Routes
- 404: ?

## Superuser

The superuser of the database is controlled by environment variabless, DJANGO_SUPERUSER_*. These variables are loaded into it the initialization script and passed into Django while it is starting up. The local environment variables are set in the <i>local.env</i> file, while the cloud environment variables need to be set with the <i>cf cli</i>

## TODO
- [x] reset service-key redirect uri on cloud.gov
- [x] determine how to protect certain endpoints from unauthenticated individuals
- [x] create users with roles in database
- [x] integrate angular frontend application with django backend framework
- [ ] bind roles to html on redirect page after successful login 
- [ ] create pipeline to build frontend and deploy to cloud
- [ ] load in database credentials for local deployments through VCAP_SERVICES environment variable to mimic cloud deployments

## Useful Links
### Core Application
- [Django: Data Migrations](https://docs.djangoproject.com/en/3.0/topics/migrations/#data-migrations)
- [Django: Authentication Documentation](https://docs.djangoproject.com/en/3.0/topics/auth/default/)<br>
- [Django: Groups Class documentation](https://docs.djangoproject.com/en/3.0/ref/contrib/auth/#django.contrib.auth.models.Group)<br>
- [Django: Permissions Class documentation](https://docs.djangoproject.com/en/3.0/topics/auth/default/#permissions-and-authorization)<br>
- [Django: User Class documentation](https://docs.djangoproject.com/en/3.0/topics/auth/default/#user-objects)<br>
- [Gunicorn Documentation](https://docs.gunicorn.org/en/stable/run.html)
### Authentication
- [Cloud.gov Identity Provider](https://cloud.gov/docs/services/cloud-gov-identity-provider/) <br/>
- [Leveraging Cloud.gov Authentication](https://cloud.gov/docs/management/leveraging-authentication/) <br/>
- [CloudFoundry: Service Keys](https://docs.cloudfoundry.org/devguide/services/service-keys.html) <br/>
- [Python Library cg-django-uaa Documentation](https://cg-django-uaa.readthedocs.io/en/latest/quickstart.html)<br/>
### Relevant Stack Discussions
- [Django, Add Auth Groups Programmatically](https://stackoverflow.com/questions/25024795/django-1-7-where-to-put-the-code-to-add-groups-programmatically/25803284#25803284)<br>
- [Creating JSON HttpResponse In Django](https://stackoverflow.com/questions/2428092/creating-a-json-response-using-django-and-python)