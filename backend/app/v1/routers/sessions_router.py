from app.v1.handlers.sessions_handler import SessionsHandler
from core.dtos.messages_dto import BaseMessageDto
from core.dtos.sessions_dto import SessionDto
from fastapi import APIRouter

router = APIRouter(prefix="/sessions", tags=["sessions", "v1"])


@router.get("/", response_model=SessionDto)
async def create_session() -> SessionDto:
    sessions_handler = SessionsHandler.create()
    response = sessions_handler.create_session()
    return response


@router.get("/end/{session_id}", response_model=SessionDto)
async def end_session(session_id: str) -> SessionDto:
    sessions_handler = SessionsHandler.create()
    response = sessions_handler.delete_session(uuid=session_id)
    return response


@router.post("/{session_id}", response_model=SessionDto)
async def generate_message(session_id: str, message: BaseMessageDto) -> SessionDto:
    text = message.content
    sessions_handler = SessionsHandler.create()
    response = await sessions_handler.aprocess_message(uuid=session_id, text=text)
    return response
