### ARGUMENTS 
## REQUIRED
# $1: Cloud Route - The URL the application lives at on CloudFoundry
## OPTIONAL
## $2: rebuild flag - deletes and recreates old instances of CloudFoundry services

### DESCRIPTION
## This script will target the CloudFoundry environment, initialize service instances, 
## bind them to the app and set environment variables. Passing in the 'rebuild' flag as 
## the third argument will cause this script to wipe the existing environment and start 
## a fresh environment. 

### EXAMPLE USAGE (from project root directory)
    ## 1: $ ./scripts/setup/setup-cloud-env.sh fakeuser fakepassword fsa-calc dev https://sinwebapp.app.cloud.gov 
        # This will build a new cloud environment
    ## 2: $ ./scripts/setup/setup-cloud-env.sh fakeuser fakepassword fsa-calc dev http:s//sinwebapp.app.cloud.gov rebuild
        # This will take down the current environment on the cloud and build a new one.

# Script Constants
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='setup-cloud-env.sh'
source "$SCRIPT_DIR/../helpers/utilities.sh"

# CloudFoundry OAuth Parameters
LOGIN_REDIRECT="auth"
LOGOUT_REDIRECT="logout"
OAUTH_SERVICE_ARG="{\"redirect_uri\": [\"$1/$LOGIN_REDIRECT\",\"$1/$LOGOUT_REDIRECT\"]}"

cd $SCRIPT_DIR/../..
formatted print "--> OAUTH_SERVICE_ARG: $OAUTH_SERVICE_ARG" $SCRIPT_NAME

formatted_print '--> Copying Initialization Script Into Application'
cp $SCRIPT_DIR/../init-app.sh $SCRIPT_DIR/../../sinwebapp/init-app.sh

if [ "$2" == "rebuild" ]
then
    formatted_print '--> Clearing Existing Services' $SCRIPT_NAME
    cf delete-service-key sin-oauth sin-key -f
    cf unbind-service sinweb sin-oauth
    cf unbind-service sinweb sin-sql
    cf delete-service sin-oauth -f
    cf delete-service sin-sql -f
fi

formatted_print '--> Creating SQL Service' $SCRIPT_NAME
cf create-service aws-rds medium-psql sin-sql
formatted_print '--> Waiting For Service Creation'
# sleep 5m
# wait for sql service to be created. Takes a bit. 
    # Probably a better way to do this. Research 
    # processes and how to watch them!

formatted_print '--> Creating OAuth Client Service' $SCRIPT_NAME
cf create-service cloud-gov-identity-provider oauth-client sin-oauth
#  cf create-service-key sin-oauth sin-key -c '{"redirect_uri": ["sinweb.app.cloud.gov/auth","sinweb.app.cloud.gov/logout"]}'
cf create-service-key sin-oauth sin-key -c "$OAUTH_SERVICE_ARG"

formatted_print '--> Pushing App To Cloud With No-Start Flag' $SCRIPT_NAME
cf push --no-start

formatted_print '--> Binding OAuth Client To App' $SCRIPT_NAME
# cf bind-service sinweb sin-oauth -c '{"redirect_uri": ["sinweb.app.cloud.gov/auth","sinweb.app.cloud.gov/logout"]}'
cf bind-service sinweb sin-oauth -c "$OAUTH_SERVICE_ARG"

SERVICE_KEY ="$(cf service-key sin-oauth sin-key)"
echo "SERVICE_KEY: $SERVICE_KEY"

CLIENT_ID = echo $SERVICE_KEY | python -c \
    'import json,sys;print json.load(sys.stdin)["client_id"]'
CLIENT_SECRET = echo $SERVICE_KEY | python -c \
    'import json,sys;print json.load(sys.stdin)["client_secret"]'

formatted_print "--> CLIENT_ID: $CLIENT_ID" $SCRIPT_NAME
formatted_print "--> CLIENT_SECRET: $CLIENT_SECRET" $SCRIPT_NAME

cf set-env sinweb UAA_CLIENT_ID $CLIENT_ID
cf set-env sinweb UAA_CLIENT_SECRET $CLIENT_SECRET
# Change these fields to change the superuser!
cf set-env sinweb DJANGO_SUPERUSER_USERNAME grantmoore
cf set-env sinweb DJANGO_SUPERUSER_EMAIL grant.moore@gsa.gov

formatted_print '--> Restaging App' $SCRIPT_NAME
cf restage sinweb

