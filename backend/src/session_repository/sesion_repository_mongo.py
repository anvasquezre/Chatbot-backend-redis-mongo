from core.dtos.sessions_dto import SessionDto
from pydantic import ConfigDict
from pymongo import MongoClient
from src.session_repository.session_repository_base import SessionRepositoryBase
from utils.settings import settings


class SessionRepositoryMongo(SessionRepositoryBase):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    mongo_client: MongoClient
    sessions_collection: str
    db_name: str

    def read(self, uuid: str) -> SessionDto:
        with self.mongo_client.start_session() as mongo_session:
            db = mongo_session.client[self.db_name]
            session = db[self.sessions_collection].find_one({"uuid": uuid})
        return SessionDto(**session)

    def update(self, session: SessionDto) -> SessionDto:
        self.save(session)
        return session

    def delete(self, uuid: str) -> SessionDto:
        with self.mongo_client.start_session() as mongo_session:
            db = mongo_session.client[self.db_name]
            session = db[self.sessions_collection].find_one_and_delete({"uuid": uuid})
        return SessionDto(**session)

    def save(self, session: SessionDto) -> SessionDto:
        with self.mongo_client.start_session() as mongo_session:
            db = mongo_session.client[self.db_name]
            db[self.sessions_collection].update_one(
                {"uuid": session.uuid},
                {"$set": session.model_dump()},
                upsert=True,
            )
        return session

    @classmethod
    def create(cls) -> "SessionRepositoryMongo":
        mongo_client = MongoClient(
            host=settings.MONGODB.MONGO_HOST,
            port=settings.MONGODB.MONGO_PORT,
            username=settings.MONGODB.MONGO_USER,
            password=settings.MONGODB.MONGO_PASSWORD.get_secret_value(),
            authSource=settings.MONGODB.MONGO_AUTH_DB,
        )
        sessions_collection = settings.MONGODB.MONGO_SESSIONS_COLLECTION
        db = settings.MONGODB.MONGO_DB
        return cls(
            mongo_client=mongo_client,
            sessions_collection=sessions_collection,
            db_name=db,
        )
