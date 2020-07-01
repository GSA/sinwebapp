if [[ $(pwd) =~ "scripts" ]]
then
    cd ../frontend
elif [[ $(pwd) =~ "sinwebapp"]]
    cd frontend
fi

ng build