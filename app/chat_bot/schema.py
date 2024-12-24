from typing import List
from pydantic import BaseModel

class CrawlResponse(BaseModel):
    status: str
    homepage: str
    crawled_urls: List[str]

class ChatBotSchema(BaseModel):
    pass