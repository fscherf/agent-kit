from typing import Literal, Any

from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    function_name: str
    function_arguments: list | dict


class ToolCallReturn(BaseModel):
    tool_call: ToolCall
    value: str = ""
    exception: Any | None = None  # FIXME


class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    thinking: str = ""
    content: str = ""
    tool_calls: list[ToolCall] = Field(default_factory=list)


# events
class ModelEvent(BaseModel):
    pass


# thinking
class ThinkingStartEvent(ModelEvent):
    pass


class ThinkingTokenEvent(ModelEvent):
    token: str


class ThinkingMessageEvent(ModelEvent):
    message: Message


# tool calls
class ToolCallEvent(ModelEvent):
    tool_call: ToolCall


class ToolCallReturnEvent(ModelEvent):
    tool_call_return: ToolCallReturn


# output
class OutputStartEvent(ModelEvent):
    pass


class OutputTokenEvent(ModelEvent):
    token: str


class OutputMessageEvent(ModelEvent):
    message: Message
