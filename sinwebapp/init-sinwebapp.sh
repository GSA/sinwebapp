# Executes from sinwebapp/sinwebapp directory (where manage.py is located).
# Gets copied over to project folder in the push-to-cloud.sh script.
# Implemented this way for organizational  reasons. 
# (I like to keep all my scripts in one folder.)

echo "> Migrating Django Database Files..."

python manage.py clearsessions

python manage.py migrate --fake authentication zero
python manage.py migrate --fake-initial

# If first cloud deployment, comment out the above line
# and uncomment the line below.

# python manage.py migrate 

# If the schema already exists in the connected sql service, 
# then doing a migrate without the --fake-initial flag
# will attempt to recreate the schema and error out.

python ./debug.py

if [ "$1" == "container" ]
then 
    python manage.py collectstatic --noinput
    echo ">> CONTAINER Environment Detected"
    echo ">> Binding Server To Non-Loopback Address for Local Configuration..."
    gunicorn core.wsgi:application --bind=0.0.0.0 --workers 3
elif [ "$1" == "local" ]
then
    python manage.py collectstatic --noinput --workers 3
    echo ">> LOCAL Environment Detected"
    echo ">> Binding Server To localhost for Local Configuration..."
    gunicorn core.wsgi:application
elif [ "$1" == "cloud" ]
then
    echo ">> CLOUD Environment Detected"
    echo ">> Deploying Server Onto the Cloud..."
    gunicorn core.wsgi:application 
fi