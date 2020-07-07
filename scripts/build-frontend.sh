SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='build-frontend.sh'
source "$SCRIPT_DIR/helpers/utilities.sh"

cd $SCRIPT_DIR/../frontend

formatted_print 'Installing Angular Dependencies...' $SCRIPT_NAME
npm install

formatted_print 'Building Angular Frontend...' $SCRIPT_NAME
ng build --prod --output-hashing none