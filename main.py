from langgraph.graph import StateGraph, END
from graph.state import AgentState
from graph.nodes import (
    search_node,
    scarped_node,
    summary_node,
    html_node,
    send_email_node
)
from datetime import datetime

time = datetime.now()
initial_state = AgentState(
    topic = f"Latest AI tools and frameworks news in {time}", # change this to your topic
    search_results = [],
    scraped_details = [],
    summaries = [],
    final_html= None,
    search_iteration= 0,
    failure_urls = [],
    send_email = None,
    email_state= None
)

def should_continue(state: AgentState) -> str:
    if not state["search_results"]:  
        if state["search_iteration"] >= 3:
            return END        
        else:
            return "searcher" 
    else:
        return "scraper"      

workflow = StateGraph(AgentState)
workflow.add_node("searcher", search_node)
workflow.add_node("scraper", scarped_node)
workflow.add_node("summarize", summary_node)
workflow.add_node("html_maker", html_node)
workflow.add_node("email_sender", send_email_node)


workflow.set_entry_point("searcher")
workflow.add_conditional_edges(
    "searcher",        
    should_continue,   
    {
        "scraper": "scraper",   
        "searcher": "searcher", 
        END: END
    }                
)
workflow.add_edge("scraper", "summarize") 
workflow.add_edge("summarize", "html_maker",) 
workflow.add_edge("html_maker", "email_sender") 
workflow.add_edge("email_sender", END)  


app = workflow.compile()


result = app.invoke(initial_state)

result = app.invoke(initial_state)
print(result["email_state"])
print(result["send_email"])