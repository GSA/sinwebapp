import os

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from files.s3_manager import upload, download
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
                upload_check = upload(request.FILES['file'], request.POST['sin_number'])
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
    logger.info('Retrieving File From S3...')

@login_required
def delete_file(request):
    logger = DebugLogger("sinwebapp.files.views.delete_file").get_logger()
    logger.info('Deleting File From S3...')