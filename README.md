# 📰 Newsletter Agent

An autonomous AI agent that **searches, scrapes, summarizes, and delivers news about any topic straight to your inbox** — powered by LangGraph.

Just set your topic, and the agent does the rest.

---

## ✨ Features

- 🤖 **Agentic workflow** — multi-step autonomous agent using LangGraph
- 🔎 **Smart search** — finds relevant articles via Tavily Search API
- 🕸️ **Web scraping** — extracts full content from each result using BeautifulSoup
- 📝 **AI summarization** — summarizes each article with LLM (Gemini 2.5 Flash)
- 📧 **Auto email delivery** — sends a beautiful HTML email report to your inbox
- 🔄 **Retry logic** — retries search up to 3x if no results found
- 🎯 **Any topic** — customize the topic to anything you want

---

## 🛠️ Tech Stack

| Component | Tool |
|---|---|
| Agent Framework | LangGraph |
| Search | Tavily API |
| Web Scraping | BeautifulSoup4 + Requests |
| LLM | Google Gemini 2.5 Flash via OpenRouter |
| Email | Python smtplib (Gmail SMTP) |
| Environment | python-dotenv |

---

## 📁 Project Structure

```
newsletter-agent/
├── graph/
│   ├── __init__.py
│   ├── state.py        # AgentState definition
│   └── nodes.py        # All agent nodes
├── .env                # API keys (not committed)
├── .gitignore
├── main.py             # Graph assembly & entry point
└── requirements.txt
```

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/newsletter-agent.git
cd newsletter-agent
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Setup environment variables**

Create a `.env` file:
```
TAVLY_API_KEY=your_tavily_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
EMAIL_SENDER=youremail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_RECEIVER=receiver@gmail.com
```

> **Note:** For Gmail, use an [App Password](https://myaccount.google.com/apppasswords), not your regular password.

---

## 🚀 Usage

**1. Set your topic**

Open `main.py` and change the topic to anything you want:
```python
topic = f"Latest AI tools and frameworks news {time}"  # change this!
```

**2. Run the agent**
```bash
python main.py
```

The agent will automatically:
1. Search for relevant articles about your topic
2. Scrape detailed content from each result
3. Summarize each article using AI
4. Generate a formatted HTML email
5. Send the newsletter to your inbox

---

## 🔄 How It Works

```
[START]
   ↓
[Search Node]  ← Tavily API
   ↓
[Results found?] → No (max 3 retries) → [END]
   ↓ Yes
[Scrape Node]  ← BeautifulSoup
   ↓
[Summary Node] ← LLM (per article)
   ↓
[HTML Node]    ← LLM (generate email template)
   ↓
[Email Node]   ← Gmail SMTP
   ↓
[END]
```

---

## 📬 Sample Output

The agent delivers a clean, card-based HTML email with:
- Article title
- Key takeaways
- Source link
- Publication date (if available)

---

## 🧠 What I Learned

- Building multi-step agentic workflows with **LangGraph**
- Implementing **conditional edges** for retry logic
- Combining **search APIs + web scraping** in one pipeline
- Structuring **AgentState** for data flow between nodes
- Sending **HTML emails** via SMTP programmatically

---

## 📄 License

MIT License