# CLI Chatbot

A terminal chatbot powered by [Ollama](https://ollama.com) (Llama 3) with JSON-based tool calling.

## Features

- **Calculator** — math via `eval`
- **getTime** — current local time and timezone
- **getWeather** — weather for your location (IP geolocation + Open-Meteo; optional OpenWeatherMap API key)

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- [Ollama](https://ollama.com) running locally with the `llama3` model

## Setup

```bash
# Install dependencies
uv sync

# Pull the model (if not already installed)
ollama pull llama3

# Optional: copy env template for OpenWeatherMap instead of default Open-Meteo
cp .env.example .env
```

## Run

```bash
uv run python -u main.py
```

Type `exit` to quit.

## Project structure

| File | Purpose |
|------|---------|
| `main.py` | REPL loop, JSON parsing, tool dispatch |
| `conversation.py` | System prompt and conversation history |
| `llm_client.py` | Ollama streaming client |
| `tools.py` | Tool implementations |

## Tool flow

1. User sends a message
2. LLM returns JSON (`tool` + `arguments`, or `response`)
3. If a tool is requested, it runs and the result is added to history
4. LLM is called again to produce the final answer
