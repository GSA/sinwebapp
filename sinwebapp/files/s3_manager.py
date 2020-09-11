import boto3
from botocore.exceptions import ClientError

from debug import DebugLogger

def create_bucket(bucket_name, region=None):
    logger = DebugLogger("sinwebapp.files.views.init_s3").get_logger()
    debug_region = "No Region" if region is None else region
    logger.info('Initialzing S3 Bucket "%s" In Region: %s', bucket_name, debug_region)
    # region defaults to (us-east-1) if no region provided
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, 
                                    CreateBucketConfiguration=location)

    except ClientError as e:
        logger.warn('Error Occured Creating S3 Bucket: %s', e)
        return False
    
    return True

def upload_file(file_name, bucket, object_name=None):
    logger = DebugLogger("sinwebapp.files.views.upload_file").get_logger()
    logger.info('Uploading File "%s" To S3 Bucket "%s"', file_name, bucket)

    if object_name is None:
        object_name = file_name
    
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logger.warn('Error Occured Uploading File %s To S3 Bucket: "%s"', file_name, bucket_name)

def download_file(file_name, bucket, object_name=None):
    logger = DebugLogger("sinwebapp.files.views.download_file").get_logger()
    logger.info('Downloading File "%s" From S3 Bucket "%s": %s', file_name, bucket)

    if object_name is None:
        object_name = file_name
    
    s3_client = boto3.client('s3')
    try:
        response = s3_client.download_file(bucket, object_name, file_name)
        return response
    except ClientError as e:
        logger.warn('Error Occured Downloading File "%s" From S3 Bucket "%s": %s', file_name, bucket)