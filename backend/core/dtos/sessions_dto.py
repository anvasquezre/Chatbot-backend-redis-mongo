import time
import uuid
from enum import Enum

from core.dtos.base_dto import BaseDTO
from core.dtos.messages_dto import BaseMessageDto
from pydantic import Field, field_serializer


class SessionStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class SessionDto(BaseDTO):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: float = Field(default_factory=lambda: int(time.time()))
    status: SessionStatusEnum = SessionStatusEnum.ACTIVE
    messages: list[BaseMessageDto] = []
