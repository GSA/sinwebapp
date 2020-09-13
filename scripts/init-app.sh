### ARGUMENTS
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='init-app.sh'
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
    formatted_print "--> $1 Environment Detected" $SCRIPT_NAME

    if [ "$1" == "local" ]
    then
        # set environment variables
        formatted_print '--> Setting Environment Variables' $SCRIPT_NAME
        if [ -f "$SCRIPT_DIR/../env/local.env" ]
        then
            set -o allexport
            source $SCRIPT_DIR/../env/local.env
            set +o allexport
        fi

        formatted_print '--> Invoking \e[3minit-scripts.sh\e[0m Script' $SCRIPT_NAME
        bash $SCRIPT_DIR/init-scripts.sh
        
        formatted_print '--> Invoking \e[3msetup-frontend-env.sh\e[0m Script' $SCRIPT_NAM
        bash $SCRIPT_DIR/setup/setup-frontend-env.sh local

        formatted_print '--> Invoking \e[3mbuild-frontend.sh\e[0m Script'
        bash $SCRIPT_DIR/build-frontend.sh

        formatted_print '--> Navigating to Project Root' $SCRIPT_NAME
        cd $SCRIPT_DIR/../sinwebapp/

        formatted_print '--> Invoking \e[3minit-migrations.sh\e[0m Script' $SCRIPT_NAME
        bash $SCRIPT_DIR/init-migrations.sh $1

    elif [ "$1" == "container" ]
    then
        formatted_print '--> Navigating to Project Root' $SCRIPT_NAME
        cd $SCRIPT_DIR/../sinwebapp/

        formatted_print '--> Invoking \e[3minit-migrations.sh\e[0m Script' $SCRIPT_NAME
        bash $SCRIPT_DIR/init-migrations.sh $1

    elif [ "$1" == "cloud" ]
    then
        formatted_print "--> Clearing Sessions" $SCRIPT_NAME
        # python manage.py clearsessions
        # python ./files/s3_manager.py create_bucket
    fi


    formatted_print '--> Migrating Django Database Files' $SCRIPT_NAME
    python manage.py migrate

    formatted_print '--> Printing Configuration' $SCRIPT_NAME
    python debug.py

    if [ "$1" == "container" ]
    then 
        formatted_print '--> Collecting Static Files' $SCRIPT_NAME
        python manage.py collectstatic --noinput
        formatted_print '--> Binding Gunicorn Server To Non-Loopback Address For Container Configuration' $SCRIPT_NAME
        gunicorn core.wsgi:application --bind=0.0.0.0 --workers 3
    elif [ "$1" == "local" ]
    then
        formatted_print '--> Collecting Static Files' $SCRIPT_NAME
        python manage.py collectstatic --noinput
        formatted_print '--> Binding Gunicorn Server To \e[3mlocalhost\e[0m For Local Configuration' $SCRIPT_NAME
        gunicorn core.wsgi:application --workers 3
    elif [ "$1" == "cloud" ]
    then
        formatted_print '--> Testing Email Service' $SCRIPT_NAME
        # python ./tests/email_test.py
        formatted_print '--> Deploying Gunicorn Server Onto The Cloud' $SCRIPT_NAME
        gunicorn core.wsgi:application 
    fi
fi