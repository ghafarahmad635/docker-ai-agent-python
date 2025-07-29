from pydantic import BaseModel, Field


class EmailMessageSchema(BaseModel):
    subject: str
    contents: str
    invalid_request: bool | None = Field(default=False, description="Indicates if the request is invalid")