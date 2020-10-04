SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='\e[4mbuild-frontend\e[0m'
nl=$'\n'
SCRIPT_DES="This script will install the frontend dependencies and then \
build the Angular application.${nl}   The output for the build is controlled \
by the \e[3mangular.json\e[0m within the \e[4m/frontend/\e[0m directory. ${nl}\
   The default built directory is the \e[4m/sinwebapp/static/\e[0m directory."

source "$SCRIPT_DIR/util/logging.sh"

if [ "$1" == "--help" ] || [ "$1" == "--h" ] || [ "$1" == "-help" ] || [ "$1" == "-h" ]
then
    help_print "$SCRIPT_DES" $SCRIPT_NAME
else
    cd $SCRIPT_DIR/../frontend

    formatted_print '--> Installing Angular Dependencies' $SCRIPT_NAME
    npm install

    formatted_print '--> Building Angular Frontend' $SCRIPT_NAME
    ng build --prod --output-hashing none
fi