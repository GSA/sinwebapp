SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [ -d "$SCRIPT_DIR/../sinwebapp/static/" ]
then
    rm -r $SCRIPT_DIR/../sinwebapp/static/
fi
if [ -d "$SCRIPT_DIR/../frontend/node_modules/" ]
then
    rm -r $SCRIPT_DIR/../frontend/node_modules/
fi
