from typing import Optional
from uuid import uuid4
from beanie import Document,Link
from pydantic import EmailStr, Field
from datetime import datetime, timezone
from app.authentication.models import User
from typing import List,Dict
from app.chat_bot.schema import ChatMessage

class ChatBot(Document):
    id: str = Field(default_factory=lambda: str(uuid4()))
    is_active: bool = False  # For account activation
    name: str
    user: Link[User]
    messages: List[Dict[str, str]] = Field(default_factory=list)  # Conversation history
    crawl_links : Optional[List[str]]=None
    session_id : Optional[str]=None

    class Settings:
        name = "chatbot"

    class Config:
        json_schema_extra = {
            "example": {
                "is_active": False,
                "name":"My Chatbot"
            }
        }
        
    def add_links(self, link:List):
        """Add a new message to the messages list."""
        self.crawl_links=link

        
# Define the ChatBot Document