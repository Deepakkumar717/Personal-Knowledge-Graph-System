import asyncio
import json
from typing import AsyncGenerator, Set

class EventService:
    def __init__(self):
        self._subscribers: Set[asyncio.Queue] = set()

    def subscribe(self) -> asyncio.Queue:
        """Register a new SSE client subscriber."""
        queue = asyncio.Queue()
        self._subscribers.add(queue)
        return queue

    def unsubscribe(self, queue: asyncio.Queue) -> None:
        """Unregister an SSE client subscriber."""
        self._subscribers.discard(queue)

    async def broadcast(self, event_type: str, data: dict) -> None:
        """Broadcast an event payload to all active SSE subscribers."""
        payload = json.dumps({"event": event_type, "data": data})
        for queue in list(self._subscribers):
            try:
                await queue.put(payload)
            except Exception:
                self._subscribers.discard(queue)

    async def event_generator(self) -> AsyncGenerator[str, None]:
        """Async generator yielding SSE formatted messages."""
        queue = self.subscribe()
        try:
            while True:
                try:
                    data = await asyncio.wait_for(queue.get(), timeout=15.0)
                    yield f"data: {data}\n\n"
                except asyncio.TimeoutError:
                    yield ": ping\n\n"
        except (asyncio.CancelledError, GeneratorExit):
            pass
        finally:
            self.unsubscribe(queue)

event_service = EventService()
