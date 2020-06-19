<b>Still in Progress!!!</b>

Sample app that uses cloud.gov login OAuth2 endpoints and the pre-configured python library <i>cg-django-uaa</i> to authenticate user.

Steps to get up and running:<br>
1. Open local.env and edit UAA_CLIENT_ID and UAA_CLIENT_SECRET to the service credentials provided by cloud.gov identity provider
    - Message me for the ID and SECRET!
2. From project's root directory, run 
>docker-compose up  
     
# TODO
[ ] reset service-key redirect uri on cloud.gov
[ ] determine how to protect certain endpoints from unauthenticated individuals
[ ] create users with roles in database
[ ] bind roles to html on redirect page after successful login 