echo "> Migrating Django Database Files..."

python manage.py clearsessions
python manage.py makemigrations
python manage.py migrate 

python ./debug.py

if [ "$1" == "container" ]
then 
    python manage.py collectstatic --noinput
    echo ">> CONTAINER Environment Detected"
    echo ">> Binding Server To Non-Loopback Address for Local Configuration..."
    gunicorn core.wsgi:application --bind=0.0.0.0
elif [ "$1" == "local" ]
then
    python manage.py collectstatic --noinput
    echo ">> LOCAL Environment Detected"
    echo ">> Binding Server To localhost for Local Configuration..."
    gunicorn core.wsgi:application
elif [ "$1" == "cloud" ]
then
    echo ">> CLOUD Environment Detected"
    echo ">> Deploying Server Onto the Cloud..."
    gunicorn core.wsgi:application 
fi