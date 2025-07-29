from datetime import datetime, timezone
from typing import List
from pydantic import ConfigDict
from sqlmodel import DateTime, Field, Relationship, SQLModel

def get_utc_now():
    """
    Returns the current UTC datetime.
    """
    return datetime.now().replace(tzinfo=timezone.utc)

class ChatMessagePayload(SQLModel):
    message: str
    
class AIChatResponse(SQLModel, table=True):
    id:            int                   | None = Field(default=None, primary_key=True)
    chat_message_id: int                 = Field(foreign_key="chatmessage.id")
    subject:       str
    contents:      str
    is_response:   bool                  = Field(default=True)
    created_at: datetime | None = Field(
        default_factory=get_utc_now,
        sa_type=DateTime(timezone=True),
    )

    # back‑link so you can do ai_resp.chat
    chat: "ChatMessage" = Relationship(back_populates="responses")
    
    
class ChatMessage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    message: str
    is_response: bool = False
    created_at: datetime | None = Field(
        default_factory=get_utc_now,
        sa_type=DateTime(timezone=True),
        nullable=True,
        primary_key=False,
    )
    responses: list[AIChatResponse] = Relationship(back_populates="chat")
    
    



class ChatMessagesRecent(SQLModel):
    message: str
    
    created_at: datetime | None = Field(
        default_factory=get_utc_now,
        sa_type=DateTime(timezone=True),
        nullable=True,
        primary_key=False,
    )

    # enable parsing from ORM attributes
    model_config = ConfigDict(from_attributes=True)
    
    
class AIChatResponseRead(SQLModel):
    subject:    str
    contents:   str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class ChatMessagesWithResponse(SQLModel):
    message:    str
    created_at: datetime
    responses:  List[AIChatResponseRead] = []

    model_config = ConfigDict(from_attributes=True)