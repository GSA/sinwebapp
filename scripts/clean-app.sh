# DESCRIPTION
# Clears the /sinwebapp/static/ and /frontend/node_modules/ directories.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='clean-app.sh'
source "$SCRIPT_DIR/helpers/utilities.sh"

if [ -d "$SCRIPT_DIR/../sinwebapp/static/" ]
then
    formatted_print '--> Cleaning \e[4m/static/\e[0m Directory' $SCRIPT_NAME
    rm -r $SCRIPT_DIR/../sinwebapp/static/
fi
if [ -d "$SCRIPT_DIR/../frontend/node_modules/" ]
then
    formatted_print '--> Cleaning \e[4m/node_modules/\e[0m Directory' $SCRIPT_NAME
    rm -r $SCRIPT_DIR/../frontend/node_modules/
fi
