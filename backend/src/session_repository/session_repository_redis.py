import json

from core.dtos.sessions_dto import SessionDto
from pydantic import ConfigDict
from src.session_repository.session_repository_base import SessionRepositoryBase
from utils.settings import settings

from redis import Redis


class SessionRepositoryRedis(SessionRepositoryBase):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    redis_client: Redis

    def read(self, uuid: str) -> SessionDto:
        session_dict = self.redis_client.hgetall(uuid)
        for key, value in session_dict.items():
            try:
                session_dict[key] = json.loads(value)
            except json.JSONDecodeError:
                pass
        return SessionDto(**session_dict)

    def update(self, session: SessionDto) -> SessionDto:
        self.save(session)
        return session

    def delete(self, uuid: str) -> SessionDto:
        session = self.read(uuid)
        self.redis_client.delete(uuid)
        return session

    def save(self, session: SessionDto) -> SessionDto:
        session_dict = session.model_dump()
        for key, value in session_dict.items():
            if isinstance(value, list):
                session_dict[key] = json.dumps(value)
        self.redis_client.hset(session.uuid, mapping=session_dict)
        self.redis_client.expire(session.uuid, 3600)  # renew TTL
        return session

    @classmethod
    def create(cls) -> "SessionRepositoryRedis":
        redis_client = Redis(
            host=settings.REDIS.REDIS_HOST,
            port=settings.REDIS.REDIS_PORT,
            db=settings.REDIS.REDIS_DB,
            decode_responses=True,
        )
        return cls(redis_client=redis_client)
