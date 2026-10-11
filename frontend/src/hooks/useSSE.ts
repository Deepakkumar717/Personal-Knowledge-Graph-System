import { useEffect, useState, useRef } from 'react';

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export type SSEStatus = 'connected' | 'reconnecting' | 'disconnected';

export function useSSE(onEvent: (event: string, data: any) => void) {
  const [status, setStatus] = useState<SSEStatus>('disconnected');
  const onEventRef = useRef(onEvent);
  onEventRef.current = onEvent;

  useEffect(() => {
    let eventSource: EventSource | null = null;
    let reconnectTimeout: any = null;
    let isMounted = true;

    function connect() {
      if (!isMounted) return;

      try {
        eventSource = new EventSource(`${baseURL}/events`);

        eventSource.onopen = () => {
          if (isMounted) {
            setStatus('connected');
          }
        };

        eventSource.onmessage = (e) => {
          try {
            const parsed = JSON.parse(e.data);
            if (isMounted && status !== 'connected') {
              setStatus('connected');
            }
            if (parsed.event && onEventRef.current) {
              onEventRef.current(parsed.event, parsed.data);
            }
          } catch (err) {
            console.error('Failed to parse SSE payload:', err);
          }
        };

        eventSource.onerror = () => {
          if (isMounted) {
            setStatus('reconnecting');
          }
          if (eventSource) {
            eventSource.close();
            eventSource = null;
          }
          // Attempt reconnection after 1.5 seconds
          if (isMounted) {
            reconnectTimeout = setTimeout(connect, 1500);
          }
        };
      } catch (err) {
        if (isMounted) {
          setStatus('reconnecting');
          reconnectTimeout = setTimeout(connect, 2000);
        }
      }
    }

    connect();

    return () => {
      isMounted = false;
      if (reconnectTimeout) clearTimeout(reconnectTimeout);
      if (eventSource) {
        eventSource.close();
      }
      setStatus('disconnected');
    };
  }, []);

  return {
    status,
    isConnected: status === 'connected',
  };
}
