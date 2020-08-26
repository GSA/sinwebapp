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
${nl}       local - environment for local applicatoin.\
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
        source $SCRIPT_DIR/../env/local.sh

        formatted_print '--> Invoking \e[3minit-scripts.sh\e[0m Script' $SCRIPT_NAME
        bash $SCRIPT_DIR/init-scripts.sh
        
        formatted_print '--> Invoking \e[3msetup-frontend-env.sh\e[0m Script' $SCRIPT_NAM
        bash $SCRIPT_DIR/setup/setup-frontend-env.sh local

        formatted_print '--> Invoking \e[3mbuild-frontend.sh\e[0m Script'
        bash $SCRIPT_DIR/build-frontend.sh

        formatted_print '--> Navigating to Project Root' $SCRIPT_NAME
        cd $SCRIPT_DIR/../sinwebapp/

    elif [ "$1" == "container" ]
    then
        formatted_print '--> Navigating to Project Root' $SCRIPT_NAME
        cd $SCRIPT_DIR/../sinwebapp/
    elif [ "$1" == "cloud" ]
    then
        formatted_print "--> Clearing Sessions" $SCRIPT_NAME
        # python manage.py clearsessions
    fi

    formatted_print '--> Creating New Migrations, If Needed' $SCRIPT_NAME
    python manage.py makemigrations

    formatted_print '--> Migrating Django Database Files' $SCRIPT_NAME
    # python manage.py migrate --fake authentication zero
    # python manage.py migrate --fake-initial

    python manage.py migrate

    # formatted_print "--> Setting <$DJANGO_SUPERUSER_USERNAME, $DJANGO_SUPERUSER_EMAIL> As Superuser" $SCRIPT_NAME
    # python manage.py createsuperuser --username $DJANGO_SUPERUSER_USERNAME --noinput --email $DJANGO_SUPERUSER_EMAIL

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
        # python email_test.py
        formatted_print '--> Deploying Gunicorn Server Onto The Cloud' $SCRIPT_NAME
        gunicorn core.wsgi:application 
    fi
fi