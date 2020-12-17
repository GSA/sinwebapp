### ARGUMENTS
# $1: Required: dev, staging or prod

### NOTE: This script is only executed within the CircleCi pipeline
##          environment to push application builds to the cloud.

### NOTE: $CF_DEV_USER, $CF_DEV_PASSWORD store the CloudFoundry dev login
### credentials on the CircleCi environment. $CF_ORGANIZATION, 
### $CF_DEV_SPACE, $CF_STAGING_SPACE and $CF_PROD_SPACE store the
### attributes used to target an organization and space on 
### CloudFounry.

# TODO: verify number of arguments, else exit

# TODO: Need CircleCi credentials for different environments

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='\e[4mcc-cf-push\e[0m'
nl=$'\n'
SCRIPT_DES="This script should only be invoked within the CircleCI pipeline environment. \
This script is used after${nl}   the application has been built on the pipeline and is \
ready for deployment. This script will push the${nl}   pipeline build on the cloud using \
dummy account credentials provided by a service account within cloud.gov."
source "$SCRIPT_DIR/util/logging.sh"

if [ "$1" == "--help" ] || [ "$1" == "--h" ] || [ "$1" == "-help" ] || [ "$1" == "-h" ]
then
    help_print "$SCRIPT_DES" $SCRIPT_NAME
else
    cf api api.fr.cloud.gov
    if [ "$1" == "dev" ]
    then
        cf auth $CF_DEV_USERNAME $CF_DEV_PASSWORD
        formatted_print ">> Targetting (Org, Space) = ($CF_ORGANIZATION, $CF_DEV_SPACE)" $SCRIPT_NAME
        cf target -o $CF_ORGANIZATION -s $CF_DEV_SPACE
    elif [ "$1" == "prod" ]
    then
        cf auth $CF_PROD_USERNAME $CF_PROD_PASSWORD
        formatted_print ">> Targetting (Org, Space) = ($CF_ORGANIZATION, $CF_PROD_SPACE)" $SCRIPT_NAME
        cf target -o $CF_ORGANIZATION -s $CF_PROD_SPACE
    elif [ "$1" == "staging" ]
    then
        cf auth $CF_STAGING_USERNAME $CF_STAGING_PASSWORD
        formatted_print ">> Targetting (Org, Space) = ($CF_ORGANIZATION, $CF_STAGING_SPACE)" $SCRIPT_NAME
        cf target -o $CF_ORGANIZATION -s $CF_STAGING_SPACE
    fi

    formatted_print '>> Pushing To CloudFoundry' $SCRIPT_NAME
    cf push
fi

