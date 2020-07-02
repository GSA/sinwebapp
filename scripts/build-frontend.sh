echo "Present working directory: $(pwd)"

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