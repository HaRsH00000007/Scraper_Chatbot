from fastapi import APIRouter,HTTPException, Request, Depends
from typing import List, Dict
from .utils import crawl_logic
from .schema import CrawlResponse
from app.chat_bot.models import ChatBot
from app.authentication.models import User
from app.chat_bot.utils import login_required
from typing import Any
scrap_router = APIRouter()

@scrap_router.get("/crawl", response_model=CrawlResponse)
def crawl_urls(homepage: str, max_pages: int = 100) -> Dict[str, List[str]]:
    try:
        result = crawl_logic(homepage, max_pages)
        if not result["crawled_urls"]:
            raise HTTPException(status_code=404, detail="No URLs found during crawling")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@scrap_router.post("/chatbot")
async def create_chatbot(name:str,request: Request, user: dict = Depends(login_required)) -> Any:
    """
    API to create a chatbot for the currently logged-in user.
    """
    # Fetch the currently logged-in user from the database
    # existing_user = await User.find_one({"email": user["email"]})
    
    # if not existing_user:
    #     raise HTTPException(status_code=404, detail="User not found")

    # Create a new chatbot for the authenticated user
    chatbot = ChatBot(user="existing_user",name=name)  # Add additional fields if required
    await chatbot.insert()

    return {
        "status": "success",
        "message": "Chatbot created successfully",
        "chatbot": {
            "id": str(chatbot.id),
            "user_id": str("existing user"),
            "name": chatbot.name
        }
    }


@scrap_router.get("/chatbots")
async def list_chatbots(user: dict = Depends(login_required)) -> Any:
    """
    API to list all chatbots for the currently logged-in user.
    """
    # Fetch the currently logged-in user from the database
    # existing_user = await User.find_one({"email": user["email"]})

    # if not existing_user:
    #     raise HTTPException(status_code=404, detail="User not found")

    # Fetch all chatbots associated with the logged-in user
    chatbots = await ChatBot.find(ChatBot.user == "existing_user").to_list()

    # Return the list of chatbots
    return {
        "status": "success",
        "message": "Chatbots retrieved successfully",
        "chatbots": [
            {
                "id": str(chatbot.id),
                "name": chatbot.name,
                "is_active": chatbot.is_active,
                "user_id": str("id"),
            }
            for chatbot in chatbots
        ],
    }
