SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='init-migrations.sh'
nl=$'\n'
SCRIPT_DES=""
source "$SCRIPT_DIR/util/logging.sh"

if [ "$1" == "--help" ] || [ "$1" == "--h" ] || [ "$1" == "-help" ] || [ "$1" == "-h" ]
then
    help_print "$SCRIPT_DES" $SCRIPT_NAME
else
    formatted_print "--> Initializing Django Migrations" $SCRIPT_NAME
    # copy current 0002_data.py into db/0002_data.py
    # clean api/migrations
    # create migrations
        # python manage.py makemigrations --name init
    # copy 0002_data.py back into api/migrations
fi