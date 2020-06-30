from urllib.parse import urlencode
from django.http.request import HttpRequest
from . import settings
import logging, re
from debug import DebugLogger

class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.dl=DebugLogger("core.middleware.DebugMiddleware")
        self.logger=dl.get_logger()

    def __call__(self, request: HttpRequest):

        if settings.DEBUG:
            self.logger.info('> Request Path: %s', request.path)
            self.logger.info('> Request Host: %s', request.META["HTTP_HOST"])

            for key, value in request.GET.items():
                self.logger.info('>> Request Parameter %s = %s', key, value)

            for key, value in request.session.items():
                if value is not None:
                    self.logger.info('>>> Session Variable %s = %s', key, value)
   
        response = self.get_response(request)

        return response