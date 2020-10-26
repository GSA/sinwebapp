import boto3, sys
from botocore.exceptions import ClientError

from core.settings import aws_creds

from debug import DebugLogger

# Returns an S3 Client authenticted with credentials in settings.py
def get_s3_client():
    logger = DebugLogger("sinwebapp.files.s3_manager.get_s3_client").get_logger()
    logger.info('Instantiating boto3 S3 Client')
    return boto3.client('s3', aws_access_key_id=aws_creds['access_key_id'],
                        aws_secret_access_key=aws_creds['secret_access_key'],
                        region_name=aws_creds['region'])

# Returns an S3 Session authenticated with credentials in settings.py      
def get_s3_session():
    logger = DebugLogger("sinwebapp.files.s3_manager.get_s3_session").get_logger()
    logger.info('Instantiating boto3 S3 Session')
    return boto3.session.Session(aws_access_key_id=aws_creds['access_key_id'],
                                aws_secret_access_key=aws_creds['secret_access_key'],
                                region_name=aws_creds['region'])
                                
# Returns True if 'bucket_name' is created successfully. Returns False if 'bucket_name' 
# creation fails
def create_bucket(bucket_name, region=None):
    logger = DebugLogger("sinwebapp.files.s3_manager.create_bucket").get_logger()
    debug_region = "No Region" if region is None else region
    logger.info('Initialzing S3 Bucket %s In Region: %s', bucket_name, debug_region)

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

# Returns True is 'file' is uploaded successfully. Returns False if 'file' upload 
# fails.
def upload(file, file_name):
    logger = DebugLogger("sinwebapp.files.s3_manager.upload").get_logger()
    logger.info('Uploading File %s To S3 Bucket %s With Key %s', file, aws_creds["bucket"], file_name)

    s3_client = get_s3_client()
    # TODO: check if object_name already exists in bucket, if so, append -# identifier to it
    try:
        s3_client.upload_fileobj(Fileobj=file, Bucket=aws_creds["bucket"], Key=str(file_name))
        return True
    except ClientError as e:
        logger.warn('Error Occured Uploading File %s To S3 Bucket: %s', file, aws_creds["bucket"], e)
        return False

# Returns download if 'file_name' is found within S3. Returns None if 'file_name' doesn't 
# exist within S3.
def download(object_name):
    logger = DebugLogger("sinwebapp.files.s3_manager.download").get_logger()
    logger.info('Downloading Attachment for SIN # %s From S3 Bucket "%s"', object_name, aws_creds["bucket"])

    s3_client = get_s3_client()
    try:
        logger.info('trying')
        response = s3_client.get_object(Bucket=aws_creds["bucket"], Key=object_name)
        logger.info('did it')
        return response 
    except:
        e = sys.exc_info()[0]
        f = sys.exc_info()[1]
        g = sys.exc_info()[2]
        logger.warn('Error Occured Downloading Attachment For SIN # %s From S3 Bucket %s: %s', object_name, aws_creds["bucket"])
        logger.warn('Error: %s %s %s', e, f, g)
        return None

# Returns True if 'file_name' is successfully deleted from S3.
def delete(file_name):
    logger = DebugLogger("sinwebapp.files.s3_manager.delete").get_logger()
    logger.info('Deleting File "%s" From S3 Bucket "%s" : "%s"', file_name, aws_creds["bucket"])
    
    s3_client = get_s3_client()
    try:
        response = s3_client.delete_object(file_name)
        return True
    except ClientError as e:
        logger.warn('Error Occured Deleting File "%s" From S3 Bucket "%s" : %s', file_name, aws_creds["bucket"], e)
        return False

# Returns list of all files in S3 Bucket
def list_all():
    logger = DebugLogger("sinwebapp.files.s3_manager.list_all").get_logger()
    logger.info('Retrieving List Of Files From S3 Bucket %s', aws_creds["bucket"])

    s3_client = get_s3_client()

    try:
        response = s3_client.list_objects_v2(Bucket=aws_creds["bucket"])['Contents']
        return response
    except ClientError as e:
        logger.warn('Error Occured Retrieving Files From S3 Bucket "%s"', aws_creds["bucket"])
        return None

# Returns a list of files filtered by sin_number in S3 Bucket
def list_for_sin(sin_number):
    logger = DebugLogger("sinwebapp.files.s3_manager.list_for_sin").get_logger()
    logger.info('Retrieving List Of Files From S3 Bucket "%s"', aws_creds["bucket"])
    
    s3_client = get_s3_client()

    try:
        response = s3_client.list_objects_v2(Bucket=aws_creds["bucket"], Prefix=str(sin_number))['Contents']
        return response
    except ClientError as e:
        logger.warn('Error Occured Retrieving Files From S3 Bucket "%s"', aws_creds["bucket"])
        return None