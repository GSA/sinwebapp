SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME="\e[4minit-migrations\e[0m"
nl=$'\n'
SCRIPT_DES="This script will scrub the existing migrations from the application,${nl}\
    and then create fresh migrations to ensure the model is up to date. Ensure \e[3mlocal.env\e[0m${nl}\
     file is loaded if executing this script locally. In other words, before running this ${nl}\
    on your local computer, configure your \e[3mlocal.env\e[0m file and then execute \
    ${nl}${nl}           source \e[3m$SCRIPT_DIR/init-env.sh\e[0m ${nl}${nl}\
    which will activate the \e[3mlocal.env\e[0m file.${nl}\
         This script will leave the terminal within the $SCRIPT_DIR/../sinwebapp/
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
        formatted_print ">> Initializing Django Migrations" $SCRIPT_NAME

        # NAVIGATE TO FOLDER CONTAINING MANAGE.PY
        if [ "$1" == "local" ] || [ "$1" == "container" ]
        then
            APP_DIR="$SCRIPT_DIR/../sinwebapp"
        else 
            # executing from cloud environment
            APP_DIR=$SCRIPT_DIR
        fi

        formatted_print ">> Navigating To Project Root" $SCRIPT_NAME
        cd $APP_DIR
        formatted_print ">> Project Root: $(pwd)" $SCRIPT_NAME

        # CACHE CUSTOM MIGRATIONS IN /DB/ FOLDER
        formatted_print '>> Copying Custom Data Migrations Into \e[4m/db/\e[0m Directory Before Scrubbing The Application' $SCRIPT_NAME
        if [ -f "$APP_DIR/api/migrations/0002_api_data.py" ]
        then
            formatted_print '>> Caching 0002_api_data.py' $SCRIPT_NAME
            cp -R "$APP_DIR/api/migrations/0002_api_data.py" "$APP_DIR/db/0002_api_data.py"
        fi
        if [ -f "$APP_DIR/api/migrations/0003_api_validation.py" ]
        then
            formatted_print '>> Caching 0003_api_validation.py' $SCRIPT_NAME
            cp -R "$APP_DIR/api/migrations/0003_api_validation.py" "$APP_DIR/db/0003_api_validation.py"
        fi
        if [ -f "$APP_DIR/authentication/migrations/0002_authentication_data.py" ]
        then
            formatted_print '>> Caching 0002_authentication_data.py' $SCRIPT_NAME
            cp -R "$APP_DIR/authentication/migrations/0002_authentication_data.py" "$APP_DIR/db/0002_authentication_data.py"
        fi
        
        # CLEAN MIGRATIONS
        formatted_print ">> Cleaning Migrations In All \e[4m$APP_DIR/\e[0m Modules" $SCRIPT_NAME
        if [ -d "$APP_DIR/api/migrations/" ]
        then
            formatted_print '>> Cleaning \e[4m/api/migrations/\e[0m Directory' $SCRIPT_NAME
            rm -r $APP_DIR/api/migrations/
        fi
        if [ -d "$APP_DIR/authentication/migrations/" ]
        then
            formatted_print '>> Cleaning \e[4m/authenication/migrations/\e[0m Directory' $SCRIPT_NAME
            rm -r $APP_DIR/authentication/migrations/
        fi

        # CREATE FRESH MIGRAITONS
        formatted_print ">> Creating New Model Migrations"
        python manage.py makemigrations api --name init
        python manage.py makemigrations authentication --name init
        python manage.py makemigrations

        # COPY CUSTOM MIGRATIONS BACK INTO APPLICAITON
        if [ ! -d "$APP_DIR/api/migrations/" ]
        then
            formatted_print '>> No \e[4m/api/migrations/\e[0m Directory Detected, Creating New Directory' $SCRIPT_NAME
            mkdir -p "$APP_DIR/api/migrations/"
            touch "$APP_DIR/api/migrations/__init__.py"
        fi
        if [ ! -d "$APP_DIR/authentication/migrations/" ]
        then
            formatted_print '>> No \e[4m/authentication/migrations/\e[0m Directory Detected, Creating New Directory' $SCRIPT_NAME
            mkdir -p "$APP_DIR/authentication/migrations/"
            touch "$APP_DIR/authentication/migrations/__init__.py"
        fi

        formatted_print '>> Copying Custom Data Migrations Back Into Application' $SCRIPT_NAME
        cp -R "$APP_DIR/db/0002_api_data.py" "$APP_DIR/api/migrations/0002_api_data.py"
        cp -R "$APP_DIR/db/0003_api_validation.py" "$APP_DIR/api/migrations/0003_api_validation.py"
        cp -R "$APP_DIR/db/0002_authentication_data.py" "$APP_DIR/authentication/migrations/0002_authentication_data.py"
    fi
fi