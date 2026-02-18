
# Stock Picker Agent (CrewAI + LangGraph)

A multi-agent investment research assistant that automates **equity research** and produces a **ranked list of stock ideas** using:
- **CrewAI** for agent collaboration
- **LangGraph** for deterministic, auditable workflows
- **RAG** (vector search) for grounded analysis and citations
- **LLM synthesis** for summaries, scoring, and investment-style screening

> **Audience (one sentence):** Built for engineers, analysts, and builders who want a reproducible, modular “AI analyst team” that turns news + documents into ranked investment ideas.

---

## Why this exists (business impact)
Investment research is time-consuming and inconsistent across sources (news, filings, transcripts, notes). This project provides a repeatable pipeline to:
- reduce manual reading and summarization time
- standardize screening criteria (value/growth/momentum/dividend)
- keep outputs grounded in retrieved documents (RAG) with traceable sources
- accelerate early-stage idea generation and triage (not execution)

> ⚠️ **Not financial advice.** This is a research automation demo for educational/engineering purposes.

---

## What it does

### End-to-end workflow
1. **Discover candidates** (recent news / market activity)
2. **Retrieve evidence** (RAG over your corpus: filings, transcripts, notes, articles)
3. **Summarize + extract signals** (catalysts, risks, financial highlights)
4. **Score + rank ideas** (style-aware rubric)
5. **Output a report** (markdown + structured JSON) with citations and dates

### Output artifacts
By default, the run generates:
- `outputs/rankings.md` — ranked stock ideas with rationale + citations
- `outputs/rankings.json` — structured rankings for programmatic use
- `outputs/research_pack/` — per-ticker notes, snippets, and retrieved sources (optional)

---

## Architecture (high level)

**CrewAI** handles agent roles and tool usage, while **LangGraph** defines the workflow as a graph (stateful, inspectable, and easier to debug than pure prompting).

Typical agent responsibilities:
- **News Scout**: finds candidate tickers and relevant items
- **Retriever**: queries the vector store for grounding documents
- **Fundamentals Analyst**: extracts metrics and constraints
- **Risk Analyst**: flags red flags, uncertainty, missing data
- **Portfolio PM / Ranker**: scores + ranks and produces final output

---

## Tech stack
- Python **3.11+** (recommended)
- **CrewAI** (multi-agent orchestration)
- **LangGraph** (workflow graph + state transitions)
- **LangChain** (document loaders / splitters / retrieval helpers)
- **Pinecone** (vector database) *(optional — can swap to FAISS/Chroma)*
- LLM provider: OpenAI / Anthropic / Gemini
- **uv** for dependency management

---

## Project structure

```text
stock-picker-agent/
├── src/
│   ├── ai_stock_picker_agent/
│   │   ├── config/
│   │   │   ├── agents.yaml
│   │   │   └── tasks.yaml
│   │   ├── crew.py                 # CrewAI agents + tasks wiring
│   │   ├── graph.py                # LangGraph workflow (if enabled)
│   │   ├── tools/                  # Serper, fundamentals, RAG, etc.
│   │   └── main.py                 # entrypoint
├── data/
│   ├── raw/                        # optional ingested docs
│   └── processed/                  # optional embeddings / chunked docs
├── outputs/                        # generated rankings + reports
├── pyproject.toml
└── README.md
````

---

## Quick Start (uv)

### 1) Clone

```bash
git clone https://github.com/<YOUR_GITHUB_ORG>/stock-picker-agent.git
cd stock-picker-agent
```

### 2) Install `uv`

```bash
pip install uv
```

### 3) Create environment + install dependencies

```bash
uv sync
```

### 4) Configure environment variables

Create a `.env` file in the repo root:

```bash
# LLM provider (choose one)
OPENAI_API_KEY="..."
# or:
ANTHROPIC_API_KEY="..."
# or:
GEMINI_API_KEY="..."

# Optional: web search (Serper)
SERPER_API_KEY="..."

# Optional: Pinecone (RAG)
PINECONE_API_KEY="..."
PINECONE_INDEX="stock-picker"
PINECONE_ENVIRONMENT="..."  # if required by your Pinecone setup

