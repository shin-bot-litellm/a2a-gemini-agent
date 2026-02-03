"""Gemini agent using Google ADK with streaming support."""

from collections.abc import AsyncIterable

from google.adk import Runner
from google.adk.agents import LlmAgent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types


def create_agent() -> LlmAgent:
    return LlmAgent(
        name="gemini_agent",
        model="gemini-2.5-flash-lite",
        description="A helpful AI assistant powered by Gemini.",
        instruction=(
            "You are a helpful AI assistant. Answer questions clearly and concisely. "
            "Use Google Search when you need up-to-date information."
        ),
        tools=[google_search],
    )


class GeminiAgent:
    """Wraps the ADK agent with session management and streaming."""

    def __init__(self) -> None:
        self._agent = create_agent()
        self._user_id = "a2a_user"
        self._runner = Runner(
            app_name=self._agent.name,
            agent=self._agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

    async def stream(
        self, query: str, session_id: str
    ) -> AsyncIterable[tuple[bool, str]]:
        session = await self._runner.session_service.get_session(
            app_name=self._agent.name,
            user_id=self._user_id,
            session_id=session_id,
        )
        if session is None:
            session = await self._runner.session_service.create_session(
                app_name=self._agent.name,
                user_id=self._user_id,
                state={},
                session_id=session_id,
            )

        content = types.Content(
            role="user", parts=[types.Part.from_text(text=query)]
        )

        async for event in self._runner.run_async(
            user_id=self._user_id, session_id=session.id, new_message=content
        ):
            if event.is_final_response():
                response = "\n".join(
                    [p.text for p in event.content.parts if p.text]
                )
                yield (True, response)
            else:
                yield (False, "working...")
