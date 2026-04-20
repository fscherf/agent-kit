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


class Interface:
    def __init__(
            self,
            system_prompt="",
            user_prompt="",
            think=True,
            max_steps=10,
    ):

        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.think = think
        self.max_steps = max_steps

    def should_stop(self, step):
        return step + 1 >= self.max_steps

    def get_think(self):
        return self.think

    # prompts
    def get_system_prompt(self):
        return self.system_prompt

    def get_user_prompt(self):
        return self.user_prompt

    # thinking
    def handle_thinking_start(self, event: ThinkingStartEvent):
        pass

    def handle_thinking_token(self, event: ThinkingTokenEvent):
        pass

    def handle_thinking_message(self, event: ThinkingMessageEvent):
        pass

    # tool calls
    def handle_tool_call(self, event: ToolCallEvent):
        pass

    def handle_tool_call_return(self, event: ToolCallReturnEvent):
        pass

    # output
    def handle_output_start(self, event: OutputStartEvent):
        pass

    def handle_output_token(self, event: OutputTokenEvent):
        pass

    def handle_output_message(self, event: OutputMessageEvent):
        pass
