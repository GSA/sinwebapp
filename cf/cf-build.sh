# SCRIPT ARGUMENTS 
# $1: CloudFoundry Username
# $2: CloudFoundry Password
# $3: rebuild flag

# Description: This script will login to the CloudFoundry environment and initialize
# service instances, bind them to the app and set environment variables. Passing in
# the rebuild flag as the third argument will cause this script to wipe the existing
# environment and start fresh. 

ROUTE="https://sinwebapp.app.cloud.gov"
LOGIN_REDIRECT="auth"
LOGOUT_REDIRECT="logout"
OAUTH_SERVICE_ARG="{\"redirect_uri\": [\"$ROUTE/$LOGIN_REDIRECT\",\"$ROUTE/$LOGOUT_REDIRECT\"]}"

cf login -a api.fr.cloud.gov -u $1 -p $2 -o sandbox-gsa

if [ $3 == "rebuild" ]
then
    #TODO: delete service keys, unbind services
fi

cf create-service aws-rds medium-psql sin-sql
# TODO: wait for sql service to be created. Takes a bit.
cf create-service cloud-gov-identity-provider oauth-client sin-oauth
cf create-service-key sin-oauth sin-key -c $OAUTH_SERVICE_ARG

cf push --no-start

cf bind-service sinwebapp sin-oauth -c $OAUTH_SERVICE_ARG

SERVICE_KEY ="$(cf service-key sin-oauth sin-key)"
CLIENT_ID = echo $SERVICE_KEY | python -c \
    'import json,sys;print json.load(sys.stdin)["client_id"]'
CLIENT_SECRET = echo $SERVICE_KEY | python -c \
    'import json,sys;print json.load(sys.stdin)["client_secret"]'
    
cf set-env sinwebapp UAA_CLIENT_ID $CLIENT_ID
cf set-env sinwebapp UAA_CLIENT_SECRET $CLIENT_SECRET

cf restage

