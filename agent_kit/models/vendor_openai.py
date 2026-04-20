import inspect

from agent_kit.models.base import Model

from agent_kit.types import (
    ThinkingTokenEvent,
    OutputTokenEvent,
    ToolCallEvent,
    ToolCall,
)


class OpenAI(Model):
    def __init__(self, host, api_key):
        raise NotImplementedError()

    def get_model_names(self):
        raise NotImplementedError()

    def add_message_to_memory(self, message, memory):
        raise NotImplementedError()

    def get_tool_descriptions(self, tools):
        tool_descriptions = []

        # inspect tool
        for tool in tools.values():
            tool_name = tool.__name__

            tool_description = {
                "type": "function",
                "name": tool_name,
                "description": tool.__doc__,
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
                "required": [],
            }

            signature = inspect.signature(tool)

            for name, parameter in signature.parameters.items():
                parameter_description = {}

                # type
                if parameter.annotation is not inspect._empty:
                    parameter_description["type"] = (
                        parameter.annotation.__name__
                    )

                # required
                if parameter.default is not inspect._empty:
                    tool_description["required"].append(name)

                tool_description["parameters"][name] = parameter_description

            # register tool
            tool_description.append(tool_description)

        return tool_descriptions

    def run(self, memory, tool_descriptions, think):
        raise NotImplementedError()
