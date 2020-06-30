# TODO: login and target org/space

ROUTE="https://sinwebapp.app.cloud.gov"
LOGIN_REDIRECT="auth"
LOGOUT_REDIRECT="logout"
OAUTH_SERVICE_ARG="{\"redirect_uri\": [\"$ROUTE/$LOGIN_REDIRECT\",\"$ROUTE/$LOGOUT_REDIRECT\"]}"

cf create-service aws-rds medium-psql sin-sql
# TODO: wait for sql service to be created. Takes a bit.

cf create-service cloud-gov-identity-provider oauth-client sin-oauth
cf create-service-key sin-oauth sin-key -c $OAUTH_SERVICE_ARG

cf push --no-start

cf bind-service sinwebapp sin-oauth -c $OAUTH_SERVICE_ARG

cf service-key sin-oauth sin-key
# outputs {"client_id:", "client_secret"} json
# to do: parse json, this is a python environment, maybe json python library?

cf set-env sinwebapp UAA_CLIENT_ID # insert client id from service
cf set-env sinwebapp UAA_CLIENT_SECRET # insert client secret from service

cf restage

