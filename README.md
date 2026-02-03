# A2A Gemini Agent

A simple, deployable [A2A (Agent-to-Agent)](https://github.com/a2aproject/a2a-samples) agent powered by Google Gemini via the [Agent Development Kit (ADK)](https://google.github.io/adk-docs/).

Based on the [a2a-samples](https://github.com/a2aproject/a2a-samples) project.

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set your Gemini API key

```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

Get a key at: https://aistudio.google.com/apikey

### 3. Run the agent

```bash
python __main__.py
```

### 4. Test it

```bash
python test_client.py
```

Or hit the agent card endpoint directly:

```bash
curl http://localhost:8001/.well-known/agent.json
```

## Docker

```bash
docker build -t a2a-gemini-agent .
docker run -p 8001:8001 -e GOOGLE_API_KEY=your_key_here a2a-gemini-agent
```

## Deploy to Railway / Render / Fly.io

Set the environment variable `GOOGLE_API_KEY` and deploy. The `PORT` env var is respected automatically.

## Streaming

This agent supports both `message/send` and `message/stream`. To stream:

```bash
curl -X POST http://localhost:8001/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "message/stream",
    "params": {
      "message": {
        "role": "user",
        "messageId": "msg-001",
        "parts": [{"kind": "text", "text": "Tell me a joke"}]
      }
    }
  }'
```

## What's Inside

- `agent.py` — Gemini agent with Google Search tool + streaming
- `agent_executor.py` — A2A executor bridging ADK ↔ A2A protocol
- `__main__.py` — Server entry point with agent card config
- `test_client.py` — Simple A2A client to test the agent
- `Dockerfile` — Container-ready
- `requirements.txt` — Dependencies

## License

Apache 2.0 (based on [a2a-samples](https://github.com/a2aproject/a2a-samples))
