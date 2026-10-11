import React from 'react';
import { useToast } from '../context/ToastContext';
import { CheckCircle, AlertCircle, Info, X } from 'lucide-react';

export const ToastContainer: React.FC = () => {
  const { toasts, removeToast } = useToast();

  if (toasts.length === 0) return null;

  return (
    <div
      style={{
        position: 'fixed',
        bottom: '24px',
        right: '24px',
        zIndex: 9999,
        display: 'flex',
        flexDirection: 'column',
        gap: '8px',
        maxWidth: '400px',
      }}
    >
      {toasts.map((t) => (
        <div
          key={t.id}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            padding: '12px 16px',
            backgroundColor: 'var(--bg)',
            color: 'var(--text)',
            borderRadius: 'var(--radius-md)',
            border: `1px solid ${
              t.type === 'error'
                ? 'var(--danger)'
                : t.type === 'success'
                ? 'var(--success)'
                : 'var(--border)'
            }`,
            boxShadow: 'var(--shadow-lg)',
            fontSize: '14px',
            animation: 'slideIn 0.2s ease-out',
          }}
        >
          {t.type === 'success' && <CheckCircle size={18} color="var(--success)" />}
          {t.type === 'error' && <AlertCircle size={18} color="var(--danger)" />}
          {t.type === 'info' && <Info size={18} color="var(--accent)" />}

          <span style={{ flex: 1 }}>{t.message}</span>

          {t.actionLabel && t.onAction && (
            <button
              onClick={() => {
                t.onAction?.();
                removeToast(t.id);
              }}
              style={{
                backgroundColor: 'var(--accent-soft)',
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius-sm)',
                padding: '4px 8px',
                fontWeight: 600,
                color: 'var(--accent-dark)',
                cursor: 'pointer',
              }}
            >
              {t.actionLabel}
            </button>
          )}

          <button
            onClick={() => removeToast(t.id)}
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              color: 'var(--muted)',
            }}
          >
            <X size={16} />
          </button>
        </div>
      ))}
    </div>
  );
};
