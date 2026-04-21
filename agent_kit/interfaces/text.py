import readline
import textwrap
import pprint
import json
import os

from agent_kit.interfaces.base import Interface
from agent_kit.terminal import color

from agent_kit.types import (
    ThinkingStartEvent,
    ThinkingTokenEvent,
    ThinkingMessageEvent,
    ToolCallEvent,
    ToolCallReturnEvent,
    OutputStartEvent,
    OutputTokenEvent,
    OutputMessageEvent,
)


class TextInterface(Interface):
    HISTORY_FILE = "~/.agent-kit.history"
    HISTORY_SIZE = 1000

    # prompt
    def read_history(self):
        self.history = []
        readline.clear_history()

        try:
            abs_history_path = os.path.expanduser(self.HISTORY_FILE)

            for line in open(abs_history_path, "r"):
                item = json.loads(line)
                self.add_to_history(item)

        except Exception:
            pass

    def write_history(self):
        try:
            abs_history_path = os.path.expanduser(self.HISTORY_FILE)

            with open(abs_history_path, 'w+') as f:
                for item in self.history:
                    f.write(json.dumps(item) + '\n')

        except Exception:
            pass

    def add_to_history(self, item):
        # skip duplicates
        if self.history and item == self.history[-1]:
            return

        self.history.append(item)

        # rotate
        self.history = self.history[self.HISTORY_SIZE*-1:]
        readline.clear_history()

        for item in self.history:
            readline.add_history(item)

        self.write_history()

    def get_user_prompt(self, agent):
        if not hasattr(self, "history"):
            self.read_history()

        while True:
            prompt = input(color(f"{agent.model.name} > ", "bold-green"))

            if prompt.strip():
                break

        self.add_to_history(prompt)

        return prompt

    # thinking
    def handle_thinking_start(self, event: ThinkingStartEvent):
        print()

    def handle_thinking_token(self, event: ThinkingTokenEvent):
        print(color(event.token, "grey"), end="")

    def handle_thinking_message(self, event: ThinkingMessageEvent):
        print()

    # tool calls
    def handle_tool_call(self, event: ToolCallEvent):
        function_name = event.tool_call.function_name
        function_arguments = event.tool_call.function_arguments
        function_arguments_string = ""

        if isinstance(function_arguments, list):
            function_arguments_string = ", ".join([
                repr(value) for value in function_arguments
            ])

        else:
            function_arguments_string = ", ".join([
                f"{key}={repr(value)}"
                for key, value in function_arguments.items()
            ])

        print()
        print(f"    >>> {function_name}({function_arguments_string})")

    def handle_tool_call_return(self, event: ToolCallReturnEvent):
        if event.tool_call_return.exception:
            exception_string = repr(event.tool_call_return.exception)

            print(color(f"    {exception_string}", "bold-red"))

        else:
            try:
                return_value_string = textwrap.indent(
                    pprint.pformat(
                        json.loads(event.tool_call_return.value),
                    ),
                    prefix="    ",
                )

            except Exception:
                return_value_string = repr(event.tool_call_return.value)

            print(return_value_string)

    # output
    def handle_output_start(self, event: OutputStartEvent):
        print()

    def handle_output_token(self, event: OutputTokenEvent):
        print(event.token, end="")

    def handle_output_message(self, event: OutputMessageEvent):
        print("\n")
