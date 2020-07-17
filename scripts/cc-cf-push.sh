### ARGUMENTS
# $1: Required: dev, staging or prod

### Note: $CF_DEV_USER, $CF_DEV_PASSWORD store the CloudFoundry login
### credentials on the CircleCi environment. $CF_ORGANIZATION, 
### $CF_DEV_SPACE, $CF_STAGING_SPACE and $CF_PROD_SPACE store the
### attributes used to target an organization and space on 
### CloudFounry.

# TODO: verify number of arguments, else exit
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='cc-cf-push.sh'
source "$SCRIPT_DIR/util/logging.sh"

cf api api.fr.cloud.gov
if [ "$1" == "dev" ]
then
    cf auth $CF_DEV_USERNAME $CF_DEV_PASSWORD
    cf target -o $CF_ORGANIZATION -s $CF_DEV_SPACE
elif [ "$1" == "prod" ]
then
    cf auth $CF_DEV_USERNAME $CF_DEV_PASSWORD
    cf target -o $CF_ORGANIZATION -s $CF_PROD_SPACE
elif [ "$1" == "staging" ]
then
    cf auth $CF_DEV_USERNAME $CF_DEV_PASSWORD
    cf target -o $CF_ORGANIZATION -s $CF_STAGING_SPACE
fi

cf push

