"""A2A Agent powered by Google Gemini via the Agent Development Kit (ADK)."""

import os

from google.adk import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.tools import google_search


root_agent = Agent(
    name="gemini_agent",
    model="gemini-2.5-flash-lite",
    description="A helpful AI assistant powered by Gemini.",
    instruction=(
        "You are a helpful AI assistant. Answer questions clearly and concisely. "
        "Use Google Search when you need up-to-date information."
    ),
    tools=[google_search],
)

# Create the A2A ASGI application
a2a_app = to_a2a(root_agent, port=int(os.getenv("PORT", "8001")))
