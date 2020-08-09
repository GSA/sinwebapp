### Documentation Navigation
[<< Setup](SETUP.md) | [^ ReadMe ^](../README.md) | [API >>](API.md)

# Development

## 1. Frontend

### A. Environment

In the <i>/frontend/environments/</i> directory, there is a TypeScript file that controls the Angular Service HTTP routing. When the variable <b>production</b> is set to true, Angular services will direct their HTTP calls to the backend on the cloud. When <b>production</b> is set to false, Angulars services will direct their HTTP calls to the localhost backend. Be sure to set this variable to the proper value during development and when pushing to production! Note: If you use the <i>cf-push</i>, <i>build-container</i> and <i>init-app</i> scripts, this step will automatically be taken care of for you! I.e. these scripts configure the frontend environment before building the application.

### B. Context

The <b>production</b> environment variable for the Angular application affects the <i>ContextService</i>. The <i>ContextService</i> is injected into other service instances to provide application-wide configuration, such as URLs to the backend API and other application properties that change based on the type of the deployment: <b>local</b> or <b>production</b>. 

### C. Models

The data models for the frontend are located in <i>/frontend/src/app/models/</i>. These models must map to the backend models. See <b>Section 2A</b> for more information on the backend models. These models are used by the Services and Components within Angular to format requests and responses sent to the backend. They are the key to communication between the back- and frontend. 

### D. App Structure

The <b>Angular</b> frontend app is broken into four pieces: components, interceptors, models and services. Components are the programmatic classes attached to HTML templates that define UI behavior. Models define the structure of the data the user interacts with. Services provide model data to the Components. Interceptors grab outgoing requests to the backend and attach headers and cookies that are required for authentication and CSRF tokens. 

## 2. Backend

### A. Database Configuratoin

The file <i>/sinwebapp/authentication/db_init.py</i> creates application-specific Groups, Permissions and Users within three separate functions, using Django's built-in <i>Auth</i> class models. These functions are added to the Migration queue within <i>/sinwebapp/authentication/migrations/</i>. 

The files <i>/sinwebapp/api/models.py</i> and <i>/sinwebapp/api/db_init.py</i> create the SIN, Status, Audit and Comment tables and then initialize the tables with constant data. These migrations and initializations are added to the Migration queue within <i>/sinwebapp/api/migrations/</i>. The models defined here must map to the models defined in the frontend in order for the backend and frontend to be able to communicate. If any changes are made to any of the underlying data model for SINs, then both the back- and frontend must be changed in parallel to reflect this change. See <b>Section 1C</b> for more information on the frontend data models.

In addition, if the data model is changed, the migrations stored within each app of the backend must be remade. Delete <i>only</i> the <i>0001_initial.py</i> migration from each app's migrations if the database model needs to be updated. The other migrations in these folders are custom migrations that cannot be created by the <b>django-admin</b>. Once the initial migrations are deleted and the backend models updated, the following command issued from the <i>/sinwebapp/</i> directory will create new migrations,

> python manage.py makemigrations

### B. Superuser

The superuser of the database is controlled by environment variabless, DJANGO_SUPERUSER_*. These variables are loaded into it the initialization script and passed into Django while it is starting up. The local environment variables are set in the <i>/env/local.sh</i> script, the docker environment variables are set in the <i>/env/container.env</i> file, while the cloud environment variables can set manually with the <i>cf cli</i> or loaded in through the <i>/env/cloud.sh</i> script when invoking the <i>/scripts/setup-cloud-env.sh</i> script.

### C. App Structure

The <b>django</b> backend application is broken into several component apps: <i>api</i>, <i>authentication</i> and <i>core</i>. The <i>core</i> app sets up the basic framework necessary for a django app to function. While the application utilizes the external library <i>cg-django-uaa</i> for most of its authentication and authorization, the <i>authentication</i> app is responsible for some application specific customization. The <i>api</i> app provides endpoints that exposeS the database to user queries.  

## 3.  Building and Pushing

### Automatic : CircleCi Pipeline

A CircleCi pipeline is hooked into the <i>master</i> branch on GitHub. Anytime new code is pushed to the <i>master</i>, the pipeline will trigger. The pipeline will automatically build and deploy the application to the cloud. In order to deploy the application to the cloud, the pipeline needs credentials for the cloud.gov environment. You can create a cloud-environment-specific service account for CircleCi with the <i>cf cli</i> with the following command,

> cf create-service cloud-gov-service-account sin-/CLOUD_SPACE_GOES_HERE/-deployer circleci-account

You can then create a service-key for this service,

> cf create-service-key circleci-account circleci-key

And then retrieve the credentials for this account with the newly created key,

> cf service-key circleci-account circle-key

You will then need to store these credentials on the CircleCi pipeline environment in variables named <b>CF_/CLOUD_SPACE_GOES_HERE/_USERNAME</b> and <b>CF_/CLOUD_SPACE_GOES_HERE/_PASSWORD</b> respectively. 

<b>Note: the current application has already been configured for CircleCi</b>

In the future, the pipeline will include other branches and also test the application before deployment.

### Manual : <i>cf cli</i>

When deploying the application to the cloud yourself, you will need to manually build the frontend with the <i>build-frontend.sh</i> BASH script contained in the <i>/scripts/</i> folder before pushing. The Angular build is configured to output its artifacts into the <i>/sinwebapp/static/frontend/</i> directory, which is statically served through the Django framework. 

Once the frontend is built, you can push the application to CloudFoundry.

In other words, if you add code to the frontend, be sure to run this command from the project's root directory:

> bash ./scripts/build-frontend.sh

Before pushing to the cloud,

> cf push

These commands are so frequent they have been further condensed into another BASH script. The BASH script, <i>/scripts/cf-push.sh</i>, takes care of installing and building the frontend for you, as long as you already logged into the <i>cf cli</i>, if you provide it the proper argument

> bash ./scripts/cf-push.sh build

This script has other functionality, such as cleaning the artifacts from the build after pushing them to the cloud or trailing the cloud logs. For example, the command,

> bash ./scripts/cf-push.sh build dispose trail

will build the frontnend application, push it to the cloud, remove the generated artifacts from the project and trail the logs outputted by CloudFoundry. The order of arguments does not matter, i.e. the following command will accomplish the same task,

> bash ./scripts/cf-push.sh dispose trail build

## 4. Miscellanous

### A. Scripts

There are a variety of scripts within the <i>/scripts/</i> that will perform many of the tasks that pop up during the course of development. For example, you may need to tear down the existing SQL service on <i>cloud.gov</i> and reinitialize it with a fresh database. The script <i>reset-sql-service.sh</i> will do just that! 

More documentation can be found within the comments of the scripts themselves. TODO: implement --help argument for each script that prints out it function and usage. 

All of the scripts are BASH scripts and so must be executed with a UNIX/Linux environment. <b>Git for Windows</b> will work if you happen to be on a Windows machine. 

### B. Work Flows

The artifacts from the Angular build are outputted into the <i>/sinwebapp/static/</i> directory, where the Django web framework serves them up through <b>gunicorn</b>. The HTML templates in the Django backend are configured to load in these artifacts; since the Angular app enters through these Django templates, there is no <i>index.html</i> in the <i>/frontend/</i> folder. In other words, each Angular app launched from a different Django template is an entirely distinct instance of a separate Angular application.
