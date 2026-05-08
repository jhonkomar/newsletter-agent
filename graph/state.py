from typing import TypedDict, List

class AgentState(TypedDict):
    topic: str
    search_results: List[str]   
    scraped_details: List[str]  
    summaries: List[str]
    final_html: str
    iteration: int

# state for nodes