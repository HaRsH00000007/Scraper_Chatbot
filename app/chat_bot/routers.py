from fastapi import APIRouter,HTTPException, Request, Depends, Path
from typing import List, Dict
from .utils import crawl_logic, scrape_logic,process_and_store_logic,query_logic
from .schema import CrawlResponse, ChatBotIn,ChatBotOut,ScrapedContent,QueryResponse,CrawlRequest,QueryRequest
from app.chat_bot.models import ChatBot
from app.authentication.models import User
from typing import Any
from fastapi.responses import JSONResponse


scrap_router = APIRouter()



@scrap_router.post("/chatbot")
async def create_chatbot(name:str,chatbot: ChatBotIn) -> Any:
    """
    API to create a chatbot for the currently logged-in user.
    """
    # Fetch the currently logged-in user from the database
    user = await User.find_one({"_id":chatbot.user_id})
    print(user.id,"user")
    # existing_user = await User.find_one({"email": "gautamkr1998+2@gmail.com"})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create a new chatbot for the authenticated user
    chatbot = ChatBot(user=user,name=name)  # Add additional fields if required
    await chatbot.insert()

    return {
        "status": "success",
        "message": "Chatbot created successfully",
        "chatbot": {
            "id": str(chatbot.id),
            "user_id": user.id,
            "name": chatbot.name
        }
    }


@scrap_router.get("/chatbots", response_model=List[ChatBotOut])
async def list_chatbots():
    """
    API to list all chatbots.
    """
    # Fetch all chatbots from the database
    chatbots = await ChatBot.all().to_list()
    chatbots_with_user = []

    for chatbot in chatbots:
        # Fetch the associated user for each chatbot
        user = await chatbot.user.fetch()

        # Construct a response dictionary with only the needed fields
        chatbot_dict = chatbot.dict()
        chatbot_dict["user"] = {"id": user.id, "email": user.email}  # Only include user id and email

        # Add the chatbot with user data to the list
        chatbots_with_user.append(chatbot_dict)

    # Return the list of chatbots with user info
    return chatbots_with_user

@scrap_router.get("/chatbots/{chatbot_id}", response_model=ChatBotOut)
async def get_chatbot(chatbot_id: str = Path(..., description="The ID of the chatbot to retrieve")) -> Any:
    """
    API to get details of a specific chatbot by ID.
    """
    # Fetch the chatbot with the specified ID
    chatbot = await ChatBot.find_one({"_id": chatbot_id})
    
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    
    # Fetch the associated user
    user = await chatbot.user.fetch()
    
    # Prepare the chatbot response, including only necessary user fields
    chatbot_dict = chatbot.dict()  # Get chatbot data as a dictionary
    chatbot_dict["user"] = {"id": user.id, "email": user.email}  # Only include 'id' and 'email'

    # Return the chatbot data with user details, matching the response model
    return chatbot_dict

@scrap_router.delete("/chatbots/{chatbot_id}")
async def delete_chatbot(chatbot_id: str = Path(..., description="The ID of the chatbot to delete")):
    """
    API to delete a chatbot by its ID.
    """
    # Fetch the chatbot with the specified ID
    chatbot = await ChatBot.find_one({"_id": chatbot_id})
    
    if not chatbot:
        # Raise HTTP 404 if chatbot not found
        raise HTTPException(status_code=404, detail="Chatbot not found")
    
    # Delete the chatbot
    await chatbot.delete()

    # Return a success message
    return JSONResponse(status_code=200, content={"detail": "Chatbot deleted successfully"})

@scrap_router.post("/crawl", response_model=CrawlResponse)
def crawl_urls(request: CrawlRequest, max_pages: int = 100) -> Dict[str, List[str]]:
    try:
        homepage = request.homepage
        result = crawl_logic(homepage, max_pages)
        if not result["crawled_urls"]:
            raise HTTPException(status_code=404, detail="No URLs found during crawling")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


# @scrap_router.post("/scrape", response_model=List[ScrapedContent])
async def scrape_urls(urls: List[str]) -> List[Dict]:
    try:
        return scrape_logic(urls)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @scrap_router.post("/process_and_store")
async def process_and_store(scraped_data: List[ScrapedContent]):
    try:
        process_and_store_logic(scraped_data)
        return {"status": "success", "message": "Data processed and stored in ChromaDB"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@scrap_router.post("/query", response_model=QueryResponse)
async def query_and_respond(request: QueryRequest) -> Dict:
    try:
        query = request.query
        result = query_logic(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

