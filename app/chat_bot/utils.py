from typing import List, Dict
from urllib.parse import urljoin
import requests
from app.chat_bot.models import ChatBot
from app.authentication.models import User
from bs4 import BeautifulSoup
from app.chat_bot.schema import llm
import re
import concurrent.futures
from tqdm import tqdm
from urllib.parse import urlparse, urlunparse
from chromadb.utils import embedding_functions
import chromadb
from app.chat_bot.schema import QueryResponse


chroma_client = chromadb.Client()


async def chabot_create():
    existing_user = await User.find_one({"email": "user_email"})
    chatbot = ChatBot(user=existing_user)
    await chatbot.insert()


def scrape_logic(urls: List[str]) -> List[Dict]:
    def scrape_single_url(url: str) -> Dict:
        try:
            response = requests.get(
                url, 
                verify=False, 
                timeout=10, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            for script in soup(["script", "style"]):
                script.decompose()

            text = soup.get_text()
            text = re.sub(r'\s+', ' ', text).strip()
            text = re.sub(r'[^\w\s.,?!-]', '', text)

            return {"url": url, "content": text, "status": "success"}
        except Exception as e:
            return {"url": url, "content": "", "status": f"error: {str(e)}"}

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(tqdm(executor.map(scrape_single_url, urls), total=len(urls), desc="Scraping URLs"))
    return results


# def process_and_store_logic(scraped_data: List[Dict]):
#     chroma_docs, chroma_meta, chroma_ids = [], [], []
#     doc_counter = 0

#     for item in scraped_data:
#         if item.status == "success" and item.content:
#             chunks = chunk_text(item.content)
#             for chunk in chunks:
#                 chroma_docs.append(chunk)
#                 chroma_meta.append({"url": item.url})
#                 chroma_ids.append(f"doc_{doc_counter}")
#                 doc_counter += 1

#     if chroma_docs:
#         chroma_collection.add(
#             documents=chroma_docs,
#             metadatas=chroma_meta,
#             ids=chroma_ids
#         )

# def chunk_text(text: str, chunk_size: int = 1000) -> List[str]:
#     words = text.split()
#     chunks, current_chunk, current_length = [], [], 0

#     for word in words:
#         current_length += len(word) + 1
#         if current_length > chunk_size:
#             chunks.append(' '.join(current_chunk))
#             current_chunk = [word]
#             current_length = len(word)
#         else:
#             current_chunk.append(word)

#     if current_chunk:
#         chunks.append(' '.join(current_chunk))

#     return chunks

def chroma_fn(id):
    chroma_collection = chroma_client.get_or_create_collection(
        name=id,  # The name of the collection is set dynamically
        embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"  # You can replace this with your own model if needed
        )
    )
    return chroma_collection

def process_and_store_logic(scraped_data: List[Dict], chatbot_id: str):
    print(f"scrappped::{scraped_data}")
    chroma_docs, chroma_meta, chroma_ids = [], [], []
    doc_counter = 0
    chroma_obj = chroma_fn(chatbot_id)

    # Dynamically create or get the collection using the chatbot_id
    # chroma_collection = chroma_client.get_or_create_collection(
    #     name=chatbot_id,  # The name of the collection is set dynamically
    #     embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
    #         model_name="all-MiniLM-L6-v2"  # You can replace this with your own model if needed
    #     )
    # )

    # Process the scraped data and store it in Chroma
    for item in scraped_data:
        print(f"item::{item}")
        if item["status"] == "success" and item["content"]:
            print("yes come")
            chunks = chunk_text(item["content"])
            for chunk in chunks:
                chroma_docs.append(chunk)
                chroma_meta.append({"url": item["url"]})
                chroma_ids.append(f"doc_{doc_counter}")
                doc_counter += 1
    max_batch_size = 5000

    for i in range(0, len(chroma_docs), max_batch_size):
        batch_docs = chroma_docs[i:i + max_batch_size]
        batch_meta = chroma_meta[i:i + max_batch_size]
        batch_ids = chroma_ids[i:i + max_batch_size]


        # If there are any documents, add them to the Chroma collection
        print(f"Adding batch {i // max_batch_size + 1} to ChromaDB")
        chroma_obj.add(
            documents=batch_docs,
            metadatas=batch_meta,
            ids=batch_ids
        )
# Your chunk_text function stays the same
def chunk_text(text: str, chunk_size: int = 1000) -> List[str]:
    words = text.split()
    chunks, current_chunk, current_length = [], [], 0

    for word in words:
        current_length += len(word) + 1
        if current_length > chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


def crawl_logic(homepages: List[str], max_pages: int = 100) -> Dict[str, List[str]]:
    """
    Function to handle the crawling logic for multiple homepages.
    """
    results = {}  # Dictionary to store crawled URLs for each homepage

    def normalize_url(url):
        parsed = urlparse(url)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path or "/", "", "", ""))

    all_crawled_urls = []
    for homepage in homepages:
        visited = set()
        to_visit = [homepage]
        crawled_urls = []

        while to_visit and len(visited) < max_pages:
            current_url = to_visit.pop(0)
            try:
                print(f"Crawling: {current_url} (Domain: {homepage})")
                response = requests.get(
                    current_url,
                    verify=False,
                    timeout=10,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                )
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                for link in soup.find_all("a", href=True):
                    url = urljoin(current_url, link['href'])
                    normalized_url = normalize_url(url)
                    if normalized_url not in visited and normalized_url.startswith(homepage):
                        to_visit.append(normalized_url)
                        visited.add(normalized_url)
                        crawled_urls.append(normalized_url)
            except Exception as e:
                print(f"Error crawling {current_url}: {e}")

        results[homepage] = crawled_urls
        all_crawled_urls.extend(crawled_urls)
    scraped_results = scrape_logic(all_crawled_urls)
    process_and_store_logic(scraped_results, "dev-1")

    
    return {
        "status": "success",
        "crawled_urls": "results",
        "scraped_data": "scraped_results"
    }


def query_logic(query: str) -> QueryResponse:
    try:
        # Create or get the collection with an embedding function
        # chroma_collection = chroma_client.get_or_create_collection(
        #     name="97401bb2-d261-4761-9e7c-8c72261ebb",  # The name of the collection
        #     embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
        #         model_name="all-MiniLM-L6-v2"  # You can replace this with your own model if needed
        #     )
        # )
        chroma_obj = chroma_fn("dev-1")
        results = chroma_obj.query(
            query_texts=[query],
            n_results=1
        )

        contexts = [doc for doc in results['documents'][0]]

        system_prompt = """You are a helpful AI assistant that answers questions based on the provided context.
        Your answers should be accurate, informative, and directly related to the context provided."""

        user_prompt = f"""Context information is below.
        ---------------------
        {' '.join(contexts)}
        ---------------------
        Given the context information, please answer this question: {query}

        If the context doesn't contain relevant information, please say so instead of making up an answer."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = llm.invoke(messages).content

        return QueryResponse(query=query, response=response, contexts=contexts)
    
    except Exception as e:
        # If there's an error, return a structured response with the error message
        return QueryResponse(query=query, response=f"Error processing query: {e}", contexts=[])