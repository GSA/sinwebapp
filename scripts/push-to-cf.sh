# Cleans the application, copies over scripts into cloud application folder,
# installs frontend dependencies, builds frontend and then pushes to the 
# cloud.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "> Cleaning Application..."
bash $SCRIPT_DIR/clean-application.sh

echo "> Copying Initialization Script Into App Directory..."
cp $SCRIPT_DIR/init-sinwebapp.sh $SCRIPT_DIR/../sinwebapp/init-sinwebapp.sh

echo "> Invoking 'build-frontend.sh' Script..."
bash $SCRIPT_DIR/build-frontend.sh

echo "> Pushing To The Cloud..."
cd $SCRIPT_DIR/..
cf push
cd $SCRIPT_DIR

echo "> Cleaning Up..."
rm $SCRIPT_DIR/../sinwebapp/init-sinwebapp.sh
bash $SCRIPT_DIR/clean-application.sh