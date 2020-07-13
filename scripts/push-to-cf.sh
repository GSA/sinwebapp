### ARGUMENTS
## OPTIONAL
# clean - wipes application before pushing to cloud,
    # i.e. removes artifacts from previous builds.
# build - builds the application before pushing to
    # the cloud
# dispose - wipes application after pushing to cloud,
    # i.e. removes artifacts from current build.
# reset - returns project to development mode after 
    # pushing, i.e. makes sure all project settings
    # are configured for local deployment.
# trail - trails cloud application logs after pushing

### DESCRIPTION
## Copies over scripts into cloud application folder, installs 
## frontend dependencies, builds frontend and then pushes to the 
## cloud. Frontend build is configured to output into the 
## /sinwebapp/static/folder. Optional argument flags provide other
## functionality.

### NOTE
## Make sure you are logged into cf cli and that you have targetted
## the organization and space you want to deploy the application to 
## before executing this script!

### EXAMPLE USAGE (from project root directory)
    ## 1: $ ./scripts/push-to-cf.sh trail
    ## 2: $ ./scripts/push-to-cf.sh clean trail dispose
    ## 3: $ ./scripts.push-to-cf.sh clean build dispose reset
    
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='push-to-cf.sh'
source "$SCRIPT_DIR/helpers/utilities.sh"

formatted_print 'Invoking \e[3msetup-frontend-env.sh\e[0m Script...' $SCRIPT_NAME
bash $SCRIPT_DIR/setup/setup-frontend-env.sh cloud

for input in $@;
do
    if [ "$input" == "clean" ]
    then
        formatted_print 'Invoking \e[3mclean-app.sh\e[0m Script...' $SCRIPT_NAME
        bash $SCRIPT_DIR/clean-app.sh
    fi
    if [ "$input" == "build " ]
    then 
        formatted_print 'Invoking \e[3mbuild-frontend.sh\e[0m Script...' $SCRIPT_NAME
        bash $SCRIPT_DIR/build-frontend.sh
    fi
done

formatted_print 'Pushing To The Cloud...' $SCRIPT_NAME
cd $SCRIPT_DIR/..
cf push

for input in $@;
do
    if [ "$input" == "dispose" ]
    then
        formatted_print 'Invoking \e[3mclean-app.sh\e[0m Script...' $SCRIPT_NAME
        bash $SCRIPT_DIR/clean-app.sh
    elif [ "$input" == "trail" ]
    then
        formatted_print 'Trailing CF Logs...' $SCRIPT_NAME
        cf logs sinwebapp
    elif [ "$input" == "reset" ]
    then
        formatted_print 'Invoking \e[3msetup-frontend-env.sh\e[0m Script...' $SCRIPT_NAME
        bash $SCRIPT_DIR/setup-frontend-env.sh local
    fi
done

