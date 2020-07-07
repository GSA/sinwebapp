### ARGUMENTS
## OPTIONAL
# clean - wipes application before pushing to cloud,
    # removes artifacts from previous builds.
# dispose - wipes application after pushing to cloud,
    # removes artifacts from current build.
# trail - trails cloud application logs after pushing

### DESCRIPTOIN
## Copies over scripts into cloud application folder, installs 
## frontend dependencies, builds frontend and then pushes to the 
## cloud. Optional flags provide other functionality.

### EXAMPLE USAGE (from project root directory)
    ## 1: $ ./scripts/push-to-cf.sh trail
    ## 2: $ ./scripts/push-to-cf.sh clean dispose trail
    
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='push-to-cf.sh'
source "$SCRIPT_DIR/helpers/utilities.sh"

for input in $@;
do
    if [ "$input" == "clean" ]
    then
        formatted_print 'Invoking \e[3mclean-application.sh\e[0m Script...' $SCRIPT_NAME
        bash $SCRIPT_DIR/clean-application.sh
    fi
done

formatted_print 'Copying Initialization Script Into App Directory...' $SCRIPT_NAME
cp $SCRIPT_DIR/init-sinwebapp.sh $SCRIPT_DIR/../sinwebapp/init-sinwebapp.sh

formatted_print 'Invoking \e[3msetup-frontend-env.sh\e[0m Script...' $SCRIPT_NAME
bash $SCRIPT_DIR/setup/setup-frontend-env.sh cloud

formatted_print 'Invoking \e[3mbuild-frontend.sh\e[0m Script...' $SCRIPT_NAME
bash $SCRIPT_DIR/build-frontend.sh

formatted_print 'Pushing To The Cloud...' $SCRIPT_NAME
cd $SCRIPT_DIR/..
cf push

formatted_print 'Resetting Frontend Environment To \e[3mlocalhost\e[0m...'
formatted_print 'Invoking \e[3msetup-frontend-env.sh\e[0m Script...' $SCRIPT_NAME
bash $SCRIPT_DIR/setup-frontend-env.sh local

for input in $@;
do
    if [ "$input" == "dispose" ]
    then
        formatted_print 'Invoking \e[3mclean-application.sh\e[0m Script...' $SCRIPT_NAME
        bash $SCRIPT_DIR/clean-application.sh
    fi
    if [ "$input" == "trail" ]
    then
        formatted_print 'Trailing CF Logs...' $SCRIPT_NAME
        cf logs sinwebapp
    fi
done

