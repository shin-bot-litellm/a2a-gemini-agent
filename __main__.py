"""Entry point for the A2A Gemini Agent server."""

import os

import uvicorn
from dotenv import load_dotenv

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from agent_executor import GeminiAgentExecutor


load_dotenv()


def main():
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8001"))

    skill = AgentSkill(
        id="gemini_assistant",
        name="Gemini Assistant",
        description="A helpful AI assistant powered by Gemini with Google Search.",
        tags=["gemini", "search", "assistant"],
        examples=["What's the weather like today?", "Tell me about quantum computing"],
    )

    agent_card = AgentCard(
        name="Gemini Agent",
        description="A helpful AI assistant powered by Google Gemini.",
        url=f"http://{host}:{port}/",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )

    request_handler = DefaultRequestHandler(
        agent_executor=GeminiAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    uvicorn.run(server.build(), host=host, port=port)


if __name__ == "__main__":
    main()
