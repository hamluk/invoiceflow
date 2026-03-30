import logging

from openai import OpenAI

logger = logging.getLogger(__name__)


def init_openai_client(api_key: str) -> OpenAI:
    logger.info("Initialize openai client")
    return OpenAI(api_key=api_key)
