from urllib.parse import urlencode
from django.http.request import HttpRequest
from . import settings
import logging


class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.configure_logging()

    def __call__(self, request: HttpRequest):
        path=request.path

        if settings.DEBUG:
            self.LOGGER.info('Intercepted Request Path: %s', path)
            
            if path == '/auth/callback':
                self.LOGGER.info('Detected OAuth Callback...')
                self.LOGGER.info('OAuth CallBack Code Parameter: %s', request.GET.get('code'))
                self.LOGGER.info('OAuth CallBack State Parameter %s', request.GET.get('state'))
                
        response = self.get_response(request)

        return response

    def configure_logging(self):
        self.LOGGER = logging.getLogger("DEBUG DebugMiddleware DEBUG")
        self.LOGGER.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setLevel(logging.INFO)
        ch.setFormatter(format)
        self.LOGGER.addHandler(ch) 