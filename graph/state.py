from typing import TypedDict, List

class AgentState(TypedDict):
    topic: str
    search_results: List[str]  
    faliure_urls: list[str] 
    scraped_details: List[str]  
    summaries: List[str]
    final_html: str
    send_email : str
    email_state : bool
    search_iterationn: int

# state for nodes