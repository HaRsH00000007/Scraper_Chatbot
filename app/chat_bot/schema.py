from typing import List,Optional,Dict
from pydantic import BaseModel
from app.chat_bot.models import User
import chromadb
from langchain_groq import ChatGroq
import os
from chromadb.config import Settings
from chromadb.utils import embedding_functions

os.environ["GROQ_API_KEY"] = "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"  # Replace with your Groq API key

# Initialize Groq LLM
llm = ChatGroq(
    model_name="mixtral-8x7b-32768",
    temperature=0.7,
    max_tokens=4096
)

# chroma_client = chromadb.Client()

# Create or get the collection with an embedding function
# chroma_collection = chroma_client.get_or_create_collection(
#     name="web_content",  # The name of the collection
#     embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
#         model_name="all-MiniLM-L6-v2"  # You can replace this with your own model if needed
#     )
# )

class CrawlRequest(BaseModel):
    homepage: List[str] 

class ScrapedData(BaseModel):
    url: str
    content: str
    status: str

class CrawlResponse(BaseModel):
    status: str
    crawled_urls: Dict[str, List[str]]
    scraped_data: List[ScrapedData]

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