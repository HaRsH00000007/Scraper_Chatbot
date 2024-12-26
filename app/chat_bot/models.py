from typing import Optional
from uuid import uuid4
from beanie import Document,Link
from pydantic import EmailStr, Field
from datetime import datetime, timezone
from app.authentication.models import User
from typing import List
from app.chat_bot.schema import ChatMessage

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
        
# Define the ChatBot Document
class ChatBot(Document):
    id: str = Field(default_factory=lambda: str(uuid4()))
    is_active: bool = False  # For account activation
    name: str
    user: Link[User]
    chat_history: List[ChatMessage] = []  # Optional, add this if you need to store the chat
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "chatbot"