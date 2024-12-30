from typing import List,Optional,Dict
from pydantic import BaseModel
from app.chat_bot.models import User
from langchain_groq import ChatGroq
import os
from datetime import datetime
from config import settings

os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY

# Initialize Groq LLM
llm = ChatGroq(
    model_name="mixtral-8x7b-32768",
    temperature=0.7,
    max_tokens=4096
)


class CrawlRequest(BaseModel):
    homepage: List[str] 
    chatbot_id: str
    max_pages:int=30

class QueryRequest(BaseModel):
    query:str
    chatbot_id:str
    session_id:str

class ScrapedData(BaseModel):
    url: str
    content: str
    status: str

# class CrawlResponse(BaseModel):
#     status: str
#     crawled_urls: Dict[str, List[str]]
#     scraped_data: List[ScrapedData]

class CrawlResponse(BaseModel):
    status: str
    crawled_urls: str
    scraped_data: str

class ChatBotSchema(BaseModel):
    pass

class ChatBotIn(BaseModel):
    name: str
    is_active: Optional[bool] = False
    user_id: str

class UserPartial(BaseModel):
    id: str
    email: str

# Define the ChatBotOut model to include the partial user object
class ChatBotOut(BaseModel):
    id: str
    is_active: Optional[bool]
    name: str
    user: UserPartial

class ScrapedContent(BaseModel):
    url: str
    content: str
    status: str

class QueryResponse(BaseModel):
    query: str
    response: str
    contexts: List[str]
    

class ChatMessage(BaseModel):
    role: str  # 'human' or 'ai'
    message: str

class ChatHistory(BaseModel):
    chatbot_id: str
    user_id: str
    session_id: str
    chat_history: List[ChatMessage]
    timestamp: datetime