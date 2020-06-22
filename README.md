# <b>SIN Web App: A Work In Progress</b>

This is a sample app that uses a <u>cloud.gov</u> OAuth2 client and a pre-configured python library specifically for that client, <i>cg-django-uaa</i>, to authenticate users.

Note the <i>manifest.yml</i> for CloudFoundry names this app <u><b>sinwebapp</b></u>, so when it is pushed to the cloud, it will live at [https://sinwebapp.app.cloud.gov](https://sinwebapp.app.cloud.gov). Edit the application name accordingly, if you need another domain route.

## Local 

1. Open the <i>local.env</i> file in project's root directory and verify the following variable is set,
> ENVIRONMENT=local

This will be loaded into the <i>settings.py</i> configuration file and allow certain settings to be parsed for their respective environments, <i>local</i> or <i>cloud</i>. Note in the <i>manifest.yml</i> for CloudFoundry, an environment variable is set,

> env: ENVIRONMENT: cloud

You will also find two other environment variables in the <i>local.env</i> file, <b>UAA_CLIENT_ID</b> and <b>UAA_CLIENT_SECRET</b>. The <b>UAA_CLIENT_ID</b> and <b>UAA_CLIENT_SECRET</b> do not matter for local deployments; they are only there to maintain minimal differences in the codebase for cloud and local deployments. In other words, they make life easier. 

2. From project's root directory, run 
>docker-compose up  
    
This will build the <u><b>sinwebapp</u></b> locally from the <i>Dockerfile</i> and orchestrate it with <u>postgres</u> image. The database credentials are set up in the <i>docker-compose.yml</i> file for the database image, but are also hard-coded into the <i>Dockerfile</i> through an environment variable <b>VCAP_SERVICES</b> in order to mimic how a CloudFoundry deployment will pass in database credentials.

## CloudFoundry

1. Stage the app without starting it

> cf push --no-start

2. Create cloud-gov identity provider service and service key and then bind it to app (replace BASE_URL with web app URL),

> cf create-service cloud-gov-identity-provider oauth-client sin-oauth <br>
> cf create-service-key sin-oauth sin-key -c '{"redirect_uri": ["BASE_URL/auth","BASE_URL/logout"]}'<br>
> cf bind-service sinwebapp sin-oauth <br>

The first line is of the form <i>'cf create-service <u>SERVICE_PLAN</u> <u>SERVICE_INSTANCE</u> <u>APP_INSTANCE</u>'</i>, where <u>SERVICE_PLAN</u> is the type of service being implemented, <u>SERVICE_INSTANCE</u> is the name of the particular service created and the <u>APP_INSTANCE</u> is the application space is which the service in made available.

The second line generates a key so that the application instance can leverage this service. The third line binds the application instance to the service instance.

3. Retrieve client ID and client secret from service key,

> cf service-key sin-oauth sin-key

4. Django reads the client ID and client secret from Environment Variables. In the local setup, these are contained in the <i>local.env</i>. To set them on CloudFoundry, execute these commands,

> cf set-env sinwebapp UAA_CLIENT_ID "client id goes here"<br>
> cf set-env sinwebapp UAA_CLIENT_SECRET "client secret goes here"

5. Create a PostgresSql service,

> cf create-service aws-rds medium-psql sin-sql 

Again, this command uses the form <i>'cf create-service <u>SERVICE_PLAN</u> <u>SERVICE_INSTANCE</u> <u>APP_INSTANCE</u>'</i> just like in step 2, since we are creating a service in an application space. No need to bind the <i>sin-sql</i> service to app, since it is included in the manifest. Note: the cloud-gov-identity-provider cannot be specified in the manifest since the application must first be configured with the client ID and client secret that is provided in the service key. 

6. Restage and start the app

> cf restage
> cf start

## TODO
- [x] reset service-key redirect uri on cloud.gov
- [x] determine how to protect certain endpoints from unauthenticated individuals
- [ ] create users with roles in database
- [ ] bind roles to html on redirect page after successful login 

## Thoughts

Roles can be implemented with the Groups object type provided by the Django authentication backend: https://docs.djangoproject.com/en/3.0/topics/auth/default/

## Useful Links
- [Cloud.gov Identity Provider](https://cloud.gov/docs/services/cloud-gov-identity-provider/) <br/>
- [Leveraging Cloud.gov Authentication](https://cloud.gov/docs/management/leveraging-authentication/) <br/>
- [CloudFoundry: Service Keys](https://docs.cloudfoundry.org/devguide/services/service-keys.html) <br/>
- [Python Library cg-django-uaa Documentation](https://cg-django-uaa.readthedocs.io/en/latest/quickstart.html)<br/>