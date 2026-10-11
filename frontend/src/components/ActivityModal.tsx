import React, { useState, useEffect } from 'react';
import { ActivityLogRead, BackupItemRead, systemApi } from '../api';
import { useToast } from '../context/ToastContext';
import { History, HardDrive, RotateCcw, X, Clock, Database, CheckCircle2 } from 'lucide-react';

interface ActivityModalProps {
  isOpen: boolean;
  onClose: () => void;
  onRefreshAll: () => void;
}

export const ActivityModal: React.FC<ActivityModalProps> = ({ isOpen, onClose, onRefreshAll }) => {
  const { showToast } = useToast();
  const [activeTab, setActiveTab] = useState<'activity' | 'backups'>('activity');
  const [activities, setActivities] = useState<ActivityLogRead[]>([]);
  const [backups, setBackups] = useState<BackupItemRead[]>([]);
  const [dbPath, setDbPath] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [restoring, setRestoring] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [act, bkp, health] = await Promise.all([
        systemApi.getActivity(60),
        systemApi.getBackups(),
        systemApi.health(),
      ]);
      setActivities(act);
      setBackups(bkp);
      if (health.database_path) {
        setDbPath(health.database_path);
      }
    } catch (err: any) {
      showToast({ type: 'error', message: `Failed to load system information: ${err.message}` });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchData();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleRestoreBackup = async (filename: string) => {
    if (
      !window.confirm(
        `Are you sure you want to restore snapshot "${filename}"?\n\nThe current database state will be backed up before restoration.`
      )
    ) {
      return;
    }

    setRestoring(filename);
    try {
      const res = await systemApi.restoreBackup(filename);
      showToast({ type: 'success', message: res.message });
      onRefreshAll();
      fetchData();
    } catch (err: any) {
      showToast({ type: 'error', message: `Restore failed: ${err.message}` });
    } finally {
      setRestoring(null);
    }
  };

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
          width: '720px',
          maxWidth: '100%',
          maxHeight: '85vh',
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
                backgroundColor: 'var(--accent-soft)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'var(--primary)',
              }}
            >
              <History size={18} />
            </div>
            <div>
              <h2 style={{ fontSize: '16px', fontWeight: 700, color: 'var(--text)', margin: 0 }}>
                System Activity & Backups
              </h2>
              <p style={{ fontSize: '12px', color: 'var(--muted)', margin: 0 }}>
                Audit trail and automated SQLite database snapshots
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

        {/* DB Path Banner */}
        {dbPath && (
          <div
            style={{
              padding: '8px 20px',
              backgroundColor: 'var(--accent-soft)',
              borderBottom: '1px solid var(--border)',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              fontSize: '11px',
              color: 'var(--primary-dark)',
            }}
          >
            <Database size={13} />
            <span>Active Database File:</span>
            <code
              style={{
                backgroundColor: 'var(--bg)',
                padding: '2px 6px',
                borderRadius: '4px',
                border: '1px solid var(--border)',
                fontWeight: 600,
              }}
            >
              {dbPath}
            </code>
          </div>
        )}

        {/* Tab Switcher */}
        <div
          style={{
            display: 'flex',
            borderBottom: '1px solid var(--border)',
            backgroundColor: 'var(--surface)',
            padding: '0 20px',
          }}
        >
          <button
            onClick={() => setActiveTab('activity')}
            style={{
              padding: '10px 16px',
              border: 'none',
              borderBottom: activeTab === 'activity' ? '2px solid var(--primary)' : '2px solid transparent',
              background: 'transparent',
              color: activeTab === 'activity' ? 'var(--primary)' : 'var(--muted)',
              fontWeight: activeTab === 'activity' ? 700 : 500,
              fontSize: '13px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
            }}
          >
            <History size={14} />
            <span>Activity Log ({activities.length})</span>
          </button>
          <button
            onClick={() => setActiveTab('backups')}
            style={{
              padding: '10px 16px',
              border: 'none',
              borderBottom: activeTab === 'backups' ? '2px solid var(--primary)' : '2px solid transparent',
              background: 'transparent',
              color: activeTab === 'backups' ? 'var(--primary)' : 'var(--muted)',
              fontWeight: activeTab === 'backups' ? 700 : 500,
              fontSize: '13px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
            }}
          >
            <HardDrive size={14} />
            <span>Database Backups ({backups.length})</span>
          </button>
        </div>

        {/* Content Body */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '16px 20px' }}>
          {loading ? (
            <div style={{ padding: '36px', textAlign: 'center', color: 'var(--muted)', fontSize: '13px' }}>
              Loading system data...
            </div>
          ) : activeTab === 'activity' ? (
            activities.length === 0 ? (
              <div style={{ padding: '36px', textAlign: 'center', color: 'var(--muted)', fontSize: '13px' }}>
                No activity logged yet.
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {activities.map((item) => (
                  <div
                    key={item.id}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: '10px 14px',
                      borderRadius: 'var(--radius-sm)',
                      backgroundColor: 'var(--surface)',
                      border: '1px solid var(--border)',
                      fontSize: '12px',
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <span
                        style={{
                          fontSize: '10px',
                          fontWeight: 700,
                          padding: '2px 6px',
                          borderRadius: '4px',
                          textTransform: 'uppercase',
                          backgroundColor:
                            item.action.includes('CREATE')
                              ? '#DEF7EC'
                              : item.action.includes('DELETE')
                              ? '#FEE2E2'
                              : item.action.includes('RESTORE')
                              ? '#FEF08A'
                              : 'var(--accent-soft)',
                          color:
                            item.action.includes('CREATE')
                              ? '#03543F'
                              : item.action.includes('DELETE')
                              ? '#991B1B'
                              : item.action.includes('RESTORE')
                              ? '#854D0E'
                              : 'var(--primary-dark)',
                        }}
                      >
                        {item.action}
                      </span>
                      <span style={{ fontWeight: 600, color: 'var(--text)' }}>
                        {item.entity} {item.entity_id ? `#${item.entity_id}` : ''}
                      </span>
                      {(item.title || item.detail) && (
                        <span style={{ color: 'var(--muted)', fontSize: '11px' }}>
                          {item.title ? `'${item.title}' ` : ''}{item.detail || ''}
                        </span>
                      )}
                    </div>
                    <span style={{ color: 'var(--muted)', fontSize: '11px' }}>
                      {new Date(item.ts).toLocaleString()}
                    </span>
                  </div>
                ))}
              </div>
            )
          ) : backups.length === 0 ? (
            <div style={{ padding: '36px', textAlign: 'center', color: 'var(--muted)', fontSize: '13px' }}>
              No automated backups found.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {backups.map((bkp) => (
                <div
                  key={bkp.filename}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '12px 14px',
                    borderRadius: 'var(--radius-sm)',
                    backgroundColor: 'var(--surface)',
                    border: '1px solid var(--border)',
                  }}
                >
                  <div>
                    <h4 style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text)', margin: '0 0 4px' }}>
                      {bkp.filename}
                    </h4>
                    <div style={{ display: 'flex', gap: '12px', fontSize: '11px', color: 'var(--muted)' }}>
                      <span>Size: {Math.round(bkp.size_bytes / 1024)} KB</span>
                      <span>&bull;</span>
                      <span>Created: {new Date(bkp.created_at).toLocaleString()}</span>
                    </div>
                  </div>

                  <button
                    onClick={() => handleRestoreBackup(bkp.filename)}
                    disabled={restoring === bkp.filename}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '5px',
                      padding: '6px 12px',
                      backgroundColor: 'var(--surface)',
                      color: 'var(--primary)',
                      border: '1px solid var(--primary)',
                      borderRadius: 'var(--radius-sm)',
                      fontSize: '12px',
                      fontWeight: 600,
                      cursor: 'pointer',
                      opacity: restoring === bkp.filename ? 0.6 : 1,
                    }}
                  >
                    <RotateCcw size={13} />
                    <span>{restoring === bkp.filename ? 'Restoring...' : 'Restore'}</span>
                  </button>
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
            justifyContent: 'flex-end',
            backgroundColor: 'var(--surface)',
          }}
        >
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
