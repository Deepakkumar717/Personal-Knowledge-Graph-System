import React, { useState } from 'react';
import { systemApi } from '../api';
import { useToast } from '../context/ToastContext';
import { Download, Upload, X, CheckCircle, FileText } from 'lucide-react';

interface ExportImportModalProps {
  isOpen: boolean;
  onClose: () => void;
  onRefreshAll: () => void;
}

export const ExportImportModal: React.FC<ExportImportModalProps> = ({ isOpen, onClose, onRefreshAll }) => {
  const { showToast } = useToast();
  const [importJsonText, setImportJsonText] = useState('');
  const [importSummary, setImportSummary] = useState<any | null>(null);
  const [isExporting, setIsExporting] = useState(false);
  const [isImporting, setIsImporting] = useState(false);

  if (!isOpen) return null;

  const handleExport = async () => {
    setIsExporting(true);
    try {
      const data = await systemApi.exportData();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `knowledge_graph_backup_${new Date().toISOString().slice(0, 10)}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
      showToast({ type: 'success', message: 'Export downloaded successfully!' });
    } catch (err: any) {
      showToast({ type: 'error', message: err.message });
    } finally {
      setIsExporting(false);
    }
  };

  const handleImport = async () => {
    if (!importJsonText.trim()) {
      showToast({ type: 'error', message: 'Please provide JSON content to import.' });
      return;
    }

    let parsed;
    try {
      parsed = JSON.parse(importJsonText);
    } catch (err) {
      showToast({ type: 'error', message: 'Invalid JSON format.' });
      return;
    }

    setIsImporting(true);
    try {
      const summary = await systemApi.importData(parsed);
      setImportSummary(summary);
      showToast({ type: 'success', message: 'Import completed successfully!' });
      onRefreshAll();
    } catch (err: any) {
      showToast({ type: 'error', message: err.message });
    } finally {
      setIsImporting(false);
    }
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      const text = event.target?.result as string;
      setImportJsonText(text);
    };
    reader.readAsText(file);
  };

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.4)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 10000,
      }}
    >
      <div
        style={{
          width: '540px',
          maxHeight: '90vh',
          backgroundColor: 'var(--bg)',
          borderRadius: 'var(--radius-lg)',
          border: '1px solid var(--border)',
          boxShadow: 'var(--shadow-lg)',
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
          <h2 style={{ fontSize: '16px', fontWeight: 700, color: 'var(--text)' }}>
            Export / Import Knowledge Graph
          </h2>
          <button onClick={onClose} style={{ background: 'none', border: 'none', color: 'var(--muted)', cursor: 'pointer' }}>
            <X size={20} />
          </button>
        </div>

        {/* Content */}
        <div style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '20px', overflowY: 'auto' }}>
          {/* Export Section */}
          <div style={{ padding: '16px', backgroundColor: 'var(--surface)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border)' }}>
            <h3 style={{ fontSize: '14px', fontWeight: 600, marginBottom: '6px' }}>Export Graph Data</h3>
            <p style={{ fontSize: '13px', color: 'var(--muted)', marginBottom: '12px' }}>
              Download all notes, links, tags, and graph structure as a JSON file.
            </p>
            <button
              onClick={handleExport}
              disabled={isExporting}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '8px 16px',
                backgroundColor: 'var(--accent)',
                color: '#FFFFFF',
                border: '1px solid var(--accent-dark)',
                borderRadius: 'var(--radius-sm)',
                fontWeight: 600,
                fontSize: '13px',
              }}
            >
              <Download size={15} />
              <span>{isExporting ? 'Exporting...' : 'Download JSON Backup'}</span>
            </button>
          </div>

          {/* Import Section */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <h3 style={{ fontSize: '14px', fontWeight: 600 }}>Import Graph Data</h3>
            <p style={{ fontSize: '13px', color: 'var(--muted)' }}>
              Upload a JSON file or paste JSON data below. Duplicate notes will be safely skipped.
            </p>

            <input
              type="file"
              accept=".json,application/json"
              onChange={handleFileUpload}
              style={{ fontSize: '13px', padding: '6px' }}
            />

            <textarea
              placeholder="Or paste JSON payload here..."
              value={importJsonText}
              onChange={(e) => setImportJsonText(e.target.value)}
              style={{
                width: '100%',
                height: '140px',
                padding: '10px',
                fontFamily: 'monospace',
                fontSize: '12px',
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius-md)',
                backgroundColor: 'var(--bg)',
                outline: 'none',
              }}
            />

            <button
              onClick={handleImport}
              disabled={isImporting || !importJsonText.trim()}
              style={{
                alignSelf: 'flex-start',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '8px 16px',
                backgroundColor: isImporting || !importJsonText.trim() ? 'var(--muted)' : 'var(--accent)',
                color: '#FFFFFF',
                border: 'none',
                borderRadius: 'var(--radius-sm)',
                fontWeight: 600,
                fontSize: '13px',
                cursor: isImporting || !importJsonText.trim() ? 'not-allowed' : 'pointer',
              }}
            >
              <Upload size={15} />
              <span>{isImporting ? 'Importing...' : 'Import Data'}</span>
            </button>

            {/* Import Summary */}
            {importSummary && (
              <div
                style={{
                  marginTop: '12px',
                  padding: '12px',
                  backgroundColor: 'var(--accent-soft)',
                  border: '1px solid var(--border)',
                  borderRadius: 'var(--radius-md)',
                  fontSize: '13px',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: 700, color: 'var(--accent-dark)', marginBottom: '4px' }}>
                  <CheckCircle size={16} />
                  <span>Import Summary:</span>
                </div>
                <p>• Notes imported: <strong>{importSummary.imported_notes}</strong> (Skipped duplicate: {importSummary.skipped_notes})</p>
                <p>• Links imported: <strong>{importSummary.imported_links}</strong> (Skipped duplicate: {importSummary.skipped_links})</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
