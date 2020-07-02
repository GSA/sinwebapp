DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo $DIR

if [[ $(pwd) =~ "scripts" ]]
then
    echo '> In /sinwebapp/scripts/ directory, moving to /sinwebapp/frontend/ directory...'
    cd ../frontend
elif [[ $(pwd) =~ "sinwebapp" ]]
then
    echo '> In root /sinwebapp/ directory, moving to /sinwebapp/frontend/ directory...'
    cd frontend
fi

if [ -d '../sinwebapp/static/frontend' ]
then
    echo '> Cleaning /sinwebapp/static/frontend folder...'
    rm -r ../sinwebapp/static/frontend/*
fi

echo "> Building Angular frontend..."
ng build --prod --output-hashing none