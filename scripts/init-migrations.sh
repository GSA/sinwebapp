SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='init-migrations.sh'
nl=$'\n'
SCRIPT_DES="This script will scrub the existing migrations from the application,${nl}\
    and then create fresh migrations to ensure the model is up to date."
source "$SCRIPT_DIR/util/logging.sh"

if [ "$1" == "--help" ] || [ "$1" == "--h" ] || [ "$1" == "-help" ] || [ "$1" == "-h" ]
then
    help_print "$SCRIPT_DES" $SCRIPT_NAME
else
    formatted_print "--> Initializing Django Migrations" $SCRIPT_NAME
    APP_DIR="$SCRIPT_DIR/../sinwebapp"

    formatted_print '--> Copying Data Migrations Into \e[4m/db/\e[0m Directory Before Scrubbing The Application' $SCRIPT_NAME
    if [ -f "$APP_DIR/api/migrations/0002_api_data.py" ]
    then
        cp "$APP_DIR/api/migrations/0002_api_data.py" "$APP_DIR/db/0002_api_data.py"
    fi
    if [ -f "$APP_DIR/api/authentication/migrations/0002_authentication_data.py" ]
    then
        cp "$APP_DIR/api/authentication/migrations/0002_authentication_data.py" "$APP_DIR/db/0002_authentication_data.py"
    fi
    
    formatted_print "--> Cleaning Migrations In All \e[4m$APP_DIR/\e[0m Modules" $SCRIPT_NAME
    formatted_print '--> Cleaning \e[4m/api/migrations/\e[0m Directory' $SCRIPT_NAME
    rm -r $APP_DIR/api/migrations/
    formatted_print '--> Cleaning \e[4m/api/authentication/\e[0m Directory' $SCRIPT_NAME
    rm -r $APP_DIR/authentication/migrations/

    formatted_print "--> Creating New Migrations"
    cd $APP_DIR
    python manage.py makemigrations api --name init
    python manage.py makemigrations authentication --name init

    cp "$APP_DIR/db/0002_api_data.py" "$APP_DIR/api/migrations/0002_api_data.py"

    if [ ! -d "$APP_DIR/authentication/migrations/" ]
    then
        formatted_print '--> No \e[4m/authentication/migrations/\e[0m Directory Detected, Creating New Directory' $SCRIPT_NAME
        mkdir -p "$APP_DIR/authentication/migrations/"
        touch "$APP_DIR/authentication/migrations/__init__.py"
    fi

    cp  "$APP_DIR/db/0002_authentication_data.py" "$APP_DIR/authentication/migrations/0002_authentication_data.py"
fi