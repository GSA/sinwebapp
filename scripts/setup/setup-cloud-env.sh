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

### NOTE
## You should only need to use this script when you want to initially set up the 
## CloudFoundry application on cloud.gov or if you want to tear down the existing 
## application and create a fresh instance. CAREFUL: If you tear down the existing
## application, it will delete all the data stored in the database service!

### EXAMPLE USAGE (from project root directory)
    ## 1: $ ./scripts/setup/setup-cloud-env.sh sinweb.app.cloud.gov 
        # This will build a new cloud environment
    ## 2: $ ./scripts/setup/setup-cloud-env.sh sinweb.app.cloud.gov rebuild
        # This will take down the current environment on the cloud and build a new one.

# Script Constants
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='setup-cloud-env.sh'
source "$SCRIPT_DIR/../util/logging.sh"

# CloudFoundry OAuth Parameters
LOGIN_REDIRECT="auth"
LOGOUT_REDIRECT="logout"
OAUTH_SERVICE_ARG="{\"redirect_uri\": [\"https://$1/$LOGIN_REDIRECT/\",\"https://$1/$LOGOUT_REDIRECT\"]}"

cd $SCRIPT_DIR/../..
formatted_print "--> OAUTH_SERVICE_ARG: $OAUTH_SERVICE_ARG" $SCRIPT_NAME

formatted_print '--> Copying Initialization Script Into Application'
cp $SCRIPT_DIR/../init-app.sh $SCRIPT_DIR/../../sinwebapp/init-app.sh
mkdir $SCRIPT_DIR/../../sinwebapp/util/ && \
    cp $SCRIPT_DIR/../util/logging.sh $SCRIPT_DIR/../../sinwebapp/util/logging.sh


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

formatted_print '--> Creating OAuth Client Service' $SCRIPT_NAME
cf create-service cloud-gov-identity-provider oauth-client sin-oauth
#  cf create-service-key sin-oauth sin-key -c '{"redirect_uri": ["https://sinweb.app.cloud.gov/auth","https://sinweb.app.cloud.gov/logout"]}'
cf create-service-key sin-oauth sin-key -c "$OAUTH_SERVICE_ARG"

while [[ "$(cf service sin-sql)" == *"create in progress"* ]]
do  
    formatted_print '--> Waiting On SQL Service Creation' $SCRIPT_NAME
    formatted_print '--> SQL Service Status...' $SCRIPT_NAME
    cf service sin-sql
    sleep 15s
done
# wait for services to be created. Takes a bit. 
    # Probably a better way to do this. Research 
    # processes and how to watch them!

formatted_print '--> Pushing App To Cloud With \e[3m--no-start\e[0m Flag' $SCRIPT_NAME
cf push --no-start

formatted_print '--> Binding OAuth Client To App' $SCRIPT_NAME
# cf bind-service sinweb sin-oauth -c '{"redirect_uri": ["https://sinweb.app.cloud.gov/auth","https://sinweb.app.cloud.gov/logout"]}'
cf bind-service sinweb sin-oauth -c "$OAUTH_SERVICE_ARG"

SERVICE_KEY="$(cf service-key sin-oauth sin-key)"
filtered_key="${SERVICE_KEY#*\{}"
CLIENT_ID=$(echo "{$filtered_key" | python -c 'import json,sys;print(json.load(sys.stdin)["client_id"])')
CLIENT_SECRET=$(echo "{$filtered_key" | python -c 'import json,sys;print(json.load(sys.stdin)["client_secret"])')

formatted_print "--> CLIENT_ID: $CLIENT_ID" $SCRIPT_NAME
formatted_print "--> CLIENT_SECRET: $CLIENT_SECRET" $SCRIPT_NAME

cf set-env sinweb UAA_CLIENT_ID $CLIENT_ID
cf set-env sinweb UAA_CLIENT_SECRET $CLIENT_SECRET
# Change these fields to change the superuser!
cf set-env sinweb DJANGO_SUPERUSER_USERNAME grantmoore
cf set-env sinweb DJANGO_SUPERUSER_EMAIL grant.moore@gsa.gov

formatted_print '--> Starting App' $SCRIPT_NAME
cf start sinweb

