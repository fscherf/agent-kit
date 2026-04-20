import sys

from agent_kit.types import (
    ThinkingMessageEvent,
    ToolCallReturnEvent,
    OutputMessageEvent,
    ThinkingStartEvent,
    ThinkingTokenEvent,
    OutputStartEvent,
    OutputTokenEvent,
    ToolCallReturn,
    ToolCallEvent,
    ModelEvent,
    Message,
)


class Agent:
    def __init__(self, harness, model, memory, interface):
        self.harness = harness
        self.model = model
        self.memory = memory
        self.interface = interface

        self._tool_descriptions = None

    def _get_tool_descriptions(self):
        if self._tool_descriptions is None:
            self._tool_descriptions = self.model.get_tool_descriptions(
                tools=self.harness.get_tools(),
            )

        return self._tool_descriptions

    def run(self):

        # system prompt
        if self.memory.is_empty():
            system_prompt_message = Message(
                role="system",
                content=self.interface.get_system_prompt(),
            )

            self.model.add_message_to_memory(
                message=system_prompt_message,
                memory=self.memory,
            )

        # user prompt
        user_prompt_message = Message(
            role="user",
            content=self.interface.get_user_prompt(
                agent=self,
            ),
        )

        self.model.add_message_to_memory(
            message=user_prompt_message,
            memory=self.memory,
        )

        # main loop
        for step in range(sys.maxsize):

            # setup state
            thinking = False
            outputting = False
            waiting_for_tool_call = False

            # setup buffer
            thinking_message_buffer = ""
            output_message_buffer = ""

            for event in self.model.run(
                    memory=self.memory,
                    tool_descriptions=self._get_tool_descriptions(),
                    think=self.interface.get_think(),
            ):

                if not isinstance(event, ModelEvent):
                    raise TypeError()

                # thinking events
                if thinking:

                    # thinking token
                    if isinstance(event, ThinkingTokenEvent):
                        thinking_message_buffer += event.token

                        self.interface.handle_thinking_token(event=event)

                    # thinking message
                    else:
                        thinking_message = Message(
                            role="assistant",
                            thinking=thinking_message_buffer,
                        )

                        self.model.add_message_to_memory(
                            message=thinking_message,
                            memory=self.memory,
                        )

                        self.interface.handle_thinking_message(
                            event=ThinkingMessageEvent(
                                message=thinking_message,
                            ),
                        )

                        thinking_message_buffer = ""
                        thinking = False

                # thinking start
                elif isinstance(event, ThinkingTokenEvent):
                    thinking_message_buffer += event.token

                    self.interface.handle_thinking_start(
                        event=ThinkingStartEvent(),
                    )

                    self.interface.handle_thinking_token(event=event)

                    thinking = True

                # output events
                if outputting:

                    # output token
                    if isinstance(event, OutputTokenEvent):
                        output_message_buffer += event.token

                        self.interface.handle_output_token(event=event)

                    # output message
                    else:
                        output_message = Message(
                            role="assistant",
                            content=thinking_message_buffer,
                        )

                        self.model.add_message_to_memory(
                            message=output_message,
                            memory=self.memory,
                        )

                        self.interface.handle_output_message(
                            event=OutputMessageEvent(
                                message=output_message,
                            ),
                        )

                        output_message_buffer = ""
                        outputting = False

                # output start
                elif isinstance(event, OutputTokenEvent):
                    output_message_buffer += event.token

                    self.interface.handle_output_start(
                        event=OutputStartEvent(),
                    )

                    self.interface.handle_output_token(event=event)

                    outputting = True

                # tool call events
                if isinstance(event, ToolCallEvent):

                    # tool call
                    tool_call_message = Message(
                        role="assistant",
                        tool_calls=[
                            event.tool_call,
                        ],
                    )

                    self.model.add_message_to_memory(
                        message=tool_call_message,
                        memory=self.memory,
                    )

                    self.interface.handle_tool_call(event=event)

                    # run tool
                    value, exception = self.harness.handle_tool_call(
                        function_name=event.tool_call.function_name,
                        function_arguments=event.tool_call.function_arguments,
                    )

                    waiting_for_tool_call = True

                    # tool call return
                    tool_call_return = ToolCallReturn(
                        tool_call=event.tool_call,
                        value=value,
                        exception=exception,
                    )

                    tool_call_return_event = ToolCallReturnEvent(
                        tool_call_return=tool_call_return,
                    )

                    tool_call_return_message = Message(
                        role="tool",
                        content=value,
                    )

                    self.model.add_message_to_memory(
                        message=tool_call_return_message,
                        memory=self.memory,
                    )

                    self.interface.handle_tool_call_return(
                        event=tool_call_return_event,
                    )

            # flush thinking buffer
            if thinking and thinking_message_buffer:
                thinking_message = Message(
                    role="assistant",
                    thinking=thinking_message_buffer,
                )

                self.model.add_message_to_memory(
                    message=thinking_message,
                    memory=self.memory,
                )

                self.interface.handle_thinking_message(
                    event=ThinkingMessageEvent(
                        message=thinking_message,
                    ),
                )

            # flush output buffer
            if outputting and output_message_buffer:
                output_message = Message(
                    role="assistant",
                    content=thinking_message_buffer,
                )

                self.model.add_message_to_memory(
                    message=output_message,
                    memory=self.memory,
                )

                self.interface.handle_output_message(
                    event=OutputMessageEvent(
                        message=output_message,
                    ),
                )

            if self.interface.should_stop(step):
                return False

            if not waiting_for_tool_call:
                return True
