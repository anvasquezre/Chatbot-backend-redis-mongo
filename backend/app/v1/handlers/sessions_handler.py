from typing import Any, List

from app.v1.handlers.sessions_handler_base import SessionsHandlerBase
from core.dtos.messages_dto import AIMessageDto, BaseMessageDto, HumanMessageDto
from core.dtos.sessions_dto import SessionDto, SessionStatusEnum
from src.agents.agent_base import AgentBase
from src.agents.agent_langchain import LangchainAgent
from src.session_repository.sesion_repository_mongo import SessionRepositoryMongo
from src.session_repository.session_repository_base import SessionRepositoryBase
from src.session_repository.session_repository_redis import SessionRepositoryRedis


class SessionsHandler(SessionsHandlerBase):
    session_cache_repository: SessionRepositoryBase
    session_persistence_repository: SessionRepositoryBase
    agent: AgentBase

    def create_session(self) -> SessionDto:
        session = SessionDto()
        new_session = self.session_cache_repository.save(session)
        return new_session

    def save_session(self, session: SessionDto) -> SessionDto:
        session.status = SessionStatusEnum.INACTIVE
        saved_session = self.session_persistence_repository.save(session=session)
        return saved_session

    def read_session(self, uuid: str) -> SessionDto:
        session = self.session_cache_repository.read(uuid)
        return session

    def update_session(self, session: SessionDto) -> SessionDto:
        updated_session = self.session_cache_repository.update(session)
        return updated_session

    def delete_session(self, uuid: str) -> SessionDto:
        deleted_session = self.session_cache_repository.delete(uuid)
        self.save_session(session=deleted_session)
        return deleted_session

    async def aprocess_message(self, uuid: str, text: str) -> SessionDto:
        session_data = self.read_session(uuid=uuid)
        new_message = HumanMessageDto(content=text)
        self.append_message_to_session(uuid=uuid, message=new_message)
        message_history = session_data.messages
        response = await self.agenerate_response(
            text=text, message_history=message_history
        )
        message = AIMessageDto(content=response)
        updated_session = self.append_message_to_session(uuid=uuid, message=message)
        return updated_session

    async def agenerate_response(
        self, text: str, message_history: List[BaseMessageDto]
    ) -> str:
        response = await self.agent.aexecute(text=text, message_history=message_history)
        return response

    def append_message_to_session(
        self, uuid: str, message: BaseMessageDto
    ) -> SessionDto:
        session = self.session_cache_repository.read(uuid)
        session.messages.append(message)
        updated_session = self.session_cache_repository.update(session)
        return updated_session

    @classmethod
    def create(cls) -> "SessionsHandlerBase":
        session_cache_repository = SessionRepositoryRedis.create()
        session_persistence_repository = SessionRepositoryMongo.create()
        agent = LangchainAgent.create()
        return cls(
            session_cache_repository=session_cache_repository,
            session_persistence_repository=session_persistence_repository,
            agent=agent,
        )
