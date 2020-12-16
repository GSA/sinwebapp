# DESCRIPTION
# Clears the /sinwebapp/static/ and /frontend/node_modules/ directories, in addition
# clearing various clutter that accumulates during development and is not required
# for production.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='\e[4mclean-app\e[0m'
SCRIPT_DES="This script scrubs the application of all build artifacts"
source "$SCRIPT_DIR/util/logging.sh"

if [ "$1" == "--help" ] || [ "$1" == "--h" ] || [ "$1" == "-help" ] || [ "$1" == "-h" ]
then
    help_print "$SCRIPT_DES" $SCRIPT_NAME
else
    if [ -d "$SCRIPT_DIR/../sinwebapp/static/" ]
    then
        formatted_print '>> Caching \e[4m/static/favicon.ico\e[0m' $SCRIPT_NAME
        cp $SCRIPT_DIR/../sinwebapp/static/favicon.ico $SCRIPT_DIR/../sinwebapp/favicon.ico
        formatted_print '>> Cleaning \e[4m/static/\e[0m Directory' $SCRIPT_NAME
        rm -r $SCRIPT_DIR/../sinwebapp/static/
        formatted_print '>> Restoring \e[4m/static/favicon.ico\e[0m' $SCRIPT_NAME
        mkdir $SCRIPT_DIR/../sinwebapp/static/
        touch .gitkeep
        cp $SCRIPT_DIR/../sinwebapp/favicon.ico $SCRIPT_DIR/../sinwebapp/static/favicon.ico
        rm $SCRIPT_DIR/../sinwebapp/favicon.ico
    fi

    if [ -d "$SCRIPT_DIR/../frontend/node_modules/" ]
    then
        formatted_print '>> Cleaning \e[4m/node_modules/\e[0m Directory' $SCRIPT_NAME
        rm -r $SCRIPT_DIR/../frontend/node_modules/
    fi

    if [ -f "$SCRIPT_DIR/../sinwebapp/init-app.sh" ]
    then 
        formatted_print '>> Cleaning \e[4m/sinwebapp/init-app.sh\e[0m File' $SCRIPT_NAME
        rm $SCRIPT_DIR/../sinwebapp/init-app.sh
    fi

    if [ -f "$SCRIPT_DIR/../sinwebapp/init-migrations.sh" ]
    then 
        formatted_print '>> Cleaning \e[4m/sinwebapp/init-migrations.sh\e[0m File' $SCRIPT_NAME
        rm $SCRIPT_DIR/../sinwebapp/init-migrations.sh
    fi


    if [ -f "$SCRIPT_DIR/../sinwebapp/util/logging.sh" ]
    then 
        formatted_print '>> Cleaning \e[4m/sinwebapp/util/logging.sh\e[0m File' $SCRIPT_NAME
        rm $SCRIPT_DIR/../sinwebapp/util/logging.sh
    fi

    if [ -d "$SCRIPT_DIR/../sinwebapp/util/" ]
    then
        formatted_print '>> Cleaning \e[4m/sinwebapp/util\e[0m Directory' $SCRIPT_NAME
        rm -r $SCRIPT_DIR/../sinwebapp/util/
    fi
fi