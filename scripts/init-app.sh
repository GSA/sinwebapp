### ARGUMENTS
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='\e[4minit-app\e[0m'
nl=$'\n'
SCRIPT_DES="This script will perform environment-specific configuration and ${nl}\
   initialization based on the provided argument. After setting up the ${nl}\
   environment, this script will run Django migrations. Finally, it will${nl}\
   bind the WSGI Django application to a Gunicorn server and start the${nl}\
   server on port 8000.
 ${nl} 
   EXAMPLE USAGE${nl}\
       bash init-app.sh local ${nl}${nl}\
   ARGUMENT - REQUIRED${nl}\
${nl}       local - environment for local application.\
${nl}       container - environment for container application \
${nl}       cloud - environment for cloud application"
source "$SCRIPT_DIR/util/logging.sh"

if [ "$1" == "--help" ] || [ "$1" == "--h" ] || [ "$1" == "-help" ] || [ "$1" == "-h" ]
then
    help_print "$SCRIPT_DES" $SCRIPT_NAME
else
    log ">> $1 Argument Provided, Ensuring Environment Initialized" $SCRIPT_NAME

    if [ "$1" == "local" ]
    then
        log '>> Invoking \e[3minit-env.sh\e[0m Script' $SCRIPT_NAME
        source $SCRIPT_DIR/init-env.sh
        
        log '>> Invoking \e[3msetup-frontend-env.sh\e[0m Script' $SCRIPT_NAME
        bash $SCRIPT_DIR/setup/setup-frontend-env.sh local

        log '>> Invoking \e[3mbuild-frontend.sh\e[0m Script' $SCRIPT_NAME
        bash $SCRIPT_DIR/build-frontend.sh

        log '>> Invoking \e[3minit-migrations.sh\e[0m Script' $SCRIPT_NAME
        bash $SCRIPT_DIR/init-migrations.sh $1
       
        log ">> Navigating To Project Root: $(pwd)" $SCRIPT_NAME
        cd $SCRIPT_DIR/../sinwebapp/

    elif [ "$1" == "container" ] || [ "$1" == "mcaas"] 
    then
        log '>> Invoking \e[3minit-migrations.sh\e[0m Script' $SCRIPT_NAME
        bash $SCRIPT_DIR/init-migrations.sh $1
        
        log ">> Navigating To Project Root: $(pwd)" $SCRIPT_NAME
        cd $SCRIPT_DIR/../sinwebapp/

    elif [ "$1" == "cloud" ]
    then
        log ">> Cloud Specific Pre-App Configuration Goes Here" $SCRIPT_NAME
        # python manage.py clearsessions
        # python ./files/s3_manager.py create_bucket

    fi

    log '>> Migrating Django Database Files' $SCRIPT_NAME
    python manage.py migrate

    log '>> Printing Configuration' $SCRIPT_NAME
    python debug.py

    # NOTE: Check APP_ENV variable, since Dockerfile specifies an argument of 
    # 'container' for this script. The Dockerfile is used to launch application
    # in MCaaS **and** locally, so script needs to differentiate these enviroments
    # by using APP_ENV instead of argument to script.
    if [ "$APP_ENV" == "container" ]
    then 
        # $DEVELOPMENT to lower case
        if [ "${DEVELOPMENT,,}" == "true" ] 
        then
            log ">> Development Mode Detected, Configuring Frontend For Live Re-loading" $SCRIPT_NAME
            bash $SCRIPT_DIR/setup/setup-frontend-env.sh development
            log "Deploying Angular Dev Server Onto 0.0.0.0:4200" $SCRIPT_NAME
            cd $SCRIPT_DIR/../frontend
            nohup ng serve --host 0.0.0.0 --port 4200 > /dev/null 2>&1 &
            cd $SCRIPT_DIR/../sinwebapp/
        fi
        log '>> Collecting Static Files' $SCRIPT_NAME
        python manage.py collectstatic --noinput
        log '>> Binding Gunicorn Server To Non-Loopback Address For Container Configuration' $SCRIPT_NAME
        gunicorn core.wsgi:application --bind=0.0.0.0 --workers 3

    elif [ "$APP_ENV" == "local" ]
    then
        log '>> Collecting Static Files' $SCRIPT_NAME
        python manage.py collectstatic --noinput
        log '>> Binding Gunicorn Server To \e[3mlocalhost\e[0m For Local Configuration' $SCRIPT_NAME
        gunicorn core.wsgi:application --workers 3
    
    elif [ "$APP_ENV" == "mcaas" ]
    then
        log '>> Colleting Static Files' $SCRIPT_NAME
        python manage.py collect static --noinput
        log '>> Binding Gunicorn Server to Non-Loopback Address for Container Configuration'
        ddtrace-run gunicorn core.wsgi:application --bind=0.0.0.0 --workers=3

    elif [ "$APP_ENV" == "cloud" ]
    then
        # log '>> Testing Email Service' $SCRIPT_NAME
        # python ./tests/email_test.py
        log '>> Deploying Gunicorn Server Onto The Cloud' $SCRIPT_NAME
        gunicorn core.wsgi:application 
    fi
fi