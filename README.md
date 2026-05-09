# 🔍 Scarper Event — AI-Powered Event & Competition Agent

An autonomous AI agent that **automatically searches, scrapes, summarizes, and delivers** the latest coding competitions and AI engineering opportunities straight to your inbox — every day.

Built with **LangGraph**, **Tavily**, **BeautifulSoup**, and **OpenRouter (Gemini 2.5 Flash)**.

---

## ✨ Features

- 🤖 **Agentic workflow** — multi-step autonomous agent using LangGraph
- 🔎 **Smart search** — finds relevant events via Tavily Search API
- 🕸️ **Web scraping** — extracts full content from each result using BeautifulSoup
- 📝 **AI summarization** — summarizes each article with LLM (Gemini 2.5 Flash)
- 📧 **Auto email delivery** — sends a beautiful HTML email report to your inbox daily
- 🔄 **Retry logic** — retries search up to 3x if no results found

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
scarper-event/
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
git clone https://github.com/yourusername/scarper-event.git
cd scarper-event
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

```bash
python main.py
```

The agent will:
1. Search for coding competitions & AI engineering events
2. Scrape detailed content from each result
3. Summarize each article using AI
4. Generate a formatted HTML email
5. Send the report to your inbox

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
- Event/competition name
- Registration deadline
- Category
- Prize or benefit
- Source link

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