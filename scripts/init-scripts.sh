SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='init-scripts.sh'
source "$SCRIPT_DIR/util/logging.sh"

formatted_print '--> Copying Initialization Script Into Application' $SCRIPT_NAME
if [ ! -f "$SCRIPT_DIR/../sinwebapp/init-app.sh" ]
then
    cp $SCRIPT_DIR/init-app.sh $SCRIPT_DIR/../sinwebapp/init-app.sh
fi

if [ ! -d "$SCRIPT_DIR/../sinwebapp/util" ]
then
    mkdir $SCRIPT_DIR/../sinwebapp/util/
    cp $SCRIPT_DIR/util/logging.sh $SCRIPT_DIR/../sinwebapp/util/logging.sh
elif [ ! -f "$SCRIPT_DIR/../sinwebapp/util/logging.sh" ]
then 
    cp $SCRIPT_DIR/util/logging.sh $SCRIPT_DIR/../sinwebapp/util/logging.sh
fi