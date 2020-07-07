# Executes from sinwebapp/sinwebapp directory (where manage.py is located).
# Gets copied over to project folder in the push-to-cloud.sh script.
# Implemented this way for organizational  reasons. 
# (I like to keep all my scripts in one folder.)

if [ "$1" == "cloud" ]
then
    echo ">> Clearing Sessions..."
    python manage.py clearsessions
fi

echo ">> Migrating Django Database Files..."
python manage.py migrate --fake authentication zero
python manage.py migrate --fake-initial

# If first cloud deployment, comment out the above line
# and uncomment the line below.

# python manage.py migrate 

# If the schema already exists in the connected sql service, 
# then doing a migrate without the --fake-initial flag
# will attempt to recreate the schema and error out.

echo ">> Setting $DJANGO_SUPERUSER_EMAIL As Superuser..."
python manage.py createsuperuser --username $DJANGO_SUPERUSER_EMAIL --noinput

echo ">> Checking Configuration..."
python ./debug.py

if [ "$1" == "container" ]
then 
    echo ">> CONTAINER Environment Detected!"
    echo ">> Collecting Static Files..."
    python manage.py collectstatic --noinput
    echo ">> Binding Gunicorn Server To Non-Loopback Address For Container Configuration..."
    gunicorn core.wsgi:application --bind=0.0.0.0 --workers 3
elif [ "$1" == "local" ]
then
    echo ">> LOCAL Environment Detected!"
    echo ">> Collecting Static Files..."
    python manage.py collectstatic --noinput
    echo ">> Binding Gunicorn Server To 'localhost' For Local Configuration..."
    gunicorn core.wsgi:application --workers 3
elif [ "$1" == "cloud" ]
then
    echo ">> CLOUD Environment Detected!"
    echo ">> Deploying Gunicorn Server Onto The Cloud..."
    gunicorn core.wsgi:application 
fi