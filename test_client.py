"""Simple test client to verify the A2A agent is working."""

import asyncio

from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    MessageSendParams,
    SendMessageRequest,
    TextPart,
    Part,
)
from uuid import uuid4


async def main():
    base_url = "http://localhost:8001"

    # Resolve agent card
    resolver = A2ACardResolver(base_url=base_url)
    card = await resolver.get_agent_card()
    print(f"Connected to: {card.name}")
    print(f"Description: {card.description}")
    print(f"Skills: {[s.name for s in card.skills]}")
    print()

    # Create client and send a message
    client = A2AClient(agent_card=card)

    request = SendMessageRequest(
        id=str(uuid4()),
        params=MessageSendParams(
            message={
                "role": "user",
                "parts": [{"kind": "text", "text": "What are 3 interesting facts about the moon?"}],
                "messageId": str(uuid4()),
            }
        ),
    )

    print("Sending message...")
    response = await client.send_message(request)
    print(f"Response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
