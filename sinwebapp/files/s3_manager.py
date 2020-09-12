import boto3
from botocore.exceptions import ClientError

from core.settings import aws_creds

from debug import DebugLogger

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

    except ClientError as e:
        logger.warn('Error Occured Creating S3 Bucket: %s', e)
        return False
    
    return True

def upload(file_name, object_name=None):
    logger = DebugLogger("sinwebapp.files.s3_manager.upload").get_logger()
    logger.info('Uploading File "%s" To S3 Bucket "%s"', file_name, aws_creds["bucket"])

    if object_name is None:
        object_name = file_name
    
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, aws_creds["bucket"], object_name)
    except ClientError as e:
        logger.warn('Error Occured Uploading File %s To S3 Bucket: "%s"', file_name, aws_creds["bucket"],e )

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

def delete(file_name):
    logger = DebugLogger("sinwebapp.files.s3_manager.delete").get_logger()
    logger.info('Deleting File "%s" From S3 Bucket "%s" : "%s"', file_name, aws_creds["bucket"])
    
    s3_client = boto3.client("s3")
    try:
        response = s3_client.delete_object(file_name)
    except ClientError as e:
        logger.warn('Error Occured Deleting File "%s" From S3 BUCKET "%s" : %s', file_name, aws_creds["bucket"], e)