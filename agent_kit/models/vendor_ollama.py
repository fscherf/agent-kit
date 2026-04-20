from ollama import Client

from agent_kit.models.base import Model

from agent_kit.types import (
    ThinkingTokenEvent,
    OutputTokenEvent,
    ToolCallEvent,
    ToolCall,
)


class Ollama(Model):
    def __init__(self, host, api_key="ollama"):
        self.identifier = ""
        self.model = ""

        self.client = Client(
            host=host,
            headers={
                "Authorization": f"Bearer {api_key}",
            },
        )

    def get_model_names(self):
        models = {}

        for model in self.client.list()["models"]:
            models[str(model.model)] = dict(model)

        return models

    def add_message_to_memory(self, message, memory):
        tool_calls = []

        for tool_call in message.tool_calls:
            tool_calls.append({
                "function": {
                    "name": tool_call.function_name,
                    "arguments": tool_call.function_arguments,
                },
            })

        memory.add_message({
            "role": message.role,
            "thinking": message.thinking,
            "content": message.content,
            "tool_calls": tool_calls,
        })

    def get_tool_descriptions(self, tools):
        return tools.values()

    def run(self, memory, tool_descriptions, think):
        stream = self.client.chat(
            model=self.name,
            messages=memory.get_context(),
            tools=tool_descriptions,
            stream=True,
            think=think,
        )

        for chunk in stream:

            # thinking
            if chunk.message.thinking:
                yield ThinkingTokenEvent(
                    token=chunk.message.thinking,
                )

            # tool calls
            elif chunk.message.tool_calls:
                for tool_call in chunk.message.tool_calls:
                    yield ToolCallEvent(
                        tool_call=ToolCall(
                            function_name=tool_call.function.name,
                            function_arguments=tool_call.function.arguments,
                        ),
                    )

            # output
            elif chunk.message.content:
                yield OutputTokenEvent(
                    token=chunk.message.content,
                )
