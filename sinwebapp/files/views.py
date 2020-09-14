import os
import mimetypes

from django.shortcuts import render
from django.http import FileResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from files.s3_manager import upload, download, list_for_sin, list_all
from files.forms import UploadFileForm
from core.settings import APP_ENV, BASE_DIR
from debug import DebugLogger

LOCAL_SAVE_DIR=os.path.join(BASE_DIR,'files','local_uploads')

@login_required
def upload_file(request):
    logger = DebugLogger("sinwebapp.files.views.upload_file").get_logger()
    logger.info('Posting File Form')
    logger.info('Mimetype Guess: %s', mimetypes.guess_extension(request.FILES['file']))
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        logger.info()

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
                save_file=os.path.join(LOCAL_SAVE_DIR,f"{sin}.pdf")
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
    logger.info('Downloading File From Environment')

    if APP_ENV == 'container':
        logger.info('Container Environment Detected')
        logger.info('Retrieving File From %s%s','/sinwebapp_web_1_container', LOCAL_SAVE_DIR)
    elif APP_ENV == 'local':
        logger.info('Local Environment Detected')
        logger.info('Retrieving File From %s', LOCAL_SAVE_DIR)
    elif APP_ENV == 'cloud':
        logger.info('Cloud Environment Detected')
        logger.info('Retrieving File From S3')

    if request.method == 'GET':
        if 'sin_number' in request.GET:
            sin_number = request.GET.get('sin_number')
            if APP_ENV == 'cloud':
                s3_file = download(sin_number)['Body']
                response = FileResponse(s3_file, as_attachment=True, filename=f"{sin_number}.pdf")
                response['Content-Type'] = 'application/pdf'
            else:
                local_file_path = os.path.join(LOCAL_SAVE_DIR,f"{sin_number}.pdf")
                response = FileResponse(open(local_file_path, 'rb'))
        else:
            logger.warn('No Query Parameter Provided')
            response = { 'message': 'No Query Parameter Provided'}
    else:
        logger.warn('Request Attempted To Access /files/download/ Without GET')
        response = { 'message': 'Request Attempted To Access /files/download/ Without GET'}

    return response

@login_required
def list_files(request):
    logger = DebugLogger("sinwebapp.files.views.list_files").get_logger()
    logger.info('Retrieving File List From Environment')

    if APP_ENV == 'container':
        logger.info('Container Environment Detected')
        logger.info('Retrieving File List From %s%s','/sinwebapp_web_1_container', LOCAL_SAVE_DIR)
    elif APP_ENV == 'local':
        logger.info('Local Environment Detected')
        logger.info('Retrieving File List From %s', LOCAL_SAVE_DIR)
    elif APP_ENV == 'cloud':
        logger.info('Cloud Environment Detected')
        logger.info('Retrieving File List From S3')

    if request.method == 'GET':
        if 'sin_number' in request.GET:
            sin_number = request.GET.get('sin_number')
            logger.info('Query Parameter Detected, Filtering List By Sin #: %s', sin_number)

            if APP_ENV == 'cloud':
                raw_list = list_for_sin(sin_number)
                response = []
                index = 1

                for item in raw_list:
                    response.append({"index": index, "filename": f"{item['Key']}.pdf"})
                    index+=1
            else:
                whole_file_list = os.listdir(LOCAL_SAVE_DIR)
                response = []
                index = 1             

                for item in whole_file_list:
                    if sin_number in item:
                        response.append({"index": index, "filename": item})
                        index+=1

        else:
            logger.info('No Query Parameters Detected, Listing All Files')
            if APP_ENV == 'cloud':
                logger.info('Cloud Environment Detected')
                logger.info('Retrieving List From S3')
                raw_list= list_all()
                response = []
                index = 1
                for item in raw_list:
                    response.append({"index": index, "filename": item})
                    index+=1
            else:
                if APP_ENV == 'container':
                    logger.info('Container Environment Detected')
                    logger.info('Retrieving File List From %s%s','/sinwebapp_web_1_container', LOCAL_SAVE_DIR)
                elif APP_ENV == 'local':
                    logger.info('Local Environment Detected')
                    logger.info('Retrieving File List From %s', LOCAL_SAVE_DIR)

                response = os.listdir(LOCAL_SAVE_DIR)
    else:
        logger.info('Request Attempted To Access /files/list/ Without GET')
        response = { 'message': 'something went wrong'}
    
    return JsonResponse(response, safe=False)

@login_required
def delete_file(request):
    logger = DebugLogger("sinwebapp.files.views.delete_file").get_logger()
    logger.info('Deleting File From S3...')