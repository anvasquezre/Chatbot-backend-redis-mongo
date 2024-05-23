from enum import Enum

from core.dtos.base_dto import BaseDTO


class UserRoleEnum(str, Enum):
    HUMAN = "human"
    AI = "ai"
    SYSTEM = "system"


class MessageTypeEnum(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    FILE = "file"


class BaseMessageDto(BaseDTO):
    role: UserRoleEnum
    content: str
    type: MessageTypeEnum = MessageTypeEnum.TEXT


class HumanMessageDto(BaseMessageDto):
    role: UserRoleEnum = UserRoleEnum.HUMAN


class AIMessageDto(BaseMessageDto):
    role: UserRoleEnum = UserRoleEnum.AI


class SystemMessageDto(BaseMessageDto):
    role: UserRoleEnum = UserRoleEnum.SYSTEM


class GenerateRequestDto(BaseDTO):
    message: HumanMessageDto
