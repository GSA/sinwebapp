# <b>SIN Web App: A Work In Progress</b>

This is a sample app that uses a <b>cloud.gov</b> OAuth2 client and a pre-configured python library specifically for that client, <i>cg-django-uaa</i>, to authenticate users.

Note the <i>manifest.yml</i> for CloudFoundry names this app <b>sinwebapp</b>, so when it is pushed to the cloud, it will live at [https://sinwebapp.app.cloud.gov](https://sinwebapp.app.cloud.gov). Edit the application name accordingly, if you need another domain route.

## Local 

1. The <i>docker-compose.yml</i> sets up the local application automatically. It reads in the <i>local.env</i> file and sets the environment for the application. Open the <i>local.env</i> file in project's root directory and verify the following variable is set,

> ENVIRONMENT=container

This will be loaded into the <i>settings.py</i> configuration file and allow certain settings to be parsed for their respective environments, <i>container</i> or <i>cloud</i>. Note in the <i>manifest.yml</i> for CloudFoundry, an environment variable is set,

> env: ENVIRONMENT: cloud

You will also find two other environment variables in the <i>local.env</i> file, <b>UAA_CLIENT_ID</b> and <b>UAA_CLIENT_SECRET</b>. The <b>UAA_CLIENT_ID</b> and <b>UAA_CLIENT_SECRET</b> do not matter for local docker deployments; they are only there to maintain minimal differences in the codebase for cloud and local docker deployments. In other words, they make life easier. 

2. From project's root directory, run 
>docker-compose up  
    
This will build the <b><b>sinwebapp</b></b> locally from the <i>Dockerfile</i> and orchestrate it with <b>postgres</b> image. The database credentials are set up in the <i>docker-compose.yml</i> file for the database image, but are also hard-coded into the <i>Dockerfile</i> through an environment variable <b>VCAP_SERVICES</b> in order to mimic how a CloudFoundry deployment will pass in database credentials.

## CloudFoundry

1. Stage the app without starting it

> cf push --no-start

2. Create cloud-gov identity provider service and service key and then bind it to app (replace BASE_URL with web app URL),

> cf create-service cloud-gov-identity-provider oauth-client sin-oauth <br>
> cf create-service-key sin-oauth sin-key -c '{"redirect_uri": ["BASE_URL/auth","BASE_URL/logout"]}'<br>
> cf bind-service sinwebapp sin-oauth <br>

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

6. Restage and start the app

> cf restage
> cf start

## Frontend

Currently, there is no build pipeline that will automatically compile and deploy the Angular frontend to the cloud. For the time being, when deploying the application to the cloud, you will need to manually build the frontend with the <i>build-frontend.sh</i> BASH script contained in the <i>/scripts/</i> folder before pushing. The Angular build is configured to output its artifacts into the <i>/sinwebapp/static/frontend/</i> directory, which is statically served through the Django framework. 

Once the frontend is build, you can push the application to CloudFoundry.

## TODO
- [x] reset service-key redirect uri on cloud.gov
- [x] determine how to protect certain endpoints from unauthenticated individuals
- [x] create users with roles in database
- [x] integrate angular frontend application with django backend framework
- [ ] bind roles to html on redirect page after successful login 
- [ ] create pipeline to build frontend and deploy to cloud

## Bugs 
### Local deployments
The <i>cg-django-uaa</i> comes with a mock login page for local deployments. By specifing the attributes <b>UAA_TOKEN_URL</b> and <b>UAA_AUTH_URL</b> to equal 'fake:' it will automatically use a mock login. The current application already detects local vs. cloud deployments through the environment variable <b>ENVIRONMENT</b> and sets these attributes accordingly. However, for local deployments, I have had issues getting the mock login to work properly.<br>

## Useful Links
- [Cloud.gov Identity Provider](https://cloud.gov/docs/services/cloud-gov-identity-provider/) <br/>
- [Leveraging Cloud.gov Authentication](https://cloud.gov/docs/management/leveraging-authentication/) <br/>
- [CloudFoundry: Service Keys](https://docs.cloudfoundry.org/devguide/services/service-keys.html) <br/>
- [Python Library cg-django-uaa Documentation](https://cg-django-uaa.readthedocs.io/en/latest/quickstart.html)<br/>
- [Django: Data Migrations](https://docs.djangoproject.com/en/3.0/topics/migrations/#data-migrations)
- [Django: Authentication Documentation](https://docs.djangoproject.com/en/3.0/topics/auth/default/)<br>
- [Django: Groups Class documentation](https://docs.djangoproject.com/en/3.0/ref/contrib/auth/#django.contrib.auth.models.Group)<br>
- [Django: Permissions Class documentation](https://docs.djangoproject.com/en/3.0/topics/auth/default/#permissions-and-authorization)<br>
- [Django: User Class documentation](https://docs.djangoproject.com/en/3.0/topics/auth/default/#user-objects)<br>

## Relevant Stack Discussions
- [Django, Add Auth Groups Programmatically](https://stackoverflow.com/questions/25024795/django-1-7-where-to-put-the-code-to-add-groups-programmatically/25803284#25803284)<br>
- [Creating JSON HttpResponse In Django](https://stackoverflow.com/questions/2428092/creating-a-json-response-using-django-and-python)