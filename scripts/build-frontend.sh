### DESCRIPTION
## Installs node dependencies in the package.json within the /frontend/ directory
## and then builds the Angular project. The output for the build is controlled 
## by the angular.json within the /frontend/ directory.

## TODO? Pass in flag to signal different types of builds, i.e. dev vs. prod.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='build-frontend.sh'
source "$SCRIPT_DIR/helpers/utilities.sh"

cd $SCRIPT_DIR/../frontend

formatted_print 'Installing Angular Dependencies...' $SCRIPT_NAME
npm install

formatted_print 'Building Angular Frontend...' $SCRIPT_NAME
ng build --prod --output-hashing none