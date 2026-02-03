"""Gemini agent using google.genai directly for true token-level streaming."""

from collections.abc import AsyncIterable

from google import genai
from google.genai import types


class GeminiAgent:
    """Streams tokens progressively from Gemini."""

    def __init__(self, model: str = "gemini-2.5-flash-lite") -> None:
        self._model = model
        self._client = genai.Client()
        self._system_instruction = (
            "You are a helpful AI assistant. Answer questions clearly and concisely."
        )
        # Track conversation history per session
        self._sessions: dict[str, list[types.Content]] = {}

    async def stream(
        self, query: str, session_id: str
    ) -> AsyncIterable[tuple[bool, str]]:
        """Yield (is_final, text_chunk) tuples as tokens arrive from Gemini."""

        # Get or create session history
        if session_id not in self._sessions:
            self._sessions[session_id] = []

        history = self._sessions[session_id]

        # Add user message to history
        user_content = types.Content(
            role="user", parts=[types.Part.from_text(text=query)]
        )
        history.append(user_content)

        # Stream from Gemini
        full_response = ""
        response_stream = await self._client.aio.models.generate_content_stream(
            model=self._model,
            contents=history,
            config=types.GenerateContentConfig(
                system_instruction=self._system_instruction,
            ),
        )
        async for chunk in response_stream:
            if chunk.text:
                full_response += chunk.text
                yield (False, chunk.text)

        # Add assistant response to history
        history.append(
            types.Content(
                role="model", parts=[types.Part.from_text(text=full_response)]
            )
        )

        # Final signal
        yield (True, "")
