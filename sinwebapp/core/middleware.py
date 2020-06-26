from urllib.parse import urlencode
from django.http.request import HttpRequest
from . import settings
import logging, re
from debug import DebugLogger

class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = DebugLogger("DebugMiddleware").get_logger()

    def __call__(self, request: HttpRequest):
        path=request.path

        if settings.DEBUG:
            self.logger.info("-------------------------------------------------")
            self.logger.info('Intercepted Request Path: %s', path)
            
            if re.search('auth.+', path):
                self.logger.info('Detected OAuth Request/Callback...')
                for key, value in request.session.items():
                    if value is not None:
                        self.logger.info('...Session Variable %s : %s', key, value)
                self.logger.info('Next URL: %s', request.GET.get('next', ''))
                self.logger.info('OAuth CallBack Code Parameter: %s', request.GET.get('code'))
                self.logger.info('OAuth CallBack State Parameter %s', request.GET.get('state'))
                
        response = self.get_response(request)

        return response