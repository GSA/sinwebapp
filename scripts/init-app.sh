### ARGUMENTS
## REQUIRED
# 1: local, container or cloud: specifies the type of environment to initialize in.

### DESCRIPTION
## Initializes python web application by clearing any outstanding sessions,
## migrating Django models to the database, setting up a super-user account,
## collecting static files (for local deployments; the cloud automatically
## collects static files) and starts a Gunicorn server and binds the WSGI
## applicaiton to it.

### EXAMPLE USAGE 
## None! This script is used in the Dockerfile and manifest.yml. 
## It executes from inside of the container running the application.
## This script is used to initialize various properties in the Django
## web framework and start the web server.

### TODO: pass in argument to determine how migrations should proceed.

if [ "$1" == "cloud" ]
then
    echo -e "> \e[4minit-sinwebapp.sh\e[0m: Clearing Sessions..."
    python manage.py clearsessions
fi

echo -e "> \e[4minit-sinwebapp.sh\e[0m: Migrating Django Database Files..."
python manage.py migrate --fake authentication zero
python manage.py migrate --fake-initial

# If the schema already exists in the connected sql service, then doing a migrate without the --fake-initial flag
# will attempt to recreate the schema and error out. If first cloud deployment, comment out the above line
# and uncomment the line below. This will perform the migrations on a fresh database

# python manage.py migrate 

# TODO: pass in flag to automate this 

echo -e "> \e[4minit-sinwebapp.sh\e[0m: Setting $DJANGO_SUPERUSER_USERNAME, $DJANGO_SUPERUSER_EMAIL As Superuser..."
python manage.py createsuperuser --username $DJANGO_SUPERUSER_USERNAME --noinput --email $DJANGO_SUPERUSER_EMAIL

echo -e '> \e[4minit-sinwebapp.sh\e[0m: Checking Configuration...'
python ./debug.py

if [ "$1" == "container" ]
then 
    echo -e '> \e[4minit-sinwebapp.sh\e[0m: CONTAINER Environment Detected!'
    echo -e '> \e[4minit-sinwebapp.sh\e[0m: Collecting Static Files...'
    python manage.py collectstatic --noinput
    echo -e '> \e[4minit-sinwebapp.sh\e[0m: Binding Gunicorn Server To Non-Loopback Address For Container Configuration...'
    gunicorn core.wsgi:application --bind=0.0.0.0 --workers 3
elif [ "$1" == "local" ]
then
    echo -e '> \e[4minit-sinwebapp.sh\e[0m: LOCAL Environment Detected!'
    echo -e '> \e[4minit-sinwebapp.sh\e[0m: Collecting Static Files...'
    python manage.py collectstatic --noinput
    echo -e '> \e[4minit-sinwebapp.sh\e[0m: Binding Gunicorn Server To \e[3mlocalhost\e[0m For Local Configuration...'
    gunicorn core.wsgi:application --workers 3
elif [ "$1" == "cloud" ]
then
    echo -e '> \e[4minit-sinwebapp.sh\e[0m: CLOUD Environment Detected!'
    echo -e '> \e[4minit-sinwebapp.sh\e[0m: Deploying Gunicorn Server Onto The Cloud...'
    gunicorn core.wsgi:application 
fi