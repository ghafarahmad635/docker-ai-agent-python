from datetime import datetime, timezone
from pydantic import ConfigDict
from sqlmodel import DateTime, Field, SQLModel

def get_utc_now():
    """
    Returns the current UTC datetime.
    """
    return datetime.now().replace(tzinfo=timezone.utc)

class ChatMessagePayload(SQLModel):
    message: str
    

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