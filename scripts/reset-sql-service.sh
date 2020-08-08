# Script to tear down existing SQL service on your CloudFoundry (Organization, Space)
# and create a new one.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='reset-sql-service.sh'
nl=$'\n'
SCRIPT_DES="This script will unbind the SQL service from the application and then delete it entirely\
${nl}   from the cloud environment. It will then recreate the SQL service and wait until the${nl}\
   service has been created before releasing control back to the user."
source "$SCRIPT_DIR/util/logging.sh"

if [ "$1" == "--help" ] || [ "$1" == "--h" ] || [ "$1" == "-help" ] || [ "$1" == "-h" ]
then
    help_print "$SCRIPT_DES" $SCRIPT_NAME
else
    formatted_print '--> Clearing Existing Service' $SCRIPT_NAME

    cf unbind-service sinweb sin-sql
    cf delete-service sin-sql -f

    formatted_print '--> Creating New SQL Service' $SCRIPT_NAME
    cf create-service aws-rds medium-psql sin-sql

    while [[ "$(cf service sin-sql)" == *"create in progress"* ]]
    do  
        formatted_print '--> Waiting On SQL Service Creation' $SCRIPT_NAME
        formatted_print '--> SQL Service Status:' $SCRIPT_NAME
        cf service sin-sql
        sleep 15s
    done

    formatted_print '--> SQL Service Created' $SCRIPT_NAME
fi