# Script to tear down existing SQL service on your CloudFoundry (Organization, Space)
# and create a new one.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='\e[4mreset-sql-service\e[0m'
nl=$'\n'
SCRIPT_DES="This script will unbind the SQL service from the application and then delete it entirely\
${nl}   from the cloud environment. It will then recreate the SQL service and wait until the${nl}\
   service has been created before releasing control back to the user.${nl}${nl}
   EXAMPLE USAGE${nl}\
       bash reset-sql-service.sh ccda ${nl}${nl}\
   ARGUMENTS - REQUIRED${nl}\
${nl}       app - name of app"
source "$SCRIPT_DIR/util/logging.sh"

if [ "$1" == "--help" ] || [ "$1" == "--h" ] || [ "$1" == "-help" ] || [ "$1" == "-h" ]
then
    help_print "$SCRIPT_DES" $SCRIPT_NAME
else
    if [ "$#" -ne 1 ]; 
    then
        formatted_print "ERROR: No Argument Provided. Please run script with --help flag for more${nl}\
         information" $SCRIPT_NAME
    else
        formatted_print ">> Clearing $1 Existing Service" $SCRIPT_NAME

        cf unbind-service "$1" "$1-sql"
        cf delete-service-key "$1-sql" SERVICE_CONNECT -f
        cf delete-service "$1-sql" -f

        formatted_print '>> Creating New SQL Service' $SCRIPT_NAME
        cf create-service aws-rds medium-psql "$1-sql"

        while [[ "$(cf service $1-sql)" == *"create in progress"* ]]
        do  
            formatted_print '>> Waiting On SQL Service Creation' $SCRIPT_NAME
            formatted_print '>> SQL Service Status:' $SCRIPT_NAME
            cf service "$1-sql"
            sleep 15s
        done

        formatted_print '>> SQL Service Created' $SCRIPT_NAME
    fi
fi