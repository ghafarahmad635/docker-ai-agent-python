from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from api.chat.model import ChatMessagePayload, ChatMessage, ChatMessagesRecent
from api.db import get_session
from typing import List
router = APIRouter()

@router.get("/")
def chat_health():
    """
    Health check endpoint to verify if the service is running.
    """
    return {"status": "ok"}

@router.post("/",response_model=ChatMessage)
def create_chat_message(
    payload: ChatMessagePayload,
    session:Session = Depends(get_session)
):
    data = payload.model_dump()
    print(f"Received chat message: {data['message']}")
    
    """
    Endpoint to create a new chat.
    """
    # Logic to create a chat would go here
    
    obj=ChatMessage.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return {"message": f"Chat created successfully {obj.message}", "id": obj.id, "is_response": obj.is_response}

# curl.exe http://localhost:8080/api/chats/recent

@router.get("/{recent}",response_model=List[ChatMessagesRecent])
def get_recent_chat_messages(
    session: Session = Depends(get_session),
):
    stmt = (
        select(ChatMessage)
        .order_by(ChatMessage.created_at.desc())
        .limit(10)
    )
    rows = session.exec(stmt).all()
    # model_validate replaces the old from_orm
    return [ChatMessagesRecent.model_validate(row) for row in rows]