SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='init-migrations.sh'
nl=$'\n'
SCRIPT_DES="This script will scrub the existing migrations from the application,${nl}\
    and then create fresh migrations to ensure the model is up to date.
${nl} 
   EXAMPLE USAGE${nl}\
       bash init-migrations.sh local ${nl}${nl}\
   ARGUMENT - REQUIRED${nl}\
${nl}       local - initialize migrations on local environment\
${nl}       container - initialize migrations on container environment\
${nl}       cloud - initialize migrations on cloud environment"
source "$SCRIPT_DIR/util/logging.sh"

if [ "$1" == "--help" ] || [ "$1" == "--h" ] || [ "$1" == "-help" ] || [ "$1" == "-h" ]
then
    help_print "$SCRIPT_DES" $SCRIPT_NAME
else
    if [ "$#" -ne 1 ]; 
    then
        formatted_print "ERROR: No Argument Provided" $SCRIPT_NAME
    else
        formatted_print "--> Initializing Django Migrations" $SCRIPT_NAME

        # LOAD IN ENVIRONMENT VARIABLES
        if [ "$1" == "local" ]
        then
            formatted_print '--> Reading Environment Variables' $SCRIPT_NAME
            if [ -f "$SCRIPT_DIR/../env/local.env" ]
            then
                formatted_print '--> Importing Environment Variables' $SCRIPT_NAME
                set -o allexport
                source $SCRIPT_DIR/../env/local.env
                set +o allexport
                echo $SECRET_KEY
                echo $AWS_BUCKET_NAME
            fi
        fi

        # NAVIGATE TO FOLDER CONTAINING MANAGE.PY
        if [ "$1" == "local" ] || [ "$1" == "container" ]
        then
            APP_DIR="$SCRIPT_DIR/../sinwebapp"
        fi

        # CACHE CUSTOM MIGRATIONS IN /DB/ FOLDER
        formatted_print '--> Copying Custom Data Migrations Into \e[4m/db/\e[0m Directory Before Scrubbing The Application' $SCRIPT_NAME
        if [ -f "$APP_DIR/api/migrations/0002_api_data.py" ]
        then
            formatted_print '--> Caching 0002_api_data.py' $SCRIPT_NAME
            cp -R "$APP_DIR/api/migrations/0002_api_data.py" "$APP_DIR/db/0002_api_data.py"
        fi
        if [ -f "$APP_DIR/api/migrations/0003_api_validation.py" ]
        then
            formatted_print '--> Caching 0003_api_validation.py' $SCRIPT_NAME
            cp -R "$APP_DIR/api/migrations/0003_api_validation.py" "$APP_DIR/db/0003_api_validation.py"
        fi
        if [ -f "$APP_DIR/authentication/migrations/0002_authentication_data.py" ]
        then
            formatted_print '--> Caching 0002_authentication_data.py' $SCRIPT_NAME
            cp -R "$APP_DIR/authentication/migrations/0002_authentication_data.py" "$APP_DIR/db/0002_authentication_data.py"
        fi
        
        # CLEAN MIGRATIONS
        formatted_print "--> Cleaning Migrations In All \e[4m$APP_DIR/\e[0m Modules" $SCRIPT_NAME
        if [ -d "$APP_DIR/api/migrations/" ]
        then
            formatted_print '--> Cleaning \e[4m/api/migrations/\e[0m Directory' $SCRIPT_NAME
            rm -r $APP_DIR/api/migrations/
        fi
        if [ -d "$APP_DIR/authenication/migrations/" ]
        then
            formatted_print '--> Cleaning \e[4m/authenication/migrations/\e[0m Directory' $SCRIPT_NAME
            rm -r $APP_DIR/authentication/migrations/
        fi

        # CREATE FRESH MIGRAITONS
        formatted_print "--> Creating New Model Migrations"
        cd $APP_DIR
        python manage.py makemigrations api --name init
        python manage.py makemigrations authentication --name init
        python manage.py makemigrations

        # COPY CUSTOM MIGRATIONS BACK INTO APPLICAITON
        if [ ! -d "$APP_DIR/api/migrations/" ]
        then
            formatted_print '--> No \e[4m/api/migrations/\e[0m Directory Detected, Creating New Directory' $SCRIPT_NAME
            mkdir -p "$APP_DIR/authentication/migrations/"
            touch "$APP_DIR/authentication/migrations/__init__.py"
        fi

        formatted_print '--> Copying Custom Data Migrations Back Into Application' $SCRIPT_NAME
        cp -R "$APP_DIR/db/0002_api_data.py" "$APP_DIR/api/migrations/0002_api_data.py"
        cp -R "$APP_DIR/db/0003_api_validation.py" "$APP_DIR/api/migrations/0003_api_validation.py"

        if [ ! -d "$APP_DIR/authentication/migrations/" ]
        then
            formatted_print '--> No \e[4m/authentication/migrations/\e[0m Directory Detected, Creating New Directory' $SCRIPT_NAME
            mkdir -p "$APP_DIR/authentication/migrations/"
            touch "$APP_DIR/authentication/migrations/__init__.py"
        fi

        cp -R "$APP_DIR/db/0002_authentication_data.py" "$APP_DIR/authentication/migrations/0002_authentication_data.py"
    fi
fi