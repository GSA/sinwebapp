<b>Still in Progress!!!</b>

Sample app that uses cloud.gov login OAuth2 endpoints and the pre-configured python library <i>cg-django-uaa</i> to authenticate user.

Steps to get up and running:<br>
## Local 

1. Open local.env and edit UAA_CLIENT_ID and UAA_CLIENT_SECRET to the service credentials provided by cloud.gov identity provider
    - Message me for the ID and SECRET!
2. From project's root directory, run 
>docker-compose up  
     
# CloudFoundry

1. Stage the app without starting it

> cf push --no-start

2. Create cloud-gov identity provider service and bind it to app

> cf create-service cloud-gov-identity-provider oauth-client sinwebapp
> cf bind-service sinwebapp sin-oauth -c '{"redirect_uri": ["https://sinwebapp.app.cloud.gov/auth", "https://sinwebapp.app.cloud.gov/logout"]}'

(not totally certain the above redirect_uris are correct yet)

3. Create a PostgresSql service,

> cf create-service aws-rds medium-psql sin-sql 

No need to bind <i>sin-sql</i> service to app, since it is included in the manifest.

4. Restage and start the app

> cf restage
> cf start

# TODO
- [ ] reset service-key redirect uri on cloud.gov
- [ ] determine how to protect certain endpoints from unauthenticated individuals
- [ ] create users with roles in database
- [ ] bind roles to html on redirect page after successful login 