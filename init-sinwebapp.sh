echo "> Migrating Django Database Files..."
python manage.py migrate

if [ "$1" == "local" ]
then 
    echo "> Binding Server To Non-Loopback Address for Local Configuration..."
    gunicorn sinapp.wsgi:application --bind=0.0.0.0
else
    echo "> Deploying Server Onto the Cloud..."
    gunicorn sinapp.wsgi:application 
fi