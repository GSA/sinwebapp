### ARGUMENTS 
## REQUIRED
# $1: Cloud Org - The organization the applications lives at on CloudFoundry
# $2: Cloud Space - The space the applications lives at on CloundFoundry
# $3: Cloud Route - The URL the application lives at on CloudFoundry
## OPTIONAL
## $4: rebuild flag - deletes and recreates old instances of CloudFoundry services

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

# CloudFoundry OAuth Parameters
LOGIN_REDIRECT="auth"
LOGOUT_REDIRECT="logout"
OAUTH_SERVICE_ARG="{\"redirect_uri\": [\"$3/$LOGIN_REDIRECT\",\"$3/$LOGOUT_REDIRECT\"]}"

# Load in 'formatted_print'
source "$SCRIPT_DIR/../helpers/utilities.sh"

cd $SCRIPT_DIR/../..
formatted_print 'Targetting CloudFoundry Organization Space...' $SCRIPT_NAME
cf target -o $1 -s $2

if [ "$4" == "rebuild" ]
then
    formatted_print 'Clearing Existing Services...' $SCRIPT_NAME
    cf delete-service-key sin-oauth sin-key -f
    cf unbind-service sinwebapp sin-oauth
    cf unbind-service sinwebapp sin-sql
    cf delete-service sin-oauth -f
    cf delete-service sin-sql -f
fi

formatted_print 'Creating SQL Service...' $SCRIPT_NAME
cf create-service aws-rds medium-psql sin-sql
sleep 5m
# wait for sql service to be created. Takes a bit.

formatted_print 'Creating OAuth Client Service...' $SCRIPT_NAME
cf create-service cloud-gov-identity-provider oauth-client sin-oauth
cf create-service-key sin-oauth sin-key -c $OAUTH_SERVICE_ARG

formatted_print 'Pushing App To Cloud With No-Start Flag...' $SCRIPT_NAME
cf push --no-start

formatted_print 'Binding OAuth Client To App...' $SCRIPT_NAME
cf bind-service sinwebapp sin-oauth -c $OAUTH_SERVICE_ARG

SERVICE_KEY ="$(cf service-key sin-oauth sin-key)"
CLIENT_ID = echo $SERVICE_KEY | python -c \
    'import json,sys;print json.load(sys.stdin)["client_id"]'
CLIENT_SECRET = echo $SERVICE_KEY | python -c \
    'import json,sys;print json.load(sys.stdin)["client_secret"]'

cf set-env sinwebapp UAA_CLIENT_ID $CLIENT_ID
cf set-env sinwebapp UAA_CLIENT_SECRET $CLIENT_SECRET

# TODO: set DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_PASSWORD, 
    # DJANGO_SUPERUSER_EMAIL

formatted_print 'Restaging And Starting App...' $SCRIPT_NAME
cf restage

