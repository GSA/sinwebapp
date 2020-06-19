# <b>Still in Progress!!!</b>

Sample app that uses cloud.gov login OAuth2 endpoints and the pre-configured python library <i>cg-django-uaa</i> to authenticate user.

Steps to get up and running:<br>
## Local 

1. Open local.env and edit UAA_CLIENT_ID and UAA_CLIENT_SECRET to the service credentials provided by cloud.gov identity provider
2. From project's root directory, run 
>docker-compose up  
     
## CloudFoundry

1. Stage the app without starting it

> cf push --no-start

2. Create cloud-gov identity provider service and service key and then bind it to app (replace BASE_URL with web app URL)

> cf create-service cloud-gov-identity-provider sin-oauth sinwebapp
> cf create-service-key sinwebapp sin-key -c '{"redirect_uri": ["BASE_URL/auth","BASE_URL/logout"]}'
> cf bind-service sinwebapp sin-oauth 

3. Retrieve client ID and client secret from service key,

> cf service-key sinwebapp sin-key

4. Django reads the client ID and client secret from Environment Variables. In the local setup, these are contained in the <i>local.env</i>. To set them on CloudFoundry, execute these commands,

> cf set-env sinwebapp UAA_CLIENT_ID "client id goes here"
> cf set-env sinwebapp UAA_CLIENT_SECRET "client secret goes here"

5. Create a PostgresSql service,

> cf create-service aws-rds medium-psql sin-sql 

No need to bind <i>sin-sql</i> service to app, since it is included in the manifest.

6. Restage and start the app

> cf restage
> cf start

## TODO
- [x] reset service-key redirect uri on cloud.gov
- [x] determine how to protect certain endpoints from unauthenticated individuals
- [ ] create users with roles in database
- [ ] bind roles to html on redirect page after successful login 

## Useful Links
[Cloud.gov Identity Provider](https://cloud.gov/docs/services/cloud-gov-identity-provider/)
[Leveraging Cloud.gov Authentication](https://cloud.gov/docs/management/leveraging-authentication/)
[CloudFoundry: Service Keys](https://docs.cloudfoundry.org/devguide/services/service-keys.html)
[Python Library cg-django-uaa Documentation](https://cg-django-uaa.readthedocs.io/en/latest/quickstart.html)