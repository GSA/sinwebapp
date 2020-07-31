import logging
from core import settings as config

class DebugLogger():

    def __init__(self, location_name):
        self.logger = self.init_logger(location_name)

    def init_logger(self, location_name):
        this_logger = logging.getLogger(location_name)
        this_logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setLevel(logging.INFO)
        ch.setFormatter(format)
        this_logger.addHandler(ch)
        return this_logger

    def get_logger(self):
        return self.logger
        
    def log_settings(self):
        self.logger.info("-------------------------------------------------")
        self.logger.info('SETTINGS.PY Configuration')
        self.logger.info("-------------------------------------------------")
        self.logger.info("# Main Configuration")
        self.logger.info("> Directory Location : %s", config.BASE_DIR)
        self.logger.info('> Debug : %s', config.DEBUG)
        self.logger.info('> Enviroment: %s', config.APP_ENV)
        self.logger.info("-------------------------------------------------")
        self.logger.info("# Database Configuration")
        self.logger.info('> Database Host: %s', config.db_creds['host'])
        self.logger.info('> Database Name: %s', config.db_creds['db_name'])
        self.logger.info('> Database Username: %s', config.db_creds['username'])
        self.logger.info("-------------------------------------------------")
        self.logger.info("# UAA OAuth2 Configuration")
        self.logger.info('> UAA_AUTH_URL: %s', config.UAA_AUTH_URL)
        self.logger.info('> UAA_TOKEN_URL: %s', config.UAA_TOKEN_URL)
        self.logger.info('> LOGIN_REDIRECT_URL : %s', config.LOGIN_REDIRECT_URL)
        self.logger.info("-------------------------------------------------")
        self.logger.info("# Miscellanous Configuration")
        self.logger.info('> CSRF_HEADER_NAME: %s', config.CSRF_HEADER_NAME)
        self.logger.info("-------------------------------------------------")

if __name__ == "__main__":
    logger = DebugLogger("debug.py")
    logger.log_settings()