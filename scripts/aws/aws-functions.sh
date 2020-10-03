# PROCESS TO AUTOMATE IN setup-local-env.sh OR setup-cloud-env.sh SCRIPTS

## 1. Install AWS CLI Client
## 2. Get AWS S3 Credentials From Cloud.Gov S3 Service Provider
## 3. Execute 'aws configure' and provide Acccess and Secret Access Key to CLI
## 4. Make sure local.env is loaded with AWS Bucket Name (also in Cloud.gov S3 Creds)
## 5. source ./this_file

## A light wrapper around the aws S3 CLI client that is configured with credentials
## delivered from the cloud.gov S3 Service Provider to the cloud application
## via the VCAP_SERVICES cloud environment variable. This wrapper performs some
## basic operations, such as deleting all the S3 bucket contents, sync it to a local
## folder, etc.  

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_NAME='aws-functions.sh'
nl=$'\n'
source "$SCRIPT_DIR/../util/logging.sh"

if [ -f "$SCRIPT_DIR/../../env/local.env" ]
then
    formatted_print '--> Reading Environment Variables' $SCRIPT_NAME
    set -o allexport
    source $SCRIPT_DIR/../../env/local.env
    set +o allexport
fi

clean_bucket(){
    aws s3 rm s3://$AWS_BUCKET_NAME --recursive
}

sync_bucket_to_folder(){
    aws s3 sync s3://$AWS_BUCKET_NAME $SCRIPT_DIR/sync/ --recursive
}

sync_folder_to_bucket(){
    aws s3 sync $SCRIPT_DIR/sync/ s3://$AWS_BUCKET_NAME --recursive
}

list_bucket_files(){
    aws s3 ls s3://$AWS_BUCKET_NAME
}