from typing import List, Dict
from urllib.parse import urljoin
import requests
from app.chat_bot.models import ChatBot
from app.authentication.models import User
from bs4 import BeautifulSoup

def crawl_logic(homepage: str, max_pages: int = 100) -> Dict[str, List[str]]:
    """
    Function to handle the crawling logic.
    """
    visited = set()
    to_visit = [homepage]
    all_urls = []

    while to_visit and len(visited) < max_pages:
        current_url = to_visit.pop(0)
        try:
            response = requests.get(
                current_url, 
                verify=False, 
                timeout=10, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all("a", href=True):
                url = urljoin(homepage, link['href'])
                if url not in visited and url.startswith(homepage):  # Ensure it's part of the homepage domain
                    to_visit.append(url)
                    visited.add(url)
                    all_urls.append(url)
        except Exception as e:
            print(f"Error crawling {current_url}: {e}")

    return {
        "status": "success",
        "homepage": homepage,
        "crawled_urls": all_urls
    }


async def chabot_create():
    existing_user = await User.find_one({"email": "user_email"})
    chatbot = ChatBot(user=existing_user)
    await chatbot.insert()
    pass


from fastapi import HTTPException, Depends, Request
from jose import jwt  # For token decoding
from config import Settings

async def login_required(request: Request):
    """
    Dependency to enforce login.
    Extract and validate the token from the Authorization header.
    """
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")

    token = token.split(" ")[1]
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, Settings.ALGORITHM)
        user = await User.find_one({"email": payload.get("sub")})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return {"email": user["email"], "id": str(user["_id"])}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
