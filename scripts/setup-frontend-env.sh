SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='setup-frontend-env.sh'
source "$SCRIPT_DIR/helpers/utilities.sh"

if [ -f "$SCRIPT_DIR/../frontend/src/environments/environment.ts" ]
then
    formatted_print 'Cleaning Current Frontend Environment' $SCRIPT_NAME
    rm $SCRIPT_DIR/../frontend/src/environments/environment.ts
fi

if [ "$1" == "local" ]
then
    formatted_print 'Setting Up Local Frontend Environment...' $SCRIPT_NAME
    cp $SCRIPT_DIR/../frontend/src/environments/environment.local.sample.ts $SCRIPT_DIR/../frontend/src/environments/environment.ts
elif [ "$1" == "container" ]
then
    formatted_print 'Setting Up Container Frontend Environment...' $SCRIPT_NAME
    cp $SCRIPT_DIR/../frontend/src/environments/environment.local.sample.ts $SCRIPT_DIR/../frontend/src/environments/environment.ts
elif [ "$1" == "cloud" ]
then
    formatted_print 'Setting Up Cloud Frontend Environment...' $SCRIPT_NAME
    cp $SCRIPT_DIR/../frontend/src/environments/environment.cloud.sample.ts $SCRIPT_DIR/../frontend/src/environments/environment.ts
fi