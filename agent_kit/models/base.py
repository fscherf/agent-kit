from typing import Any
import os

from agent_kit.types import Message
from agent_kit.memory import Memory

SEPARATOR = "__"


class Model:
    def get_model_names(self):
        return []

    def add_message_to_memory(self, message: Message, memory: Memory):
        pass

    def get_tool_descriptions(self, tools: dict):
        pass

    def run(self, memory: Memory, tool_descriptions, think):
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.model_identifier!r})>"


def get_model_identifier():
    # TODO: add error logging

    from agent_kit.models.vendor_ollama import Ollama

    model_identifier = []

    # Ollama
    ollama_url = os.environ.get("OLLAMA_URL", "")

    if ollama_url:
        try:
            vendor = Ollama(
                host=ollama_url,
            )

            for model_name in vendor.get_model_names():
                model_identifier.append(
                    f"ollama-local{SEPARATOR}{model_name}",
                )

        except Exception:
            pass

    # Ollama Cloud
    ollama_cloud_api_key = os.environ.get("OLLAMA_CLOUD_API_KEY", "")

    try:
        vendor = Ollama(
            host="https://ollama.com",
            api_key=ollama_cloud_api_key,
        )

        for model_name in vendor.get_model_names():
            model_identifier.append(
                f"ollama-cloud{SEPARATOR}{model_name}",
            )

    except Exception:
        pass

    # finish
    return model_identifier


def get_model_by_identifier(model_identifier):
    # TODO: add error handling

    from agent_kit.models.vendor_ollama import Ollama

    vendor_identifier, model_name = model_identifier.split(SEPARATOR, 1)

    # Ollama
    if vendor_identifier == "ollama-local":
        model = Ollama(
            host=os.environ.get("OLLAMA_URL"),
        )

    # Ollama Cloud
    elif vendor_identifier == "ollama-cloud":
        model = Ollama(
            host="https://ollama.com",
            api_key=os.environ.get("OLLAMA_CLOUD_API_KEY"),
        )

    # finish
    model.identifier = model_identifier
    model.name = model_name

    return model
