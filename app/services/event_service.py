import asyncio
import json
from typing import AsyncGenerator, Set, Optional

class EventService:
    def __init__(self, heartbeat_interval: float = 15.0):
        self._subscribers: Set[asyncio.Queue] = set()
        self.heartbeat_interval: float = heartbeat_interval

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

    def broadcast_sync(self, event_type: str, data: dict) -> None:
        """Helper to broadcast synchronously from sync contexts."""
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self.broadcast(event_type, data))
        except RuntimeError:
            asyncio.run(self.broadcast(event_type, data))

    async def event_generator(self, interval: Optional[float] = None) -> AsyncGenerator[str, None]:
        """
        Async generator yielding SSE formatted messages.
        Emits a heartbeat every 15 seconds if no message arrives.
        """
        timeout = interval if interval is not None else self.heartbeat_interval
        queue = self.subscribe()
        try:
            while True:
                try:
                    data = await asyncio.wait_for(queue.get(), timeout=timeout)
                    yield f"data: {data}\n\n"
                except asyncio.TimeoutError:
                    # SSE keepalive comment and heartbeat event
                    yield f": heartbeat\n\ndata: {json.dumps({'event': 'heartbeat', 'data': {}})}\n\n"
        except (asyncio.CancelledError, GeneratorExit):
            pass
        finally:
            self.unsubscribe(queue)

event_service = EventService()

