"""A2A AgentExecutor that bridges the Gemini agent with the A2A protocol."""

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
    """Executor that supports both regular and streaming responses."""

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

        async for finished, text in self.agent.stream(query, task.context_id):
            if not finished:
                await updater.update_status(
                    TaskState.working,
                    new_agent_text_message(text, task.context_id, task.id),
                )
                continue

            await updater.add_artifact(
                [Part(root=TextPart(text=text))],
                name="response",
            )
            await updater.complete()
            break

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> Task | None:
        raise ServerError(error=UnsupportedOperationError())
