# <b>Still in Progress!!!</b>

Sample app that uses cloud.gov login OAuth2 endpoints and the pre-configured python library <i>cg-django-uaa</i> to authenticate user.

Note the <i>manifest.yml</i> for CloudFoundry names this app <u><b>sinwebapp</b></u><br>
## Local 

1. Create a local.env file in project's root directory and verify the following variable is set,
> ENVIRONMENT=local

This will be loaded into the <i>settings.py</i> configuration file and allow certain settings to be parsed for their respective environments, <i>local</i> or <i>cloud</i>. Note in the <i>manifest.yml</i> for CloudFoundry, an environment variable is set,

> env: ENVIRONMENT: cloud

The UAA_CLIENT_ID and UAA_CLIENT_SECRET do not matter for local deployments are only there to maintain minimal differences in the codebase for cloud and local deployments. 

2. From project's root directory, run 
>docker-compose up  
     
## CloudFoundry

1. Stage the app without starting it

> cf push --no-start

2. Create cloud-gov identity provider service and service key and then bind it to app (replace BASE_URL with web app URL),

> cf create-service cloud-gov-identity-provider oauth-client sin-oauth
> cf create-service-key sin-oauth sin-key -c '{"redirect_uri": ["BASE_URL/auth","BASE_URL/logout"]}'
> cf bind-service sinwebapp sin-oauth 

The first line is of the form 'cf create-service SERVICE_PLAN SERVICE_INSTANCE APP_INSTANCE', where SERVICE_PLAN is the type of service being implemented, SERVICE_INSTANCE is the name of the particular service created and the APP_INSTANCE is the application space is which the service in made available.

The second line generates a key so that the application instance can leverage this service. The third line binds the application instance to the service instance.

3. Retrieve client ID and client secret from service key,

> cf service-key sin-oauth sin-key

4. Django reads the client ID and client secret from Environment Variables. In the local setup, these are contained in the <i>local.env</i>. To set them on CloudFoundry, execute these commands,

> cf set-env sinwebapp UAA_CLIENT_ID "client id goes here"
> cf set-env sinwebapp UAA_CLIENT_SECRET "client secret goes here"

5. Create a PostgresSql service,

> cf create-service aws-rds medium-psql sin-sql 

Again, this uses the form 'cf create-service SERVICE_PLAN SERVICE_INSTANCE APP_INSTANCE' just like in step 2. No need to bind the <i>sin-sql</i> service to app, since it is included in the manifest. Note: the cloud-gov-identity-provider cannot be specified in the manifest since the application must first be configured with the client ID and client secret that is provided in the service key. 

6. Restage and start the app

> cf restage
> cf start

## TODO
- [x] reset service-key redirect uri on cloud.gov
- [x] determine how to protect certain endpoints from unauthenticated individuals
- [ ] create users with roles in database
- [ ] bind roles to html on redirect page after successful login 

## Useful Links
- [Cloud.gov Identity Provider](https://cloud.gov/docs/services/cloud-gov-identity-provider/) <br/>
- [Leveraging Cloud.gov Authentication](https://cloud.gov/docs/management/leveraging-authentication/) <br/>
- [CloudFoundry: Service Keys](https://docs.cloudfoundry.org/devguide/services/service-keys.html) <br/>
- [Python Library cg-django-uaa Documentation](https://cg-django-uaa.readthedocs.io/en/latest/quickstart.html)<br/>