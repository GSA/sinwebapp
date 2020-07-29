### Documentation Navigation
[<< Setup](SETUP.md) | [^ ReadMe ^](../README.md) | [Appendix >>](APPENDIX.md)

# Development

## Frontend

### Environment

In the <i>/frontend/environments/</i> directory, there is a TypeScript file that controls the Angular Service HTTP routing. When the variable <b>production</b> is set to true, Angular services will direct their HTTP calls to the backend on the cloud. When <b>production</b> is set to false, Angulars services will direct their HTTP calls to the localhost backend. Be sure to set this variable to the proper value during development and when pushing to production! Note: If you use the <i>cf-push</i>, <i>build-container</i> and <i>init-app</i> scripts, this step will automatically be taken care of for you! I.e. these scripts configure the frontend environment before building the application.

### Context

The <b>production</b> environment variable for the Angular application affects the <i>ContextService</i>. The <i>ContextService</i> is injected into other service instances to provide application-wide configuration, such as URLs to the backend API and other application properties that change based on the type of the deployment: <b>local</b> or <b>production</b>. 

## Building and Pushing

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


## Work Flows

The artifacts from the Angular build are outputted into the <i>/sinwebapp/static/</i> directory, where the Django web framework serves them up through <b>gunicorn</b>. The HTML templates in the Django backend are configured to load in these artifacts; since the Angular app enters through these Django templates, there is no <i>index.html</i> in the <i>/frontend/</i> folder. In other words, each Angular app launched from a different Django template is an entirely distinct instance of a separate Angular application.

## Database Configuratoin

The file <i>/sinwebapp/authentication/db_init.py</i> creates Groups, Permissions and Users within three separate functions, using Django's built-in class models. These functions are added to the Migration queue within <i>/sinwebapp/authentication/migrations/</i>. The initialization script that starts up both container and cloud instances of the application applies these migrations to the host database. 

## Routes & Endpoints

Listed below are the current routes used by each component of the application, the Angular frontend and the Django backend,

Django Static HTML Endpoint
- <i>/</i>
- <i>/logout</i>
- <i>/success</i>

Application API Endpoints
- <i>/api/user</i>

Third Party Endpoints
- <i>/auth/login</i>
- <i>/auth/callback</i>
- <i>/fake/oauth/authorize</i>
- <i>/fake/oauth/token</i>

Frontend Routes
- <i>404</i>: ?

## Superuser

The superuser of the database is controlled by environment variabless, DJANGO_SUPERUSER_*. These variables are loaded into it the initialization script and passed into Django while it is starting up. The local environment variables are set in the <i>local.env</i> file, while the cloud environment variables need to be set with the <i>cf cli</i>