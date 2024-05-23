from pydantic import ConfigDict, SecretStr
from pydantic_settings import BaseSettings
from utils.custom_logger import CustomLogger


class CoreSettings(BaseSettings):
    model_config = ConfigDict(extra="forbid")


class MongoDBSettings(CoreSettings):
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017
    MONGO_DB: str = "chatbot"
    MONGO_USER: str = "root"
    MONGO_PASSWORD: SecretStr = "secret"
    MONGO_AUTH_DB: str = "admin"
    MONGO_SESSIONS_COLLECTION: str = "sessions"


class RedisSettings(CoreSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: SecretStr = ""
    REDIS_EXPIRE: int = 3600


class WeatherApiSettings(CoreSettings):
    API_KEY: SecretStr


class OpenAISettings(CoreSettings):
    OPENAI_API_KEY: SecretStr


class Settings(CoreSettings):
    MONGODB: MongoDBSettings = MongoDBSettings()
    REDIS: RedisSettings = RedisSettings()
    WEATHER_API: WeatherApiSettings = WeatherApiSettings()
    OPENAI: OpenAISettings = OpenAISettings()


settings = (
    Settings()
)  # This will load the settings from the environment variables, not from the .env file

logger = CustomLogger("Settings")
logger.info("Settings loaded.")
logger.debug(f"Settings: {settings.model_dump()}")
