SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='\e[4minit-scripts\e[0m'
nl=$'\n'
SCRIPT_DES="This script is used during initialization to copy over necessary scripts ${nl}\
   into the backend application before the application server starts."
source "$SCRIPT_DIR/util/logging.sh"

if [ "$1" == "--help" ] || [ "$1" == "--h" ] || [ "$1" == "-help" ] || [ "$1" == "-h" ]
then
    help_print "$SCRIPT_DES" $SCRIPT_NAME
else
    formatted_print '>> Checking For Existence of Initialization Scripts' $SCRIPT_NAME
    if [ ! -f "$SCRIPT_DIR/../sinwebapp/init-app.sh" ]
    then
        formatted_print '>> Copying init-app Script Into Application' $SCRIPT_NAME
        cp $SCRIPT_DIR/init-app.sh $SCRIPT_DIR/../sinwebapp/init-app.sh
    fi

    if [ ! -f "$SCRIPT_DIR/../sinwebapp/init-migrations.sh" ]
    then
        formatted_print '>> Copying init-migrations Script Into Application' $SCRIPT_NAME
        cp $SCRIPT_DIR/init-migrations.sh $SCRIPT_DIR/../sinwebapp/init-migrations.sh
    fi
    
    if [ ! -d "$SCRIPT_DIR/../sinwebapp/util" ]
    then
        formatted_print '>> Copying logging Script Into Application' $SCRIPT_NAME
        mkdir $SCRIPT_DIR/../sinwebapp/util/
        cp $SCRIPT_DIR/util/logging.sh $SCRIPT_DIR/../sinwebapp/util/logging.sh
    elif [ ! -f "$SCRIPT_DIR/../sinwebapp/util/logging.sh" ]
    then 
        cp $SCRIPT_DIR/util/logging.sh $SCRIPT_DIR/../sinwebapp/util/logging.sh
    fi
fi