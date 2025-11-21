# stock-picker-agent
A multi-agent investment research assistant powered by CrewAI and LangGraph, this stock picker automates equity analysis using vector-based RAG pipelines, LLM summarization, and fundamental screening.
Here is a polished `README.md` for the **stock-picker-agent** project, styled for use on GitHub:

---

# Stock Picker Agent

![LangGraph](https://img.shields.io/badge/LangGraph-framework-blue)
![CrewAI](https://img.shields.io/badge/CrewAI-autonomous-red)
![Pinecone](https://img.shields.io/badge/Pinecone-vector_DB-green)
![LLM](https://img.shields.io/badge/LLM-powered-orange)

A multi-agent investment research assistant powered by **CrewAI** and **LangGraph**, this stock picker automates equity analysis using vector-based RAG pipelines, LLM summarization, and fundamental screening.

## Project Description

This project simulates a team of AI analysts performing investment research in real time. Agents collaborate to:

* Extract and summarize stock market news
* Analyze company fundamentals and financials
* Screen for value, growth, or momentum candidates
* Retrieve data from Pinecone-based vector embeddings
* Produce a ranked list of investment ideas

The architecture enables modular customization for different investment styles, research goals, or data sources (e.g., earnings transcripts, FinTwit embeddings, or macro reports).

## Key Components

| Component                | Description                                          |
| ------------------------ | ---------------------------------------------------- |
| **CrewAI**               | Orchestrates multi-agent collaboration logic         |
| **LangGraph**            | Enables flow-based reasoning and sequencing          |
| **LangChain**            | Handles data parsing, LLM interaction, and tools     |
| **Pinecone**             | Vector store for similarity-based document retrieval |
| **OpenAI/Claude/Gemini** | Foundation LLMs used for summarization and scoring   |

## Technologies Used

* Python 3.11+
* CrewAI
* LangGraph
* Pinecone
* LangChain
* Claude / OpenAI LLMs
* Jupyter Notebooks (for dev + evaluation)
* Optional: FinTwitBERT or FinBERT for embeddings

## Features

* 📊 **Automated Research**: LLM agents fetch and summarize financial documents, earnings, or market news.
* 💡 **Investment Idea Generation**: Output includes ranked stock picks with rationale.
* 🔁 **Plug-and-Play**: Swap out tools, agents, or prompts to explore various strategies.
* 🧩 **RAG Pipelines**: Combines retrieval + LLM synthesis for grounded, explainable results.
* 💬 **Natural Language Querying**: Ask questions like “What are the best dividend stocks this week?”

## Project Structure

```bash
stock-picker-agent/
├── agents/                 # Agent classes and roles
├── workflows/              # LangGraph / CrewAI orchestration logic
├── prompts/                # System prompts and behavior controls
├── data/                   # Sample company docs and earnings
├── pinecone_utils.py       # Vector DB setup
├── run_stock_picker.py     # Entry point
└── README.md
```

## Use Cases

* Personal investment research automation
* Financial analyst productivity tools
* FinTech LLM assistant prototypes
* Educational demo of LangGraph + CrewAI integration

## Getting Started

```bash
git clone https://github.com/Crazy-Horse/stock-picker-agent.git
cd stock-picker-agent
pip install -r requirements.txt
python run_stock_picker.py
```

> ⚠️ You’ll need API keys for OpenAI or Claude, as well as a Pinecone project environment.

## Next Steps

* Add earnings transcript ingestion via API
* Enable portfolio constraints and optimization
* Integrate Twitter/X sentiment with FinTwitBERT

## Related Projects

* [📊 multi-agent-research](https://github.com/Crazy-Horse/multi-agent-research)
* [💰 trading-floor-agents](https://github.com/Crazy-Horse/trading-floor-agents)


