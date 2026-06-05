# Newsletter Agent

An autonomous AI agent that **searches, scrapes, summarizes, and delivers news about any topic straight to your inbox** — on a daily schedule, powered by LangGraph.

Set your topic and schedule once, deploy to a VPS, and never worry about it again.

---

## Features

- **Agentic workflow** — multi-step autonomous pipeline using LangGraph
- **Smart search** — finds relevant articles via Tavily Search API
- **Web scraping** — extracts full content from each URL using BeautifulSoup
- **AI summarization** — summarizes each article individually using an LLM
- **HTML email delivery** — generates a clean, card-based HTML email and sends it automatically
- **Retry logic** — retries search up to 3x if no results are found before giving up
- **Fully configurable via `.env`** — topic, schedule time, and all credentials are set through environment variables, no code changes needed

---

## Tech Stack

| Component | Tool |
|---|---|
| Agent Framework | LangGraph |
| Search | Tavily API |
| Web Scraping | BeautifulSoup4 + Requests |
| LLM | Google Gemini 2.5 Flash via OpenRouter |
| Email | Python smtplib (Gmail SMTP) |
| Scheduler | APScheduler |
| Environment | python-dotenv |

---

## How It Works

```
[START]
   ↓
[Search Node]        — queries Tavily API with your topic
   ↓
[Results found?]     — No → retry up to 3x → [END]
   ↓ Yes
[Scrape Node]        — scrapes full content from each URL
   ↓
[Summary Node]       — LLM summarizes each article (runs per article)
   ↓
[HTML Node]          — LLM generates a formatted HTML email from all summaries
   ↓
[Email Node]         — sends the email via Gmail SMTP
   ↓
[END]
```

The graph runs on a **daily cron schedule** (configurable). APScheduler keeps the process alive and triggers the pipeline at the specified time every day.

---

## Project Structure

```
newsletter-agent/
├── graph/
│   ├── __init__.py
│   ├── state.py        # AgentState — shared data structure across all nodes
│   └── nodes.py        # All node functions (search, scrape, summarize, html, email)
├── .env                # Your credentials and config (never commit this)
├── .env.example        # Template — copy this to .env and fill in your values
├── main.py             # Graph assembly, scheduler, and entry point
└── requirements.txt
```

---

## Setup Guide (from scratch)

### 1. Fork and clone

```bash
git clone https://github.com/yourusername/newsletter-agent.git
cd newsletter-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get your API keys

You need accounts and API keys for the following services:

**Tavily** (web search)
- Sign up at [tavily.com](https://tavily.com)
- Go to your dashboard and copy your API key

**OpenRouter** (LLM access)
- Sign up at [openrouter.ai](https://openrouter.ai)
- Go to Keys and create a new API key
- Make sure you have credits — Gemini 2.5 Flash is very cheap

**Gmail App Password** (for sending email)
- You need 2-Step Verification enabled on your Google account
- Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
- Create a new App Password (select "Mail" as the app)
- Copy the 16-character password — this is your `EMAIL_PASSWORD`
- Do **not** use your regular Gmail password, it will not work

### 5. Configure your `.env`

Copy the example file:

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
# Tavily Search API
TAVLY_API_KEY=your_tavily_api_key

# OpenRouter (LLM)
OPENROUTER_API_KEY=your_openrouter_api_key

# Gmail SMTP
EMAIL_SENDER=youremail@gmail.com
EMAIL_PASSWORD=your_16_char_app_password
EMAIL_RECEIVER=receiver@gmail.com

# Newsletter topic — change this to anything you want
TOPIC=Latest AI tools and frameworks news

# Daily schedule (24-hour format, VPS server timezone)
SCHEDULE_HOUR=8
SCHEDULE_MINUTE=0
```

### 6. Run it

```bash
python main.py
```

The scheduler will start and print the time it will run each day:

```
Scheduler started — will run daily at 08:00
```

It will stay running as a background process and trigger the agent at the configured time every day.

---

## Deploying to a VPS

Once your `.env` is configured and you've verified it works locally, deploy to a VPS:

```bash
# SSH into your VPS, clone the repo, set up .env as above, then:
nohup python main.py > newsletter.log 2>&1 &
```

To check the logs:

```bash
tail -f newsletter.log
```

To stop the process:

```bash
# Find the process ID
ps aux | grep main.py

# Kill it
kill <PID>
```

**Recommended**: use `screen` or `tmux` for easier session management:

```bash
screen -S newsletter
python main.py
# Detach: Ctrl+A then D
# Reattach: screen -r newsletter
```

---

## Changing the Topic

Edit `TOPIC` in your `.env` file, then restart the process. No code changes needed.

```env
TOPIC=Weekly cybersecurity news and vulnerabilities
```

---

## License

MIT License
