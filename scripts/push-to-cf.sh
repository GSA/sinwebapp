# ARGUMENTS
# FLAGS
# clean
# build
# trail
# TODO: determine number of arguments and parse them

# Copies over scripts into cloud application folder, installs 
# frontend dependencies, builds frontend and then pushes to the 
# cloud.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='push-to-cf.sh'
source "$SCRIPT_DIR/helpers/utilities.sh"

formatted_print 'Copying Initialization Script Into App Directory...' $SCRIPT_NAME
cp $SCRIPT_DIR/init-sinwebapp.sh $SCRIPT_DIR/../sinwebapp/init-sinwebapp.sh

formatted_print 'Invoking \e[3msetup-frontend-env.sh\e[0m Script...' $SCRIPT_NAME
bash $SCRIPT_DIR/setup-frontend-env.sh cloud

formatted_print 'Invoking \e[3mbuild-frontend.sh\e[0m Script...' $SCRIPT_NAME
bash $SCRIPT_DIR/build-frontend.sh

formatted_print 'Pushing To The Cloud...' $SCRIPT_NAME
cd $SCRIPT_DIR/..
cf push

formatted_print 'Resetting Frontend Environment To \e[3mlocalhost\e[0m...'
formatted_print 'Invoking \e[3msetup-frontend-env.sh\e[0m Script...' $SCRIPT_NAME
bash $SCRIPT_DIR/setup-frontend-env.sh local

