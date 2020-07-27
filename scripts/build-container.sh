### DESCRIPTION
## builds the app and starts it up

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='build-app.sh'
source "$SCRIPT_DIR/util/logging.sh"

formatted_print '--> Removing Running Containers' $SCRIPT_NAME
docker-compose down

formatted_print '--> Configuring Application Environment' $SCRIPT_NAME
bash $SCRIPT_DIR/setup/setup-frontend-env.sh container

formatted_print '--> Building Application Image' $SCRIPT_NAME
docker-compose build

formatted_print '--> Deleting Dangling Images' $SCRIPT_NAME
docker rmi $(docker images --filter "dangling=true" -q)

formatted_print '--> Orchestrating Images' $SCRIPT_NAME
docker-compose up