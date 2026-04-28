# ◈ ARXIS — Research Intelligence System

> A multi-agent AI pipeline that searches, scrapes, writes, and critiques — delivering intelligence-grade research reports on any topic.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1.x-green?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red?style=flat-square&logo=streamlit&logoColor=white)
![OpenRouter](https://img.shields.io/badge/OpenRouter-API-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)

---

## What is ARXIS?

ARXIS is a **multi-agent research system** built on LangChain. You give it a topic — it spins up four specialized AI agents that collaborate in sequence to produce a structured, reviewed research report automatically.

No manual searching. No copy-pasting. Just drop a topic and get a full report with a critic score.

---

## Pipeline Architecture

```
Topic Input
    │
    ▼
┌─────────────────────┐
│   01 · Search Agent │  ── Tavily web search → recent, reliable sources
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   02 · Reader Agent │  ── Picks top URL → scrapes full page content (BeautifulSoup)
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   03 · Writer Chain │  ── LCEL pipeline → structured research report (markdown)
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   04 · Critic Chain │  ── Reviews report → score /10 + strengths + improvements
└─────────────────────┘
          │
          ▼
     Final Output
  (Report + Feedback)
```

---

## Features

- **4-stage agentic pipeline** — search → scrape → write → critique
- **OpenRouter support** — use any model (GPT-4o, Claude, Mistral, etc.) via a single API key
- **LCEL writer & critic chains** — clean, composable LangChain pipelines
- **Streamlit UI (ARXIS)** — dark editorial interface with live pipeline tracker
- **Export report** — download the final report as a `.md` file
- **Critic scoring** — every report gets reviewed and scored out of 10

---

## Project Structure

```
ResearchAgenticsystem/
├── agents.py          # Builds search & reader agents + writer/critic LCEL chains
├── pipeline.py        # Orchestrates the full 4-step research pipeline
├── tools.py           # Tavily web search + BeautifulSoup scraper tools
├── app.py             # Streamlit UI (ARXIS)
├── .env               # API keys (never committed)
├── .env.example       # Template for required environment variables
├── .gitignore         # Ignores .env, venv, __pycache__, etc.
└── requirement.txt    # All dependencies
```

---

## Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/Sushit-prog/Research--Agent.git
cd Research--Agent
```

### 2. Create a virtual environment

```bash
# Using uv (recommended)
uv venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies

```bash
uv pip install -r requirement.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

> Get your OpenRouter key at [openrouter.ai](https://openrouter.ai)  
> Get your Tavily key at [tavily.com](https://tavily.com)

### 5. Run the pipeline (terminal)

```bash
python pipeline.py
```

### 6. Run the UI

```bash
uv run streamlit run app.py
```

---

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `OPENROUTER_API_KEY` | OpenRouter API key for LLM access | ✅ |
| `TAVILY_API_KEY` | Tavily API key for web search | ✅ |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | LangChain 1.x |
| LLM Provider | OpenRouter (GPT-4o-mini default) |
| Web Search | Tavily |
| Web Scraping | BeautifulSoup4 + Requests |
| UI | Streamlit |
| Package Manager | uv |
| Environment | python-dotenv |

---

## How the Agents Work

**Search Agent** — Uses the Tavily tool to find recent, reliable sources on the given topic. Returns a structured list of results with URLs and summaries.

**Reader Agent** — Takes the search results, picks the most relevant URL, and uses BeautifulSoup to scrape the full page content for deeper context.

**Writer Chain** — An LCEL pipeline (`prompt | llm | StrOutputParser`) that takes both search results and scraped content and writes a detailed report structured as: Introduction, Key Findings, Conclusion, and Sources.

**Critic Chain** — A second LCEL pipeline that independently reviews the report and returns a score out of 10, strengths, areas to improve, and a one-line verdict.

---

## UI Overview

ARXIS features a dark editorial interface built with Streamlit:

- **Live pipeline tracker** in the sidebar — shows each agent's status (idle / running / done) in real time
- **Raw output cards** — collapsible views of search and scraped content
- **Report card** — full markdown report rendered with amber accent styling
- **Critic card** — glowing cyan score badge + detailed feedback
- **Export button** — download the report as `.md`

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## License

MIT © [Sushit Prog](https://github.com/Sushit-prog)
