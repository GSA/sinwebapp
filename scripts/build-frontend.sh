echo pwd
if [[ $(pwd) =~ "scripts" ]]
then
    echo '> In scripts directory, moving to frontend directory...'
    cd ../frontend
elif [[ $(pwd) =~ "sinwebapp" ]]
then
    echo '> In root directory, moving to frontend directory...'
    cd frontend
fi

echo "> Building Angular frontend..."
ng build --prod