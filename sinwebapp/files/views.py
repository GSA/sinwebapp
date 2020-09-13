import os

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from files.s3_manager import upload, download, list_for_sin, list_all
from files.forms import UploadFileForm
from core.settings import APP_ENV, BASE_DIR
from debug import DebugLogger

LOCAL_SAVE_DIR=BASE_DIR+'/files/local_uploads/'

@login_required
def upload_file(request):
    logger = DebugLogger("sinwebapp.files.views.upload_file").get_logger()
    logger.info('Posting File Form')

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        
        logger.info('Validating Form')
        if form.is_valid():
            logger.info('Form Validated')

            if APP_ENV == "cloud":
                logger.info('Uploading File To S3 Storage Bucket')
                upload_check = upload(request.FILES['file'], str(request.POST['sin_number']))
                if upload_check:
                    logger.info('File Uploaded')
                    response = { 'message': 'File Uploaded To S3' }
                else:
                    logger.warn('Error Uploading File')
                    response = { 'message': 'Error Uploading File To S3' }

            else:
                if APP_ENV == "container":
                    logger.info('Saving File To Container File System')
                elif APP_ENV == "local":
                    logger.info('Saving File To Local File System')

                local_upload = request.FILES['file']
                sin = str(request.POST['sin_number'])
                save_file= LOCAL_SAVE_DIR + sin + '.pdf'
                with open(save_file,'wb+') as destination:
                    for chunk in local_upload.chunks():
                        destination.write(chunk)

                if APP_ENV == "container":
                    logger.info('File Uploaded To Container File System At /sinwebapp_1_container%s', save_file)
                    response = { 'message' : f"File Uploaded To Container File System At /sinwebapp_1_container{save_file}" }
                elif APP_ENV == "local":
                    logger.info('File Uploaded To Local File System At %s', save_file)
                    response = { 'message' : f"File Uploaded To Local File System At {save_file}" }

        else:
            logger.warn('Error Validating Form')
            response = { 'message' : 'Error Validating Form' }
    else:
        logger.warn("Request Attempted To Access /file/upload/ Without POST")
        response = { 'message': 'Upload Files Through POST method' }
    return JsonResponse(response, safe=False)

@login_required
def download_file(request):
    logger = DebugLogger("sinwebapp.files.views.upload_file").get_logger()
    logger.info('Downloading File')

@login_required
def list_files(request):
    logger = DebugLogger("sinwebapp.files.views.list_files").get_logger()
    logger.info('Retrieving File List')
    this_directory = os.path.dirname(os.path.abspath(__file__))

    if request.method == 'GET':
        if 'sin_number' in request.GET:
            sin_number = request.GET.get('sin_number')
            logger.info('Query Parameter Detected, Filtering List By Sin #: %s', sin_number)
            if APP_ENV == 'cloud':
                logger.info('Cloud Environment Detected')
                logger.info('Retrieving List From S3')
                response = list_for_sin(sin_number)
            else:
                if APP_ENV == 'container':
                    logger.info('Container Environment Detected')
                    logger.info('Retrieving File List From %s%s','/sinwebapp_web_1_container',this_directory)
                elif APP_ENV == 'local':
                    logger.info('Local Environment Detected')
                    logger.info('Retrieving File List From %s', this_directory)
                whole_file_list = os.listdir(os.path.join(this_directory,'local_uploads'))
                matched_list = {}
                index = 1             
                for f in whole_file_list:
                    if sin_number in f:
                        matched_list.update(index, f)
                        index+=1
                response = matched_list
        else:
            logger.info('No Query Parameters Detected, Listing All Files')
            if APP_ENV == 'cloud':
                logger.info('Cloud Environment Detected')
                logger.info('Retrieving List From S3')
                response = list_all()
            else:
                if APP_ENV == 'container':
                    logger.info('Container Environment Detected')
                    logger.info('Retrieving File List From %s%s','/sinwebapp_web_1_container',this_directory)
                elif APP_ENV == 'local':
                    logger.info('Local Environment Detected')
                    logger.info('Retrieving File List From %s', this_directory)

                response = os.listdir(os.path.join(this_directory,'local_uploads'))
    else:
        logger.info('Request Attempted To Access /file/list_files/ Without GET')
        response = { 'message': 'something went wrong'}
    
    return JsonResponse(response, safe=False)

@login_required
def delete_file(request):
    logger = DebugLogger("sinwebapp.files.views.delete_file").get_logger()
    logger.info('Deleting File From S3...')