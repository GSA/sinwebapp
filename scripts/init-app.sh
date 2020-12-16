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
    formatted_print ">> $1 Environment Detected" $SCRIPT_NAME

    if [ "$1" == "local" ]
    then
        formatted_print '>> Invoking \e[3minit-env.sh\e[0m Script' $SCRIPT_NAME
        source $SCRIPT_DIR/init-env.sh
        
        formatted_print '>> Invoking \e[3msetup-frontend-env.sh\e[0m Script' $SCRIPT_NAME
        bash $SCRIPT_DIR/setup/setup-frontend-env.sh local

        formatted_print '>> Invoking \e[3mbuild-frontend.sh\e[0m Script' $SCRIPT_NAME
        bash $SCRIPT_DIR/build-frontend.sh

        formatted_print '>> Invoking \e[3minit-migrations.sh\e[0m Script' $SCRIPT_NAME
        bash $SCRIPT_DIR/init-migrations.sh $1
       
        formatted_print ">> Navigating To Project Root: $(pwd)" $SCRIPT_NAME
        cd $SCRIPT_DIR/../sinwebapp/

    elif [ "$1" == "container" ]
    then
        formatted_print '>> Invoking \e[3minit-migrations.sh\e[0m Script' $SCRIPT_NAME
        bash $SCRIPT_DIR/init-migrations.sh $1
        
        formatted_print ">> Navigating To Project Root: $(pwd)" $SCRIPT_NAME
        cd $SCRIPT_DIR/../sinwebapp/

    elif [ "$1" == "cloud" ]
    then
        formatted_print ">> Cloud Specific Pre-App Configuration Goes Here" $SCRIPT_NAME
        # python manage.py clearsessions
        # python ./files/s3_manager.py create_bucket

    fi

    formatted_print '>> Migrating Django Database Files' $SCRIPT_NAME
    python manage.py migrate

    formatted_print '>> Printing Configuration' $SCRIPT_NAME
    python debug.py

    if [ "$1" == "container" ]
    then 
        # to lower case
        if [ "${DEVELOPMENT,,}" == "true" ] 
        then
            formatted_print ">> Development Detected, Deploying Angular Dev Server On 0.0.0.0:4200"
            cd $SCRIPT_DIR/../frontend
            nohup ng serve --host 0.0.0.0 --port 4200 > /dev/null 2>&1
            cd $SCRIPT_DIR/../sinwebapp/
        fi
        formatted_print '>> Collecting Static Files' $SCRIPT_NAME
        python manage.py collectstatic --noinput
        formatted_print '>> Binding Gunicorn Server To Non-Loopback Address For Container Configuration' $SCRIPT_NAME
        gunicorn core.wsgi:application --bind=0.0.0.0 --workers 3
    elif [ "$1" == "local" ]
    then
        formatted_print '>> Collecting Static Files' $SCRIPT_NAME
        python manage.py collectstatic --noinput
        formatted_print '>> Binding Gunicorn Server To \e[3mlocalhost\e[0m For Local Configuration' $SCRIPT_NAME
        gunicorn core.wsgi:application --workers 3
    elif [ "$1" == "cloud" ]
    then
        # formatted_print '>> Testing Email Service' $SCRIPT_NAME
        # python ./tests/email_test.py
        formatted_print '>> Deploying Gunicorn Server Onto The Cloud' $SCRIPT_NAME
        gunicorn core.wsgi:application 
    fi
fi