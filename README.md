# AI_RESEARCHER

Short, focused agent that searches, reads, and synthesizes research into actionable summaries.

## Highlights
- Automated web/paper search and retrieval
- Source-grounded notes with citations
- Iterative planning and evidence tracking
- Export to Markdown/JSON

## Tech
- Python 3.10+
- LangChain or LlamaIndex
- Vector DB (Chroma/FAISS)
- LLM provider (OpenAI/Anthropic, configurable)
- Optional: SerpAPI, arXiv/Semantic Scholar APIs, Playwright

## Quick start
- Create env: `python -m venv .venv && source .venv/bin/activate`
- Install deps: `pip install -r requirements.txt`
- Configure env: copy `.env.example` to `.env` and set:
    - `OPENAI_API_KEY=...` (or `ANTHROPIC_API_KEY`)
    - `SERPAPI_API_KEY=...` (if using web search)
    - `TAVILY_API_KEY=...` (optional)
- Run: `python -m ai_researcher.cli --query "your topic" --out reports/`

## Usage examples
- Quick brief: `... --query "LLM evaluations beyond benchmarks"`
- Deep dive with max sources: `... --query "RAG evaluation methods" --k 25`
- Resume from cache: `... --query "topic" --cache .cache/topic.json`

## Output
- reports/
    - YYYY-MM-DD-topic.md (executive summary, findings, sources)
    - topic.json (structured notes, quotes, metadata)

## Project structure
- ai_researcher/
    - agents/ tools/ pipelines/ retrieval/ evaluation/
    - cli.py config.py
- data/ reports/ .cache/
- tests/

## Development
- Lint: `ruff check .`
- Format: `ruff format .`
- Test: `pytest -q`
- Type check: `mypy ai_researcher`

## Configuration
- `MODEL_NAME` (e.g., gpt-4o-mini, claude-3-5-sonnet)
- `EMBEDDINGS_MODEL`
- `MAX_TOKENS`, `TEMPERATURE`
- `VECTOR_DB_DIR` (default: .vectorstore)

## Roadmap
- Add PDF parsing with tables/figures
- Deduplication and citation graph
- Agentic browsing with caching
- Evaluation suite for answer faithfulness

## Contributing
- Open an issue, describe change
- PR with tests and concise summary

## License
- MIT (update if different)

## Acknowledgments
- Thanks to the LangChain/LlamaIndex community and open-source tools used here.
