import boto3
from botocore.exceptions import ClientError

from core.settings import aws_creds

from debug import DebugLogger


# Returns True if 'bucket_name' is created successfully. Returns False if 'bucket_name' 
# creation fails
def create_bucket(bucket_name, region=None):
    logger = DebugLogger("sinwebapp.files.s3_manager.create_bucket").get_logger()
    debug_region = "No Region" if region is None else region
    logger.info('Initialzing S3 Bucket "%s" In Region: %s', bucket_name, debug_region)

    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, 
                                    CreateBucketConfiguration=location)
        return True

    except ClientError as e:
        logger.warn('Error Occured Creating S3 Bucket: %s', e)
        return False

# Returns True is 'file_name' is uploaded successfully. Returns False is 'file_name' upload 
# fails.
def upload(file_name, object_name=None):
    logger = DebugLogger("sinwebapp.files.s3_manager.upload").get_logger()
    logger.info('Uploading File "%s" To S3 Bucket "%s"', file_name, aws_creds["bucket"])

    if object_name is None:
        object_name = file_name
    
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, aws_creds["bucket"], str(object_name))
        return True
    except ClientError as e:
        logger.warn('Error Occured Uploading File %s To S3 Bucket: "%s"', file_name, aws_creds["bucket"], e)
        return False

# Returns download if 'file_name' is found within S3. Returns None if 'file_name' doesn't 
# exist within S3.
def download(file_name, object_name=None):
    logger = DebugLogger("sinwebapp.files.s3_manager.download").get_logger()
    logger.info('Downloading File "%s" From S3 Bucket "%s": %s', file_name, aws_creds["bucket"])

    if object_name is None:
        object_name = file_name
    
    s3_client = boto3.client('s3')
    try:
        response = s3_client.download_file(aws_creds["bucket"], object_name, file_name)
        return response
    except ClientError as e:
        logger.warn('Error Occured Downloading File "%s" From S3 Bucket "%s": %s', file_name, aws_creds["bucket"], e)
        return None

# Returns True if 'file_name' is successfully deleted from S3.
def delete(file_name):
    logger = DebugLogger("sinwebapp.files.s3_manager.delete").get_logger()
    logger.info('Deleting File "%s" From S3 Bucket "%s" : "%s"', file_name, aws_creds["bucket"])
    
    s3_client = boto3.client("s3")
    try:
        response = s3_client.delete_object(file_name)
        return True
    except ClientError as e:
        logger.warn('Error Occured Deleting File "%s" From S3 Bucket "%s" : %s', file_name, aws_creds["bucket"], e)
        return False

def list_all():
    logger = DebugLogger("sinwebapp.files.s3_manager.list_files").get_logger()
    logger.info('Retrieving List Of Files From S3 Bucket %s', aws_creds["bucket"])

    s3_client = boto3.client("s3")

    try:
        response = s3_client.list_objects_v2(Bucket=aws_creds["bucket"])
        return response
    except ClientError as e:
        logger.warn('Error Occured Retrieving Files From S3 Bucket "%s"', aws_creds["bucket"])
        return None

def list_for_sin(sin_number):
    logger = DebugLogger("sinwebapp.files.s3_manager.list_files").get_logger()
    logger.info('Retrieving List Of Files From S3 Bucket %s', aws_creds["bucket"])

    s3_client = boto3.client("s3")

    try:
        response = s3_client.list_objects_v2(Bucket=aws_creds["bucket"], Prefix=str(sin_number))
        contents=response["Contents"]
        logger.info('These are the contents: %s', contents)
        return response
    except ClientError as e:
        logger.warn('Error Occured Retrieving Files From S3 Bucket "%s"', aws_creds["bucket"])
        return None