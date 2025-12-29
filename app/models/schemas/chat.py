from datetime import datetime
from pydantic import BaseModel


class ChatMessageResponse(BaseModel):
    id: int
    author: str
    author_username: str
    is_me: bool
    is_admin: bool
    message: str
    created_at: datetime


class ChatMessageCreate(BaseModel):
    message: str