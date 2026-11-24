# AI Agents Intro: Study Guide Generator

A small AI agent system built with Python, Google ADK, LiteLLM and Ollama.

## Model Provider

- **Provider:** Ollama (local)
- **Model:** `llama3.2:1b`
- **Connector:** LiteLLM (`ollama_chat/llama3.2:1b`)

## Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install Ollama (https://ollama.com) and pull the model:

   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull llama3.2:1b
   ```

4. Test the model directly:

   ```bash
   ollama run llama3.2:1b "Say hello in one short sentence."
   ```

5. Create your local `.env` file from the example:

   ```bash
   cp .env.example .env
   ```

   The real `.env` is ignored by Git and must never be committed.

## Configuration

| Variable | Description |
|----------|-------------|
| `OLLAMA_API_BASE` | Address of the local Ollama server |
| `MODEL_NAME` | LiteLLM model name (`ollama_chat/<model>`) |
