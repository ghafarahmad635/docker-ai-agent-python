from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from api.chat.model import AIChatResponse, ChatMessagePayload, ChatMessage, ChatMessagesRecent, ChatMessagesWithResponse
from api.db import get_session
from typing import List
from api.ai.services import generate_email_message
from api.ai.schema import EmailMessageSchema
from sqlalchemy.orm   import selectinload


router = APIRouter()

@router.get("/")
def chat_health():
    """
    Health check endpoint to verify if the service is running.
    """
    return {"status": "ok"}

@router.post("/",response_model=EmailMessageSchema)
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
    # session.refresh(obj)
    response=generate_email_message(payload.message)
      # 3. save that AI response in its own table
    ai_resp = AIChatResponse(
        chat_message_id=obj.id,
        subject=response.subject,
        contents=response.contents,
    )
    session.add(ai_resp)
    session.commit()
    
    
    
    # return {"message": f"Chat created successfully {payload.message}", "id": obj.id, "is_response": obj.is_response, "email": response}
    return response

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


@router.get("/recent/response", response_model=List[ChatMessagesWithResponse])
def get_recent_chats_with_responses(
    session: Session = Depends(get_session),
):
    # fetch ChatMessage + its AI replies in one go
    stmt = (
        select(ChatMessage)
        .options(selectinload(ChatMessage.responses))
        .order_by(ChatMessage.created_at.desc())
        .limit(10)
    )
    msgs = session.exec(stmt).all()
    return [ChatMessagesWithResponse.model_validate(m) for m in msgs]