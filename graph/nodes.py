from tavily import TavilyClient
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
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
    




