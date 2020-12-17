SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='\e[4mbuild-container\e[0m'
nl=$'\n'
SCRIPT_DES="This script will stop and remove any Docker containers currently \
running on your machine,${nl}   clear the Docker cache, configure the frontend \
application's HTTP context for containers,${nl}   build the application \
images, delete any dangling images leftover after the build${nl}   completes and \
then orchestrate the application the application images through docker-compose."
source "$SCRIPT_DIR/util/logging.sh"


if [ "$1" == "--help" ] || [ "$1" == "--h" ] || [ "$1" == "-help" ] || [ "$1" == "-h" ]
then
    help_print "$SCRIPT_DES" $SCRIPT_NAME
else
    formatted_print '>> Initializing Local Environment' $SCRIPT_NAME
    source $SCRIPT_DIR/init-env.sh
    SCRIPT_NAME='\e[4mbuild-container\e[0m'
    formatted_print ">> Python Version: ${PYTHON_VERSION}" $SCRIPT_NAME
    formatted_print ">> Angular Version: ${ANGULAR_VERSION}" $SCRIPT_NAME

    formatted_print '>> Removing Running Containers' $SCRIPT_NAME
    docker-compose down

    formatted_print '>> Clearing Docker Cache' $SCRIPT_NAME
    docker system prune -f

    formatted_print '>> Configuring Application Frontend' $SCRIPT_NAME
    bash $SCRIPT_DIR/setup/setup-frontend-env.sh container

    formatted_print '>> Building Application Image' $SCRIPT_NAME
    docker-compose build

    formatted_print '>> Deleting Dangling Images' $SCRIPT_NAME
    docker rmi $(docker images --filter "dangling=true" -q)

    formatted_print '>> Orchestrating Images' $SCRIPT_NAME
    docker-compose up
fi 