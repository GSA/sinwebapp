### ARGUMENTS
## REQUIRED
# $1: local, container or cloud
 
### DESCRIPTION
## This script copies the appropriate environment Angular file into a 
## file the angular.json will recognize during the build process.

### EXAMPLE USAGE (from project root directory)
    ## 1: $ ./scripts/setup/setup-frontenv.sh local

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='\e[4msetup-frontend-env\e[0m'
source "$SCRIPT_DIR/../util/logging.sh"

log '>> Initializing Frontend Environment' $SCRIPT_NAME

if [ -f "$SCRIPT_DIR/../../frontend/src/environments/environment.ts" ]
then
    log '>> Cleaning Current Frontend Environment' $SCRIPT_NAME
    rm $SCRIPT_DIR/../../frontend/src/environments/environment.ts
fi

if [ "$1" == "local" ]
then
    log '>> Setting Up Local Frontend Environment' $SCRIPT_NAME
    cp $SCRIPT_DIR/../../frontend/src/environments/environment.local.sample.ts $SCRIPT_DIR/../../frontend/src/environments/environment.ts
elif [ "$1" == "container" ]
then
    log '>> Setting Up Container Frontend Environment' $SCRIPT_NAME
    cp $SCRIPT_DIR/../../frontend/src/environments/environment.container.sample.ts $SCRIPT_DIR/../../frontend/src/environments/environment.ts
elif [ "$1" == "development" ]
then
    log ">> Setting Up Development Mode Frontend Enviroment" $SCRIPT_NAME
    cp $SCRIPT_DIR/../../frontend/src/environments/environment.development.sample.ts $SCRIPT_DIR/../../frontend/src/environments/environment.ts
elif [ "$1" == "cloud" ]
then
    log '>> Setting Up Cloud Frontend Environment' $SCRIPT_NAME
    cp $SCRIPT_DIR/../../frontend/src/environments/environment.cloud.sample.ts $SCRIPT_DIR/../../frontend/src/environments/environment.ts
fi