# Optional: tracing / debugging
CREWAI_TRACING_ENABLED=false
```

### 5) Run

Option A — run via module:

```bash
uv run python -m ai_stock_picker_agent.main
```

Option B — if you expose a CLI entrypoint:

```bash
uv run stock-picker
```

---

## Usage

### Common inputs

Most runs accept a small set of parameters (passed in `main.py` or CLI flags):

* `sector` — e.g. `"AI"`, `"Healthcare"`, `"Energy"`
* `investment_style` — `"value" | "growth" | "momentum" | "dividend"`
* `max_candidates` — e.g. `5`
* `time_window_days` — e.g. `7`
* `universe` — e.g. `"US"`, `"S&P 500"`, or a ticker list

Example:

```bash
uv run python -m ai_stock_picker_agent.main \
  --sector "AI" \
  --investment-style "growth" \
  --max-candidates 5 \
  --time-window-days 7
```

> If you don’t have CLI flags yet, add them in `src/ai_stock_picker_agent/main.py` using `argparse` and pass the inputs into `crew().kickoff(inputs=...)`.

---

## RAG setup (Pinecone)

This project supports RAG so the model can cite your documents (transcripts, filings, notes).

### 1) Ingest documents (optional)

Put PDFs/text/markdown in `data/raw/` and run:

```bash
uv run python -m ai_stock_picker_agent.tools.ingest_docs --input data/raw --out data/processed
```

### 2) Build embeddings + upsert to Pinecone

```bash
uv run python -m ai_stock_picker_agent.tools.build_index \
  --processed data/processed \
  --index "$PINECONE_INDEX"
```

### 3) Run research

Once indexed, the Retriever agent will pull top-k chunks per ticker and use them as grounded context.

> Don’t want Pinecone? Swap the retriever to FAISS/Chroma and keep the same tool interface.

---

## How CrewAI and LangGraph are used together

### CrewAI (agents + tools)

* Defines agent roles, goals, and tool access.
* Great for “who does what” (analyst team simulation).

### LangGraph (workflow)

* Defines a graph like:
  `discover -> retrieve -> analyze -> score -> rank -> write_outputs`
* Great for:

  * deterministic execution order
  * branching (e.g., skip fundamentals if missing)
  * retries and guardrails
  * auditing intermediate state

> If you only need one: start with CrewAI. Add LangGraph when you need stricter control, branching, or debuggability.

---

## Guardrails and limitations

* Outputs depend on source coverage (news and your RAG corpus).
* LLM scoring is approximate; treat scores as heuristic.
* Avoid large time windows / huge candidate lists or you can hit token limits.
* Consider rate limiting and caching for news + document retrieval.

---

## Troubleshooting

### `KeyError: Template variable 'start_date' not found`

Your task prompt references `{start_date}` / `{end_date}` but inputs don’t include them.
Fix: add them to your `inputs` in `main.py`, or remove variables from task text.

### `RateLimitError: Request too large ... tokens per min`

Reduce:

* `max_candidates`
* `time_window_days`
* number of retrieved chunks (`top_k`)
  Also, split your workflow: generate a short “research pack” first, then rank.

### macOS ARM: `onnxruntime-gpu` cannot be installed

`onnxruntime-gpu` wheels are not available for macOS arm64. Use CPU (`onnxruntime`) or gate GPU deps by platform in `pyproject.toml`.

---

## Roadmap

* [ ] Add SEC/EDGAR ingestion (10-K, 10-Q)
* [ ] Add earnings transcript loader + chunker
* [ ] Add fundamentals provider integration (yfinance / FMP / Polygon)
* [ ] Add evaluation harness (precision of picks vs benchmark, ablation)
* [ ] Add portfolio constraints and risk budgeting

---

## Related projects

* **CrewAI version:** [<CREWAI_REPO_URL>](https://github.com/Crazy-Horse/crewai-multi-agent-research)
* **LangGraph version:** [<LANGGRAPH_REPO_URL>](https://github.com/Crazy-Horse/multi-agent-research)

---

## License

MIT

```

