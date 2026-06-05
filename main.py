import os
from datetime import datetime
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
from langgraph.graph import StateGraph, END
from graph.state import AgentState
from graph.nodes import (
    search_node,
    scraped_node,
    summary_node,
    html_node,
    send_email_node
)

load_dotenv()

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
workflow.add_node("scraper", scraped_node)
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
workflow.add_edge("summarize", "html_maker")
workflow.add_edge("html_maker", "email_sender")
workflow.add_edge("email_sender", END)

app = workflow.compile()


def run_agent():
    topic = os.getenv("TOPIC", "Latest AI tools and frameworks news")
    time = datetime.now()
    print(f"[{time.strftime('%d-%m-%Y %H:%M:%S')}] Running newsletter agent for topic: {topic}")

    initial_state = AgentState(
        topic=f"{topic} {time}",
        search_results=[],
        scraped_details=[],
        summaries=[],
        final_html=None,
        search_iteration=0,
        failure_urls=[],
        send_email=None,
        email_state=None
    )

    result = app.invoke(initial_state)
    print(result["send_email"])


if __name__ == "__main__":
    schedule_hour = int(os.getenv("SCHEDULE_HOUR", "8"))
    schedule_minute = int(os.getenv("SCHEDULE_MINUTE", "0"))

    print(f"Scheduler started — will run daily at {schedule_hour:02d}:{schedule_minute:02d}")

    scheduler = BlockingScheduler()
    scheduler.add_job(run_agent, "cron", hour=schedule_hour, minute=schedule_minute)
    scheduler.start()
