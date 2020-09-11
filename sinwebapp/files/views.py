from django.shortcuts import render

from files.forms import UploadFileForm

from debug import DebugLogger


def upload_file(request):
    logger = DebugLogger("sinwebapp.files.views.upload_file").get_logger()
    logger.info('Posting File Form...')
    if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                logger.info('Form Validated')
                # TODO: upload to S3
                pass
            else:
                logger.info('Form Not Validated')
