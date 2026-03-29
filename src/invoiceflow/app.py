import logging

from invoiceflow.config.settings import settings
from invoiceflow.config.logger import setup_logging

logger = logging.getLogger(__name__)

def run():
    setup_logging()

    logger.info("starting invoiceflow...")
    logger.info("invoiceflow live")


if __name__ == "__main__":
    run()