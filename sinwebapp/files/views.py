import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from files.forms import UploadFileForm
from core.settings import APP_ENV, BASE_DIR
from debug import DebugLogger

from files.s3_manager import upload, download

SAVE_DIR=BASE_DIR+'/files/local_uploads/'

@login_required
def upload_file(request):
    logger = DebugLogger("sinwebapp.files.views.upload_file").get_logger()
    logger.info('Posting File Form To S3...')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            logger.info('Form Validated')
            if APP_ENV == "cloud":
                upload_check = upload(request.FILES['file'], request.FILES['sin_number'])
                if upload_check:
                    logger.info('File Uploaded')
                    response = { 'message': 'File Uploaded'}
                else:
                    logger.warn('Error Uploading File')
                    response = { 'message': 'Error Uploading File'}
            else:
                logger.info('Saving File To Local Filesystem')
                local_upload = request.FILES['file']
                sin = request.FILES['sin_number']
                filename, fileext = os.path.splitext(local_upload)
                save_file= SAVE_DIR + sin + fileext
                with open('new_name','wb+') as destination:
                    for chunk in local_upload.chunks():
                        destination.write(chunk)
        else:
            logger.warn('Error Validating Form')
            response = { 'message' : 'Error Validating Form'}

@login_required
def download_file(request):
    logger = DebugLogger("sinwebapp.files.views.upload_file").get_logger()
    logger.info('Retrieving File From S3...')

@login_required
def delete_file(request):
    logger = DebugLogger("sinwebapp.files.views.delete_file").get_logger()
    logger.info('Deleting File From S3...')