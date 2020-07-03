SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd $SCRIPT_DIR/../frontend

if [ -d "$SCRIPT_DIR/../sinwebapp/static/frontend" ]
then
    echo '> Cleaning /sinwebapp/static/frontend folder...'
    rm -r $SCRIPT_DIR/../sinwebapp/static/frontend/*
fi

echo "> Installing Angular Dependencies"
npm install

echo "> Building Angular frontend..."
ng build --prod --output-hashing none