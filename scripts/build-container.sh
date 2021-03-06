SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='build-container'
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
    log '>> Initializing Local Environment' $SCRIPT_NAME
    source $SCRIPT_DIR/util/init-env.sh container
        # reset because sourcing overrides it
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
    SCRIPT_NAME='\e[4mbuild-container\e[0m'

    log ">> Python Version: ${PYTHON_VERSION}" $SCRIPT_NAME
    log ">> Angular Version: ${ANGULAR_VERSION}" $SCRIPT_NAME

    log '>> Removing Running Containers' $SCRIPT_NAME
    docker-compose down

    log '>> Clearing Docker Cache' $SCRIPT_NAME
    docker system prune -f

    
    for arg in "$@"
    do 
        if [ "$arg" == "--fresh" ] || [ "$arg" == "-f" ]
        then
            log "Pruning Docker Volumes From Prior Builds" $SCRIPT_NAME
            bash $SCRIPT_DIR/clean-app.sh
        fi
    done

    log '>> Configuring Application Frontend' $SCRIPT_NAME
    bash $SCRIPT_DIR/setup/setup-frontend-env.sh container

    log '>> Building Application Image' $SCRIPT_NAME
    docker-compose build

    log '>> Deleting Dangling Images' $SCRIPT_NAME
    docker rmi $(docker images --filter "dangling=true" -q)

    log ">> Application Image Built. Run \e[3mdocker-compose up\e[0m To Start \e[7mCCDA\e[0m" $SCRIPT_NAME
fi 