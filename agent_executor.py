"""A2A AgentExecutor with true progressive token streaming."""

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    Part,
    Task,
    TaskState,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils import new_agent_text_message, new_task
from a2a.utils.errors import ServerError
from agent import GeminiAgent


class GeminiAgentExecutor(AgentExecutor):
    """Executor that streams token-by-token as SSE artifact-update events."""

    def __init__(self) -> None:
        self.agent = GeminiAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        query = context.get_user_input()
        task = context.current_task

        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.context_id)

        async for is_final, text in self.agent.stream(query, task.context_id):
            if is_final:
                await updater.complete()
                break

            # Send each chunk as an artifact-update SSE event
            await updater.add_artifact(
                [Part(root=TextPart(text=text))],
                name="response",
            )

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> Task | None:
        raise ServerError(error=UnsupportedOperationError())
