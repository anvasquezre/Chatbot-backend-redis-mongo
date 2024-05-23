from abc import ABC, abstractmethod
from typing import List

from core.dtos.messages_dto import BaseMessageDto
from pydantic import BaseModel, Field


class AgentBase(ABC, BaseModel):
    @abstractmethod
    def execute(self, text: str, message_history: List[BaseMessageDto]) -> str:
        pass

    @abstractmethod
    async def aexecute(self, text: str, message_history: List[BaseMessageDto]) -> str:
        pass

    @classmethod
    @abstractmethod
    def create(cls, *args, **kwargs) -> "AgentBase":
        pass
