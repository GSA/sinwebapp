
### Documentation Navigation

 [^ ReadMe ^](../README.md) | [Development >>](DEVELOPMENT.md)

# Setup

## Quickstart Pointers

1. After logging into the <i>cf cli</i> and making changes to the code, use <i>/scripts/cloud/cf-push.sh</i> with the argument <i>build</i>, i.e.,

> bash PROECT_ROOT/scripts/cloud/cf-push.sh build

This will install dependencies and build the application properly before pushing to the cloud.gov. This is done because the Angular Frontend needs rebuilt and the artifacts deployed to the cloud in order for changes in code to be reflected in the deployment. This script contains the commands to build the Angular frontend properly for production deployment.

2. In the <i>/env/</i>, you will find a <i>.sample.env</i> file that you will need to copy into <i>/env/local.env</i> and <i>/env/container.env</i>. These environment variables are pulled in through the <i>/sinwebapp/core/settings.py</i> to provide application-wide configuration for various features and functionality, such as the database connection, the email notification connection, etc. These files will automatically be created and copied if you run the <i>/scripts/setup/setup-local-env.sh</i> script, but they will still need adjusted for your specific environment. See .env files for more documentation.

3. <i>docker-compose up</i> will create a local image of the application and run it on a container exposed at <i>localhost:8000</i>. It will link to a <b>postgres</b> database over a Docker network on port 5432. The database is not directly exposed to localhost, so it can only be accessed through the application's api. Once you are done, use <i>docker-compose down</i> to remove the containers running the application through Docker Compose. Note: A useful script is the <i>/scripts/build-container.sh</i>, as it will automatically remove any running containers and purge any dangling containers leftover from previous builds, before building a fresh image of the application. To accomplish this, use the script without any arguments,

> bash PROJECT_ROOT/scripts/build-container.sh

And then execute,

