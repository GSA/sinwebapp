## SCRIPT ARGUMENTS 
## $1: CloudFoundry Username
## $2: CloudFoundry Password
## $3: Cloud Space
## $4: Cloud Route
## $5: rebuild flag

## DESCRIPTION
# This script will login to the CloudFoundry environment, initialize service instances, 
# bind them to the app and set environment variables. Passing in the 'rebuild' flag as 
# the third argument will cause this script to wipe the existing environment and start 
# a fresh environment. 

## EXAMPLE USAGE
    # 1: $ ./build-cloud.sh fakeuser fakepassword dev https://sinwebapp.app.cloud.gov 
        # This will build a new cloud environment
    # 2: $ ./build-cloud.sh fakeuser fakepassword dev http:s//sinwebapp.app.cloud.gov rebuild
        # This will take down the current environment on the cloud and build a new one.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
LOGIN_REDIRECT="auth"
LOGOUT_REDIRECT="logout"
OAUTH_SERVICE_ARG="{\"redirect_uri\": [\"$4/$LOGIN_REDIRECT\",\"$4/$LOGOUT_REDIRECT\"]}"
CLOUD_ORG="fas-calc"
SCRIPT_NAME='build-cloud.sh'
source "$SCRIPT_DIR/helpers/utilities.sh"

cd $SCRIPT_DIR/..
formatted_print 'Logging Into CloudFoundry' $SCRIPT_NAME
cf login -a api.fr.cloud.gov -u $1 -p $2 -o $CLOUD_ORG -s $3

if [ $5 == "rebuild" ]
then
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

