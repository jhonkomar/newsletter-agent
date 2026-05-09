from tavily import TavilyClient
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
from openai import OpenAI
from graph.state import AgentState
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

load_dotenv()



def search_node(state: AgentState) -> dict:
    topic = state["topic"]   
    tavily_client = TavilyClient(api_key=f"{os.getenv('TAVLY_API_KEY')}")
    response = tavily_client.search(f"{topic}")
    urls = [res.get('url') for res in response["results"]]
    return {
        "search_results": urls,
        "search_iteration": state["search_iteration"] + 1
    }
    

def scarped_node(state : AgentState) -> dict:
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

def summary_node(state : AgentState) -> dict:
    scarped_result = state["scraped_details"]
    summaries = []
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key= os.getenv("OPENROUTER_API_KEY"),
        )
    for article in scarped_result:
        summary = client.chat.completions.create(
            model="google/gemini-2.5-flash",
            messages=[
                {
                    "role": "system",
                    "content":"""You are an assistant that summarizes articles about coding competitions and AI development tools.
Summarize the following article in 3-5 sentences. Focus on:
- Event/competition name
- Registration deadline
- Prize or benefits
- Link or source if available
Be concise and informative."""},
                {
                    "role": "user",
                    "content": f"article : {article}"
                }
                
            ]
        )
        summaries.append(summary.choices[0].message.content)
    return {
        "summaries": summaries
    }

def html_node(state : AgentState) -> dict:
    sum_text = state["summaries"]
    user_massage = "list article."
    for no,article in enumerate(sum_text):
        user_massage += f"article {no}:{article}"
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key= os.getenv("OPENROUTER_API_KEY"),
        )
    html = client.chat.completions.create(
            model="google/gemini-2.5-flash",
            messages=[
                {
                    "role": "system",
                    "content":"""You are an HTML Email Formatter.

Rules:

* Output only PURE HTML.
* No markdown.
* Inline CSS only.
* No external libraries or CDN.
* No explanations or intro text.
* Output must be ready to send as email HTML.

Design:

* Clean, modern, readable.
* Use card layout for each item.
* Soft professional colors.
* Clear typography.
* Responsive and email-friendly.

Structure:

* Main wrapper with max-width.
* Separate card for each item.
* Modern spacing, radius, and soft shadow.

If showing competitions/events:

* title
* deadline
* category
* benefit
* clickable link

Goal:
Create premium-looking HTML emails that render well on Gmail and mobile.
"""},
                {
                    "role": "user",
                    "content": f"{user_massage}"
                }
                
            ]
        )
    return {
        "final_html": html.choices[0].message.content
    }


def send_email_node(state : AgentState) -> dict:
    topic = state["topic"]
    time = datetime.datetime.now()
    body = state["final_html"]
    sender = os.getenv("EMAIL_SENDER")
    recipient = os.getenv("EMAIL_RECEIVER")
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    system_massage = ""
    send_state = None
    try:                  
        msg = MIMEMultipart()        
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = f"Breaking News 🔥 {time.strftime("%d-%m-%Y %H:%M:%S")} about the topic:{topic}"
        msg.attach(MIMEText(body, 'html'))
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()   
            server.login(sender, os.getenv("EMAIL_PASSWORD"))  
            server.sendmail(sender, recipient, msg.as_string())
            system_massage = "Success: Email sent successfully."
            send_state = True
    except smtplib.SMTPAuthenticationError:
        system_massage = "Error: Authentication failed. Check your App Password."
        send_state = False
    except smtplib.SMTPConnectError:
        system_massage = "Error: Failed to connect to the SMTP server."
        send_state = False
    except smtplib.SMTPException as e:
        system_massage = f"Error: SMTP issue occurred: {str(e)}"
        send_state = False
    except Exception as e:
        system_massage = f"Error: An unexpected error occurred: {str(e)}"
        send_state = False
    return {
        "send_email": system_massage,
        "email_state": send_state
    }
