from typing import Optional
from uuid import uuid4
from beanie import Document,Link
from pydantic import EmailStr, Field
from datetime import datetime, timezone
from app.authentication.models import User

class ChatBot(Document):
    id: str = Field(default_factory=lambda: str(uuid4()))
    is_active: bool = False  # For account activation
    name: str
    user: Link[User]
    class Settings:
        name = "chatbot"

    class Config:
        json_schema_extra = {
            "example": {
                "is_active": False,
                "name":"My Chatbot"
            }
        }