> docker-compose up

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)
- [Git For Windows](https://git-scm.com/download/win)
- [cf cli](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html)

## Local Environment

### Additional Prerequisites For Local Development

<b>Note you must be using a Linux distro to develop locally!</b> The python web server <i>gunicorn</i> is Unix based and incompatible with Windows! If you want to develop and test locally on Windows, please use Docker! See next section.

- [Python](https://www.python.org/downloads/)
- [NodeJs](https://nodejs.org/en/download/)
- [PostgreSQL](https://www.postgresql.org/download/)

Before you build the application, you will need to ensure <b>postgres</b> is running on port 5432 and has an empty database the application can connect to. By default, the application searches for a database named <i>sinwebapp</i>. You can edit the .<i>.env</i> file to configure your database connection, which in turn gets feed into <b>db_creds</b> variable in <i>/sinwebapp/core/settings.py</i>. The models and migrations from Django will take care of the actual schema of the database, but you must ensure the database atleast exists first.

Make sure you activate your <i>local.env</i> file before running any commands through the <b>django-admin</b>. Make sure you have copied the <i>.sample.env</i> and adjusted the variable values. Source the <i>init-env.sh</i> script and provide it an argumnet of <i>local</i> to get started, i.e.

> source PROJECT_ROOT/scripts/util/init-env.sh local

This will load in neccessary environment variables that will configure Django's connection to the database, email server, etc. Open the <i>local.env</i> for more documentation on all the configuration options.

To build the application from source, first create a virtual Python environment in the project's root folder

> python -m venv .venv

Then activate it,

> source PROJECT_ROOT/.venv/Scripts/activate

Navigate to the <i>/sinwebapp/</i> project directory and install the project requirements,

> pip install -r requirements.txt

Next, you will need to build the frontend and deploy it onto the server. You could do this manually, but all the necessary commands have been packaged in a script. Navigate to the <i>/scripts/</i> directory and locate the <i>init-app.sh</i> BASH script. This script will install all of the frontend dependencies and build the frontend project, in addition to ensuring all migrations are up-to-date, and finally output all the artifacts into the <i>/sinwebapp/static/</i> directory so the project can be statically served. It will then start the app's server. This script is also used when orchestrating the application through containers or on the cloud, so provide it an argument of "local", or in other words, execute the following command,

> bash init-app.sh local

The environment file in <i>/env/local.env</i> defines the local environment configuration. It is loaded during the <i>init-app.sh</i> script if an argument of "local" is provided, in case you forgot to source the <i>/scripts/util/init-env.sh</i> script to set the environment variables.

## Container Environment

1. The <i>docker-compose.yml</i> builds the web application and connects it to a <i>postgres</i> database. It reads in the <i>container.env</i> file and sets the environment for the application. Open the <i>/env/container.env</i> file in project's root directory and verify the following variable is set,

> ENVIRONMENT=container

This will be loaded into the <i>settings.py</i> configuration file and allow certain settings to be parsed for their respective environments, <i>local</i>, <i>container</i> or <i>cloud</i>. Note in the <i>manifest.yml</i> for CloudFoundry, an environment variable is set,

> env: ENVIRONMENT: cloud

Likewise, the <i>local.env</i> sets this variable for local deployments.

You will also find two other environment variables in the <i>container.env</i> file, <b>UAA_CLIENT_ID</b> and <b>UAA_CLIENT_SECRET</b>. The <b>UAA_CLIENT_ID</b> and <b>UAA_CLIENT_SECRET</b> do not matter for local or docker deployments; they are only there to maintain minimal differences in the codebase for cloud and docker deployments. In other words, they make life easier. If you are curious about their function, see the [cg-django-uaa documentation](https://cg-django-uaa.readthedocs.io/en/latest/quickstart.html).

You will also need to set the superuser for the program; this user will be able to add and delete users from the database, assign users to groups, etc, through the Django admin screen. The environment variables <b>DJANGO_SUPERUSER_USERNAME</b> and <b>DJANGO_SUPERUSER_EMAIL</b> set the credentials for this user. 

There are environment variables in this file for AWS S3 services and email server connections as well. Read the .env file for more documentation on each variable and its purpose.

2. From project's root directory, run 

> docker-compose up  
    
This will build the <b><b>sinwebapp</b></b> locally from the <i>Dockerfile</i> and orchestrate it with a <b>postgres</b> image. The database credentials are set up in the <i>docker-compose.yml</i> file for the database image, but are also hard-coded into the <i>Dockerfile</i> through an environment variable <b>VCAP_SERVICES</b> in order to mimic how a CloudFoundry deployment will pass in database credentials.

You can execute

> docker-compose up -d

To run the containers as detached, i.e. in the background.

Doing this too often can create dangling images in your Docker cache that need to be cleaned up every time you make a change to the code in addition to other garbage that can accumulate in the cache. The script <i>/scripts/build-container.sh</i> will clean up any artifacts leftover during docker builds and keep your system nice and tidy. Instead of using <i>docker-compose up</i>, invoke from the project root directory,

> ./scripts/build-container.sh

At the base, this script uses <i>docker-compose up</i> but will also perform some basic house cleaning so your system doesn't overload. If you ever receive an error that one of your 'docker repositories is unsigned', this is probably because your cache is overloaded. You will need to prune some the cache and remove some of the dangling docker images before the application will build properly. See the Stack Overflow link in the Appendix for more information on this error.

3. Remove the containers with the following command,

> docker-compose stop<br>
> docker-compose down

Note: the <i>build-container.sh</i> script will automatically prune running containers before building and orchestrating new images. 

## CloudFoundry Environment

TODO: Update to include S3 Service Creation and Other Environment Variable Configurations

This section gives a brief overview on how to setup the environment for this application on the cloud.gov implementation of CloudFoundry. The BASH script in <i>/scripts/setup/setup-cloud-env.sh</i> will take care of all of the steps given below, provided you are logged into the the <i>cf cli</i> and have targetted the correct organization and space. For documentation's sake, the contents of this script are described:

1. Stage the app without starting it

> cf push --no-start

2. Create cloud-gov identity provider service and service key and then bind it to app (replace BASE_URL with web app URL),

> cf create-service cloud-gov-identity-provider oauth-client sin-oauth <br>
> cf create-service-key sin-oauth sin-key -c '{"redirect_uri": ["BASE_URL/auth","BASE_URL/logout"]}'<br>
> cf bind-service sinwebapp sin-oauth -c '{"redirect_uri": ["BASE_URL/auth","BASE_URL/logout"]}'<br>

The first line is of the form <i>'cf create-service <b>SERVICE_PLAN</b> <b>SERVICE_INSTANCE</b> <b>APP_INSTANCE</b>'</i>, where <b>SERVICE_PLAN</b> is the type of service being implemented, <b>SERVICE_INSTANCE</b> is the name of the particular service created and the <b>APP_INSTANCE</b> is the application space in which the service is made available.

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

### Documentation Navigation

 [^ ReadMe ^](../README.md) | [Development >>](DEVELOPMENT.md)