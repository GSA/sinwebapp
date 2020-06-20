echo "> Migrating Django Database Files..."
python manage.py migrate

if [ "$1" == "local" ]
then 
    python manage.py collectstatic --noinput
    echo "> Binding Server To Non-Loopback Address for Local Configuration..."
    gunicorn core.wsgi:application --bind=0.0.0.0
else
    echo "> Deploying Server Onto the Cloud..."
    gunicorn core.wsgi:application 
fi