# DESCRIPTION
# Clears the /sinwebapp/static/ and /frontend/node_modules/ directories.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='clean-application.sh'
source "$SCRIPT_DIR/helpers/utilities.sh"

if [ -d "$SCRIPT_DIR/../sinwebapp/static/" ]
then
    formatted_print 'Cleaning /static/ directory...' $SCRIPT_NAME
    rm -r $SCRIPT_DIR/../sinwebapp/static/
fi
if [ -d "$SCRIPT_DIR/../frontend/node_modules/" ]
then
    formatted_print 'Cleaning /node_modules/ directory...' $SCRIPT_NAME
    rm -r $SCRIPT_DIR/../frontend/node_modules/
fi
