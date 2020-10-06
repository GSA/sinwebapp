### ARGUMENTS 
## REQUIRED
# $1: Cloud Route - The name of the application specified in manifest.yml
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
    ## 1: $ ./scripts/setup/setup-cloud-env.sh ccda
        # This will build a new cloud environment
    ## 2: $ ./scripts/setup/setup-cloud-env.sh ccda rebuild
        # This will take down the current environment on the cloud and build a new one.

# Script Constants
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='\e[4msetup-cloud-env\e[0m'
nl=$'\n'
SCRIPT_DES="This script builds the application environment on the cloud. It will setup ${nl}\
    the identity provider service, an AWS S3 service and an AWS SQL service and then ${nl}\
    configure the application for these services via environment variables. Be sure to ${nl}\
    configure \e[3mlocal.env\e[0m variables before running this script, as these values will ${nl}\
    copied over to their corresponding cloud equivalents.${nl}${nl}
   EXAMPLE USAGE${nl}\
       bash setup-cloud-env.sh ccda rebuild${nl}${nl}\
   ARGUMENTS - REQUIRED${nl}\
${nl}       app_name - the name of the application, as specified in the \e[3mmanifest.yml\e[0m${nl}\
                    Must always be the first argument provided to the script, before ${nl}\
                    any optional arguments.${nl}${nl}
   ARGUMENTS - OPTIONAL${nl}\
${nl}       rebuild - tear down existing services on the cloud, and rebuild the cloud${nl}\
                    environment from scratch. This option will delete the database ${nl}\
                    instance and destroy any application data. Be careful using this ${nl}\
                    option."
source "$SCRIPT_DIR/../util/logging.sh"

if [ "$1" == "--help" ] || [ "$1" == "--h" ] || [ "$1" == "-help" ] || [ "$1" == "-h" ]
then
    help_print "$SCRIPT_DES" $SCRIPT_NAME
else
    # cloud.gov Identity Service OAuth Parameters
    LOGIN_REDIRECT="auth"
    LOGOUT_REDIRECT="logout"
    OAUTH_SERVICE_ARG="{\"redirect_uri\": [\"https://$1.app.cloud.gov/$LOGIN_REDIRECT\",\"https://$1.app.cloud.gov/$LOGOUT_REDIRECT\"]}"

    cd $SCRIPT_DIR/../..
    formatted_print "--> OAUTH_SERVICE_ARG: $OAUTH_SERVICE_ARG" $SCRIPT_NAME

    formatted_print '--> Invoking \e[3minit-scripts.sh\e[0m Script' $SCRIPT_NAME
    bash $SCRIPT_DIR/../init-scripts.sh

    formatted_print '--> Invoking \e[3minit-env.sh\e[0m Script' $SCRIPT_NAME
    source $SCRIPT_DIR/../init-env.sh

    if [ "$2" == "rebuild" ]
    then
        formatted_print '--> Clearing Existing Services' $SCRIPT_NAME
        cf delete-service-key "$1-oauth" "$1-key" -f
        cf unbind-service $1 "$1-oauth"
        cf unbind-service $1 "$1-s3"
        cf unbind-service $1 "$1-sql"
        cf delete-service "$1-oauth" -f
        cf delete-service "$1-sql" -f
        cf delete-service "$1-s3" -f
    fi

    formatted_print '--> Creating SQL Service' $SCRIPT_NAME
    cf create-service aws-rds medium-psql "$1-sql"

    formatted_print '--> Creating S3 Service' $SCRIPT_NAME
    cf create-service s3 basic "$1-s3"

    formatted_print '--> Creating OAuth Client Service' $SCRIPT_NAME
    cf create-service cloud-gov-identity-provider oauth-client "$1-oauth"
    #  cf create-service-key $1-oauth $1-key -c '{"redirect_uri": ["https://$1.app.cloud.gov/auth","https://$1.app.cloud.gov/logout"]}'
    cf create-service-key "$1-oauth" "$1-key" -c "$OAUTH_SERVICE_ARG"

    formatted_print '--> Creating \e[3mcloud.gov\e[0m Service Account Credentials'
    cf create-service cloud-gov-service-account space-deployer "$1-account"
    cf create-service-key "$1-account" "$1-key"
    formatted_print '--> Please Configure CircleCi Pipeline With The Following Service Credentials.'
    formatted_print '--> Store (username, password) => (CF_DEV_USERNAME, CF_DEV_PASSWORD) In CircleCi Environment'
    cf service-key "$1-account" "$1-key"


    # wait for services to be created. Takes a bit. 
    while [[ "$(cf service $1-sql)" == *"create in progress"* ]]
    do  
        formatted_print '--> Waiting On SQL Service Creation' $SCRIPT_NAME
        formatted_print '--> SQL Service Status:' $SCRIPT_NAME
        cf service "$1-sql"
        sleep 15s
    done 
        # Probably a better way to do this. Research 
        # processes and how to watch them!

    formatted_print '--> Pushing App To Cloud With \e[3m--no-start\e[0m Flag' $SCRIPT_NAME
    cf push --no-start

    formatted_print '--> Binding OAuth Client To App' $SCRIPT_NAME
    # cf bind-service "$1" "$1-oauth" -c '{"redirect_uri": ["https://$1.app.cloud.gov/auth","https://$1.app.cloud.gov/logout"]}'
    cf bind-service $1 "$1-oauth" -c "$OAUTH_SERVICE_ARG"

    SERVICE_KEY="$(cf service-key $1-oauth $1-key)"
    filtered_key="${SERVICE_KEY#*\{}"
    CLIENT_ID=$(echo "{$filtered_key" | python -c 'import json,sys;print(json.load(sys.stdin)["client_id"])')
    CLIENT_SECRET=$(echo "{$filtered_key" | python -c 'import json,sys;print(json.load(sys.stdin)["client_secret"])')

    formatted_print "--> DJANGO SECRET KEY = $SECRET_KEY" $SCRIPT_NAME
    formatted_print "--> (CLIENT_ID, CLIENT_SECRET) = ($CLIENT_ID, $CLIENT_SECRET)" $SCRIPT_NAME
    formatted_print "--> (DJANGO_SUPERUSER_*) = (USERNAME=$DJANGO_SUPERUSER_USERNAME, EMAIL=$DJANGO_SUPERUSER_EMAIL" $SCRIPT_NAME
    formatted_print "--> (EMAIL_HOST, EMAIL_HOST_USER) = ($EMAIL_HOST, $EMAIL_HOST_USER)" $SCRIPT_NAME

    formatted_print "--> Setting Environment Variables On Cloud To Printed Values" $SCRIPT_NAME
    cf set-env $1 SECRET_KEY $SECRET_KEY
    cf set-env $1 UAA_CLIENT_ID $CLIENT_ID
    cf set-env $1 UAA_CLIENT_SECRET $CLIENT_SECRET
    cf set-env $1 DJANGO_SUPERUSER_USERNAME $DJANGO_SUPERUSER_USERNAME
    cf set-env $1 DJANGO_SUPERUSER_EMAIL $DJANGO_SUPERUSER_EMAIL
    cf set-env $1 DJANGO_SUPERUSER_PASSWORD $DJANGO_SUPERUSER_PASSWORD
    cf set-env $1 EMAIL_HOST $EMAIL_HOST
    cf set-env $1 EMAIL_HOST_USER $EMAIL_HOST_USER
    cf set-env $1 EMAIL_HOST_PASSWORD $EMAIL_HOST_PASSWORD

    formatted_print '--> Environment built on the Cloud. Use \e[3mcf-push.sh\e[0m to push application onto the Cloud.'
fi
