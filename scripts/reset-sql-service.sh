SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='reset-sql-service.sh'
source "$SCRIPT_DIR/util/logging.sh"

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