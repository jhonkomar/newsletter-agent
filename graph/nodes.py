from tavily import TavilyClient
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
from state import AgentState

load_dotenv()



def search_node(state: AgentState) -> dict:
    topic = state["topic"]   
    tavily_client = TavilyClient(api_key=f"{os.getenv('TAVLY_API_KEY')}")
    response = tavily_client.search(f"{topic}")
    urls = [res.get('url') for res in response["results"]]
    return {
        "search_results": urls,
        "iteration": state["iteration"] + 1
    }
    

def scarped_node(state : AgentState) -> list:
    urls = state["search_results"]
    fal_url = []
    scraped_texts = []
    for url in urls:
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            text = soup.get_text()
            scraped_texts.append(text)
        except:
            fal_url.append(url)
            continue
    return {
        "scarped_details": scraped_texts,
        "faliure_url": fal_url
    }



