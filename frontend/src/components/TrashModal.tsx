import React, { useState, useEffect } from 'react';
import { TrashItemRead, trashApi } from '../api';
import { useToast } from '../context/ToastContext';
import { Trash2, RotateCcw, X, AlertOctagon, Clock, ShieldCheck } from 'lucide-react';

interface TrashModalProps {
  isOpen: boolean;
  onClose: () => void;
  onRefreshAll: () => void;
}

export const TrashModal: React.FC<TrashModalProps> = ({ isOpen, onClose, onRefreshAll }) => {
  const { showToast } = useToast();
  const [loading, setLoading] = useState(false);
  const [trashItems, setTrashItems] = useState<TrashItemRead[]>([]);
  const [actionInProgress, setActionInProgress] = useState<number | null>(null);

  const fetchTrash = async () => {
    setLoading(true);
    try {
      const items = await trashApi.list();
      setTrashItems(items);
    } catch (err: any) {
      showToast({ type: 'error', message: `Failed to load trash: ${err.message}` });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchTrash();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleRestore = async (item: TrashItemRead) => {
    setActionInProgress(item.id);
    try {
      const restored = await trashApi.restore(item.id);
      showToast({
        type: 'success',
        message: `Restored "${restored.title}" with links and tags.`,
      });
      fetchTrash();
      onRefreshAll();
    } catch (err: any) {
      showToast({ type: 'error', message: `Restore failed: ${err.message}` });
    } finally {
      setActionInProgress(null);
    }
  };

  const handlePermanentDelete = async (item: TrashItemRead) => {
    if (!window.confirm(`Permanently delete "${item.title}"? This action cannot be undone.`)) {
      return;
    }

    setActionInProgress(item.id);
    try {
      await trashApi.permanentDelete(item.id);
      showToast({ type: 'info', message: `Permanently removed "${item.title}".` });
      fetchTrash();
    } catch (err: any) {
      showToast({ type: 'error', message: `Delete failed: ${err.message}` });
    } finally {
      setActionInProgress(null);
    }
  };

  const handlePurge = async () => {
    try {
      const res = await trashApi.purge();
      showToast({ type: 'info', message: res.message });
      fetchTrash();
    } catch (err: any) {
      showToast({ type: 'error', message: `Purge failed: ${err.message}` });
    }
  };

  function formatTimeRemaining(deletedAtStr: string): string {
    try {
      const deletedAt = new Date(deletedAtStr);
      const expiresAt = new Date(deletedAt.getTime() + 30 * 24 * 60 * 60 * 1000);
      const now = new Date();
      const diffMs = expiresAt.getTime() - now.getTime();
      const diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24));
      if (diffDays <= 0) return 'expires today';
      if (diffDays === 1) return 'expires in 1 day';
      return `expires in ${diffDays} days`;
    } catch {
      return 'expires in 30 days';
    }
  }

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(15, 23, 42, 0.45)',
        backdropFilter: 'blur(2px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 2000,
        padding: '20px',
      }}
    >
      <div
        style={{
          width: '640px',
          maxWidth: '100%',
          maxHeight: '80vh',
          backgroundColor: 'var(--bg)',
          borderRadius: 'var(--radius-lg)',
          boxShadow: 'var(--shadow-lg)',
          border: '1px solid var(--border)',
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
        }}
      >
        {/* Header */}
        <div
          style={{
            padding: '16px 20px',
            borderBottom: '1px solid var(--border)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            backgroundColor: 'var(--surface)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div
              style={{
                width: '32px',
                height: '32px',
                borderRadius: '8px',
                backgroundColor: '#FEE2E2',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#DC2626',
              }}
            >
              <Trash2 size={18} />
            </div>
            <div>
              <h2 style={{ fontSize: '16px', fontWeight: 700, color: 'var(--text)', margin: 0 }}>
                Trash Bin
              </h2>
              <p style={{ fontSize: '12px', color: 'var(--muted)', margin: 0 }}>
                Deleted notes are safely preserved here for 30 days before permanent purging.
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              cursor: 'pointer',
              color: 'var(--muted)',
              padding: '6px',
            }}
          >
            <X size={18} />
          </button>
        </div>

        {/* Content Body */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '16px 20px' }}>
          {loading ? (
            <div style={{ padding: '36px', textAlign: 'center', color: 'var(--muted)', fontSize: '13px' }}>
              Loading trash items...
            </div>
          ) : trashItems.length === 0 ? (
            <div style={{ padding: '40px 20px', textAlign: 'center' }}>
              <ShieldCheck size={36} color="var(--primary)" style={{ margin: '0 auto 12px' }} />
              <h3 style={{ fontSize: '14px', fontWeight: 600, color: 'var(--text)', margin: '0 0 4px' }}>
                Trash is Empty
              </h3>
              <p style={{ fontSize: '12px', color: 'var(--muted)', margin: 0 }}>
                No notes have been deleted. If you ever delete a note, you can restore it here anytime.
              </p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {trashItems.map((item) => (
                <div
                  key={item.id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '12px 14px',
                    borderRadius: 'var(--radius-md)',
                    border: '1px solid var(--border)',
                    backgroundColor: 'var(--surface)',
                  }}
                >
                  <div>
                    <h4 style={{ fontSize: '14px', fontWeight: 600, color: 'var(--text)', margin: '0 0 4px' }}>
                      {item.title}
                    </h4>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', fontSize: '11px', color: 'var(--muted)' }}>
                      <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <Clock size={12} /> Deleted {new Date(item.deleted_at).toLocaleDateString()}
                      </span>
                      <span>&bull;</span>
                      <span style={{ color: '#D97706', fontWeight: 500 }}>
                        {formatTimeRemaining(item.deleted_at)}
                      </span>
                    </div>
                  </div>

                  <div style={{ display: 'flex', gap: '8px' }}>
                    <button
                      onClick={() => handleRestore(item)}
                      disabled={actionInProgress === item.id}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '5px',
                        padding: '6px 12px',
                        backgroundColor: 'var(--primary)',
                        color: '#FFFFFF',
                        border: 'none',
                        borderRadius: 'var(--radius-sm)',
                        fontSize: '12px',
                        fontWeight: 600,
                        cursor: 'pointer',
                        opacity: actionInProgress === item.id ? 0.6 : 1,
                      }}
                    >
                      <RotateCcw size={13} />
                      <span>Restore</span>
                    </button>

                    <button
                      onClick={() => handlePermanentDelete(item)}
                      disabled={actionInProgress === item.id}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '5px',
                        padding: '6px 10px',
                        backgroundColor: 'transparent',
                        color: '#DC2626',
                        border: '1px solid #FECACA',
                        borderRadius: 'var(--radius-sm)',
                        fontSize: '12px',
                        cursor: 'pointer',
                        opacity: actionInProgress === item.id ? 0.6 : 1,
                      }}
                    >
                      <Trash2 size={13} />
                      <span>Delete</span>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div
          style={{
            padding: '12px 20px',
            borderTop: '1px solid var(--border)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            backgroundColor: 'var(--surface)',
          }}
        >
          <button
            onClick={handlePurge}
            style={{
              background: 'none',
              border: 'none',
              fontSize: '12px',
              color: 'var(--muted)',
              cursor: 'pointer',
              textDecoration: 'underline',
            }}
          >
            Purge expired items now
          </button>

          <button
            onClick={onClose}
            style={{
              padding: '6px 14px',
              backgroundColor: 'var(--surface)',
              border: '1px solid var(--border)',
              borderRadius: 'var(--radius-sm)',
              fontSize: '12px',
              fontWeight: 500,
              cursor: 'pointer',
              color: 'var(--text)',
            }}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
