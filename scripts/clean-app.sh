# DESCRIPTION
# Clears the /sinwebapp/static/ and /frontend/node_modules/ directories.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='clean-app.sh'
SCRIPT_DES="This script scrubs the application of all build artifacts"
source "$SCRIPT_DIR/util/logging.sh"

if [ "$1" == "--help" ] || [ "$1" == "--h" ] || [ "$1" == "-help" ] || [ "$1" == "-h" ]
then
    help_print "$SCRIPT_DES" $SCRIPT_NAME
else
    if [ -d "$SCRIPT_DIR/../sinwebapp/static/" ]
    then
        formatted_print '--> Cleaning \e[4m/static/\e[0m Directory' $SCRIPT_NAME
        rm -r $SCRIPT_DIR/../sinwebapp/static/
    fi

    if [ -d "$SCRIPT_DIR/../frontend/node_modules/" ]
    then
        formatted_print '--> Cleaning \e[4m/node_modules/\e[0m Directory' $SCRIPT_NAME
        rm -r $SCRIPT_DIR/../frontend/node_modules/
    fi

    if [ -f "$SCRIPT_DIR/../sinwebapp/init-app.sh" ]
    then 
        formatted_print '--> Cleaning \e[4m/sinwebapp/init-app.sh\e[0m File' $SCRIPT_NAME
        rm $SCRIPT_DIR/../sinwebapp/init-app.sh
    fi

    if [ -f "$SCRIPT_DIR/../sinwebapp/init-migrations.sh" ]
    then 
        formatted_print '--> Cleaning \e[4m/sinwebapp/init-migrations.sh\e[0m File' $SCRIPT_NAME
        rm $SCRIPT_DIR/../sinwebapp/init-migrations.sh
    fi


    if [ -f "$SCRIPT_DIR/../sinwebapp/util/logging.sh" ]
    then 
        formatted_print '--> Cleaning \e[4m/sinwebapp/util/logging.sh\e[0m File' $SCRIPT_NAME
        rm $SCRIPT_DIR/../sinwebapp/util/logging.sh
    fi

    if [ -d "$SCRIPT_DIR/../sinwebapp/util/" ]
    then
        formatted_print '--> Cleaning \e[4m/sinwebapp/util\e[0m Directory' $SCRIPT_NAME
        rm -r $SCRIPT_DIR/../sinwebapp/util/
    fi
fi