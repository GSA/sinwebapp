from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from files.forms import UploadFileForm

from debug import DebugLogger

@login_required
def upload_file(request):
    logger = DebugLogger("sinwebapp.files.views.upload_file").get_logger()
    logger.info('Posting File Form To S3...')
    if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                logger.info('Form Validated')
                # TODO: upload to S3
                pass
            else:
                logger.info('Form Not Validated')

@login_required
def download_file(request):
    logger = DebugLogger("sinwebapp.files.views.upload_file").get_logger()
    logger.info('Retrieving File From S3...')
