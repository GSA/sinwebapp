# Cleans the application, copies over scripts into cloud application folder,
# installs frontend dependencies, builds frontend and then pushes to the 
# cloud.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "> Cleaning application"
bash $SCRIPT_DIR/clean-application.sh

echo "> Copying initialization script into app directory..."
cp $SCRIPT_DIR/init-sinwebapp.sh $SCRIPT_DIR/../sinwebapp/init-sinwebapp.sh

echo "> Invoking 'build-frontend.sh' script..."
bash $SCRIPT_DIR/build-frontend.sh

echo "> Pushing to the cloud..."
cd $SCRIPT_DIR/..
cf push
cd $SCRIPT_DIR

echo "> Cleaning up..."
rm $SCRIPT_DIR/../sinwebapp/init-sinwebapp.sh
bash $SCRIPT_DIR/clean-application.sh