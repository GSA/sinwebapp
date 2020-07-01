# SCRIPT ARGUMENTS 
# $1: CloudFoundry Username
# $2: CloudFoundry Password
# $3: rebuild flag

# Description: This script will login to the CloudFoundry environment, initialize
# service instances, bind them to the app and set environment variables. Passing in
# the 'rebuild' flag as the third argument will cause this script to wipe the existing
# environment and start fresh. 

ROUTE="https://sinwebapp.app.cloud.gov"
LOGIN_REDIRECT="auth"
LOGOUT_REDIRECT="logout"
OAUTH_SERVICE_ARG="{\"redirect_uri\": [\"$ROUTE/$LOGIN_REDIRECT\",\"$ROUTE/$LOGOUT_REDIRECT\"]}"
CLOUD_ORG="sandbox-gsa"

echo "> Logging Into CloudFoundry..."
cf login -a api.fr.cloud.gov -u $1 -p $2 -o $CLOUD_ORG

if [ $3 == "rebuild" ]
then
    cf delete-service-key sin-oauth sin-key -f
    cf unbind-service sinwebapp sin-oauth
    cf unbind-service sinwebapp sin-sql
    cf delete-service sin-oauth -f
    cf delete-service sin-sql -f
fi

echo "> Creating SQL Service..."
cf create-service aws-rds medium-psql sin-sql
sleep 5m
# wait for sql service to be created. Takes a bit.
echo "> Creating OAuth Client Service..."
cf create-service cloud-gov-identity-provider oauth-client sin-oauth
cf create-service-key sin-oauth sin-key -c $OAUTH_SERVICE_ARG

echo "> Pushing app to cloud with no-start flag..."
cf push --no-start

echo "> Binding OAuth Client to app"
cf bind-service sinwebapp sin-oauth -c $OAUTH_SERVICE_ARG

SERVICE_KEY ="$(cf service-key sin-oauth sin-key)"
CLIENT_ID = echo $SERVICE_KEY | python -c \
    'import json,sys;print json.load(sys.stdin)["client_id"]'
CLIENT_SECRET = echo $SERVICE_KEY | python -c \
    'import json,sys;print json.load(sys.stdin)["client_secret"]'

echo "> OAuth Client Credentialss"
echo ">> Client ID: $CLIENT_ID"
echo ">> Client Secret: $CLIENT_SECRET"
echo "> Storing OAuth Client Credentials In Cloud Environment Variables..."
cf set-env sinwebapp UAA_CLIENT_ID $CLIENT_ID
cf set-env sinwebapp UAA_CLIENT_SECRET $CLIENT_SECRET

echo "> Restaging and starting app..."
cf restage

