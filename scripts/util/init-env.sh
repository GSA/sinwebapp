SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='\e[4minit-env\e[0m'
nl=$'\n'
SCRIPT_DES="This script will activate the local environment variables found in ${nl}\
   \e[3mlocal.env\e[0m file. Source this script through bash, e.g. ${nl}${nl}\
           source \e[3m$SCRIPT_DIR/init-env.sh\e[0m"
source "$SCRIPT_DIR/logging.sh"

if [ "$1" == "--help" ] || [ "$1" == "--h" ] || [ "$1" == "-help" ] || [ "$1" == "-h" ]
then
    help_print "$SCRIPT_DES" $SCRIPT_NAME
else
    if [ -f "$SCRIPT_DIR/../env/local.env" ]
    then
        set -o allexport
        source $SCRIPT_DIR/../env/local.env
        set +o allexport
    else
        log 'Please Configure \e[4mlocal.env\e[0m File' $SCRIPT_NAME
    fi
fi
