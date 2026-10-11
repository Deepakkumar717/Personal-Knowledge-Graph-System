import { useEffect } from 'react';

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export function useSSE(onEvent: (event: string, data: any) => void) {
  useEffect(() => {
    let eventSource: EventSource | null = null;
    let reconnectTimeout: any = null;

    function connect() {
      try {
        eventSource = new EventSource(`${baseURL}/events`);

        eventSource.onmessage = (e) => {
          try {
            const parsed = JSON.parse(e.data);
            if (parsed.event) {
              onEvent(parsed.event, parsed.data);
            }
          } catch (err) {
            console.error('Failed to parse SSE payload:', err);
          }
        };

        eventSource.onerror = () => {
          if (eventSource) {
            eventSource.close();
            eventSource = null;
          }
          // Attempt reconnection after 3 seconds
          reconnectTimeout = setTimeout(connect, 3000);
        };
      } catch (err) {
        console.warn('SSE connection failed:', err);
      }
    }

    connect();

    return () => {
      if (reconnectTimeout) clearTimeout(reconnectTimeout);
      if (eventSource) {
        eventSource.close();
      }
    };
  }, [onEvent]);
}
