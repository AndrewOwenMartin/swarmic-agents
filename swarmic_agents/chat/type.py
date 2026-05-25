from enum import Enum
from typing import Any, Literal, Optional, Union
from pydantic import BaseModel


class ChatInput(BaseModel):
    type: Literal["text", "image"]
    content: str


class ChatOutputMessage(BaseModel):
    type: Literal["message"]
    content: str


class ChatOutputReasoning(BaseModel):
    type: Literal["reasoning"]
    content: str


class ChatOutputToolCall(BaseModel):
    type: Literal["tool_call"]
    tool: str
    arguments: dict
    output: str
    provider_info: dict


class ChatOutputChunkType(Enum):
    TOOL_CALL = "tool_call"
    MESSAGE = "message"
    REASONING = "reasoning"


class ChatOutputChunk(BaseModel):
    type: ChatOutputChunkType
    content: dict

    @classmethod
    def factory(cls, json_dict: dict) -> "ChatOutputChunk":
        chunk_type = json_dict.pop("type")
        return ChatOutputChunk(type=chunk_type, content=json_dict)

    def parse(self):
        if self.type == ChatOutputChunkType.TOOL_CALL:
            return ChatOutputToolCall.model_validate(self.content)
        elif self.type == ChatOutputChunkType.MESSAGE:
            return ChatOutputMessage.model_validate(self.content)
        elif self.type == ChatOutputChunkType.REASONING:
            return ChatOutputReasoning.model_validate(self.content)
        else:
            raise ValueError(f"Unknown chunk type: {self.type}")


class ChatResponseErrorInfo(BaseModel):
    message: str
    type: str
    code: str
    param: str


class ChatResponseError(BaseModel):
    error: ChatResponseErrorInfo


class ChatResponse(BaseModel):
    model_instance_id: str
    output: list[Union[ChatOutputMessage, ChatOutputReasoning, ChatOutputToolCall]]
    stats: dict[str, Any]
    response_id: Optional[str] = None


class ChatRequest(BaseModel):
    model: str
    input: list[ChatInput]
    system_prompt: Optional[str] = None
    integrations: Optional[list[Any]] = None
    reasoning: Literal["off", "on"] = "off"
    store: bool = False
    stream: Optional[bool] = False


class ChatError(Exception):
    pass
