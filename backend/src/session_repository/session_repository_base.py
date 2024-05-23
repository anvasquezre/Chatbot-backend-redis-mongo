from abc import ABC, abstractmethod

from core.dtos.sessions_dto import SessionDto
from pydantic import BaseModel, Field


class SessionRepositoryBase(ABC, BaseModel):
    @abstractmethod
    def read(self, uuid: str) -> SessionDto:
        pass

    @abstractmethod
    def update(self, session: SessionDto) -> SessionDto:
        pass

    @abstractmethod
    def delete(self, uuid: str) -> SessionDto:
        pass

    @abstractmethod
    def save(self, session: SessionDto) -> SessionDto:
        pass

    @classmethod
    @abstractmethod
    def create(cls) -> "SessionRepositoryBase":
        pass
