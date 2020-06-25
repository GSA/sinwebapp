import logging
from core import settings as config

LOGGER = logging.getLogger("DEBUG Settings.py DEBUG")
LOGGER.setLevel(logging.INFO)
ch = logging.StreamHandler()
format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setLevel(logging.INFO)
ch.setFormatter(format)
LOGGER.addHandler(ch)

def log_config():
    LOGGER.info("-------------------------------------------------")
    LOGGER.info('SETTINGS.PY Confgiruation')
    LOGGER.info("-------------------------------------------------")
    LOGGER.info("# Directory Location %s", config.BASE_DIR)
    LOGGER.info("-------------------------------------------------")
    LOGGER.info("# Application Environment")
    LOGGER.info('> ENVIRONMENT: %s', config.APP_ENV)
    LOGGER.info("-------------------------------------------------")
    LOGGER.info("# Database Configuration")
    LOGGER.info('> Database Host: %s', config.db_creds['host'])
    LOGGER.info('> Database Name: %s', config.db_creds['db_name'])
    LOGGER.info('> Database Username: %s', config.db_creds['username'])
    LOGGER.info("-------------------------------------------------")
    LOGGER.info("# UAA Configuratoin")
    LOGGER.info('> UAA_AUTH_URL: %s', config.UAA_AUTH_URL)
    LOGGER.info('> UAA_TOKEN_URL: %s', config.UAA_TOKEN_URL)

if __name__ == "__main__":
    log_config()