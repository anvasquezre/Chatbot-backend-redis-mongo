from abc import ABC, abstractmethod
from typing import Any

from core.dtos.messages_dto import BaseMessageDto
from core.dtos.sessions_dto import SessionDto
from pydantic import BaseModel, Field


class SessionsHandlerBase(ABC, BaseModel):
    @abstractmethod
    def create_session(self) -> SessionDto:
        pass

    @abstractmethod
    def read_session(self, uuid: str) -> SessionDto:
        pass

    @abstractmethod
    def update_session(self, session: SessionDto) -> SessionDto:
        pass

    @abstractmethod
    def delete_session(self, uuid: str) -> SessionDto:
        pass

    @abstractmethod
    def append_message_to_session(
        self, uuid: str, message: BaseMessageDto
    ) -> SessionDto:
        pass

    @abstractmethod
    async def agenerate_response(self, text: str) -> Any:
        pass

    @abstractmethod
    async def aprocess_message(self, uuid: str, text: str) -> SessionDto:
        pass

    @classmethod
    @abstractmethod
    def create(cls, *args, **kwargs) -> "SessionsHandlerBase":
        pass
