import logging
from pathlib import Path

import yaml
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ChatModelPrompt(BaseModel):
    system: str
    user: str


def load_prompt_messages(prompt_files_path: str, version: str) -> ChatModelPrompt:
    """
    Loads system and user prompt from a yaml file.

    :param prompt_files_path: path to the prompt folder holding the yaml files
    :param version: version number of the prompt
    :return: loaded system and user prompt from the file
    """
    logger.info(f"loading prompts from version file {version}.yaml")
    path = Path(f"{prompt_files_path}/{version}.yaml")

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return ChatModelPrompt(
        system=data["system"],
        user=data["user"]
    )