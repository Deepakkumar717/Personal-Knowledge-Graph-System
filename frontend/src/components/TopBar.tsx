import React, { useState, useEffect, useRef } from 'react';
import { Search, Plus, Network, FileText, Hash, Database, Download, Upload, Trash2, Edit3, ChevronDown, Sparkles, History, Archive, BarChart2 } from 'lucide-react';
import { searchApi, AutocompleteItem } from '../api';

interface TopBarProps {
  onNewNote: () => void;
  onSelectNote: (id: number) => void;
  onSelectTag: (tag: string) => void;
  isEditMode: boolean;
  onToggleEditMode: () => void;
  onOpenExportImport: () => void;
  onResetDatabase: () => void;
  onOpenTrash?: () => void;
  onOpenActivity?: () => void;
  onOpenInsights?: () => void;
  sseStatus?: 'connected' | 'reconnecting' | 'disconnected';
  searchInputRef: React.RefObject<HTMLInputElement>;
}

export const TopBar: React.FC<TopBarProps> = ({
  onNewNote,
  onSelectNote,
  onSelectTag,
  isEditMode,
  onToggleEditMode,
  onOpenExportImport,
  onResetDatabase,
  onOpenTrash,
  onOpenActivity,
  onOpenInsights,
  sseStatus = 'connected',
  searchInputRef,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [suggestions, setSuggestions] = useState<AutocompleteItem[]>([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [showDataMenu, setShowDataMenu] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const dataMenuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!searchQuery.trim()) {
      setSuggestions([]);
      setShowDropdown(false);
      return;
    }

    const timer = setTimeout(async () => {
      try {
        const res = await searchApi.autocomplete(searchQuery);
        setSuggestions(res.results);
        setShowDropdown(res.results.length > 0);
      } catch (err) {
        console.error('Autocomplete error:', err);
      }
    }, 200);

    return () => clearTimeout(timer);
  }, [searchQuery]);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(e.target as Node) &&
        searchInputRef.current &&
        !searchInputRef.current.contains(e.target as Node)
      ) {
        setShowDropdown(false);
      }
      if (dataMenuRef.current && !dataMenuRef.current.contains(e.target as Node)) {
        setShowDataMenu(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [searchInputRef]);

  const handleSelectSuggestion = (item: AutocompleteItem) => {
    setShowDropdown(false);
    setSearchQuery('');
    if (item.type === 'note' && item.id) {
      onSelectNote(item.id);
    } else if (item.type === 'tag') {
      const cleanTag = item.title.replace(/^#/, '');
      onSelectTag(cleanTag);
    }
  };

  return (
    <header
      style={{
        height: '56px',
        backgroundColor: 'var(--bg)',
        borderBottom: '1px solid var(--border)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 20px',
        gap: '16px',
        zIndex: 100,
        position: 'relative',
        flexWrap: 'nowrap',
      }}
    >
      {/* Brand / Logo */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexShrink: 0 }}>
        <div
          style={{
            width: '34px',
            height: '34px',
            backgroundColor: 'var(--accent-soft)',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius-md)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--primary)',
          }}
        >
          <Network size={20} />
        </div>
        <div>
          <h1 style={{ fontSize: '18px', fontWeight: 700, color: 'var(--text)', lineHeight: 1.2 }}>
            Personal Knowledge Graph
          </h1>
          <p style={{ fontSize: '11px', color: 'var(--muted)', fontWeight: 500 }}>
            Deterministic &bull; Rule-based IR
          </p>
        </div>
      </div>

      {/* Global Search Bar with Autocomplete */}
      <div style={{ flex: 1, maxWidth: '520px', position: 'relative' }}>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            backgroundColor: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius-md)',
            padding: '0 12px',
            height: '38px',
          }}
        >
          <Search size={16} color="var(--muted)" style={{ marginRight: '8px' }} />
          <input
            ref={searchInputRef}
            type="text"
            placeholder="Search notes or #tags... (Press '/' to focus)"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onFocus={() => suggestions.length > 0 && setShowDropdown(true)}
            style={{
              flex: 1,
              border: 'none',
              outline: 'none',
              background: 'transparent',
              color: 'var(--text)',
              fontSize: '14px',
            }}
          />
        </div>

        {/* Autocomplete dropdown */}
        {showDropdown && (
          <div
            ref={dropdownRef}
            style={{
              position: 'absolute',
              top: '44px',
              left: 0,
              right: 0,
              backgroundColor: 'var(--bg)',
              border: '1px solid var(--border)',
              borderRadius: 'var(--radius-md)',
              boxShadow: 'var(--shadow-lg)',
              maxHeight: '320px',
              overflowY: 'auto',
              zIndex: 1000,
            }}
          >
            {suggestions.map((item, idx) => (
              <div
                key={idx}
                onClick={() => handleSelectSuggestion(item)}
                style={{
                  padding: '10px 14px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  cursor: 'pointer',
                  borderBottom: idx < suggestions.length - 1 ? '1px solid var(--surface)' : 'none',
                  transition: 'background-color 0.1s',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = 'var(--accent-soft)')}
                onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = 'transparent')}
              >
                {item.type === 'note' ? (
                  <FileText size={16} color="var(--primary)" />
                ) : (
                  <Hash size={16} color="var(--primary-dark)" />
                )}
                <span style={{ flex: 1, fontSize: '14px', fontWeight: 500 }}>
                  {item.title}
                </span>
                <span
                  style={{
                    fontSize: '11px',
                    padding: '2px 6px',
                    backgroundColor: item.type === 'note' ? 'var(--accent-soft)' : '#FCE7F3',
                    color: item.type === 'note' ? 'var(--primary-dark)' : '#DB2777',
                    borderRadius: '4px',
                    textTransform: 'uppercase',
                    fontWeight: 600,
                  }}
                >
                  {item.type}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexShrink: 0 }}>
        {/* Real-time Live indicator */}
        <div
          title={sseStatus === 'connected' ? 'Real-time SSE: Live & Connected' : 'Real-time SSE: Reconnecting...'}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            padding: '5px 11px',
            borderRadius: '16px',
            backgroundColor: sseStatus === 'connected' ? '#ECFDF5' : '#FFFBEB',
            border: `1px solid ${sseStatus === 'connected' ? '#A7F3D0' : '#FDE68A'}`,
            fontSize: '12px',
            fontWeight: 600,
            color: sseStatus === 'connected' ? '#065F46' : '#92400E',
          }}
        >
          <span
            style={{
              width: '8px',
              height: '8px',
              borderRadius: '50%',
              backgroundColor: sseStatus === 'connected' ? '#10B981' : '#F59E0B',
              boxShadow: sseStatus === 'connected' ? '0 0 6px #10B981' : 'none',
            }}
          />
          <span>{sseStatus === 'connected' ? 'Live' : 'Reconnecting...'}</span>
        </div>

        {/* Insights Button */}
        {onOpenInsights && (
          <button
            onClick={onOpenInsights}
            title="Open knowledge graph insights & charts"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '0 12px',
              height: '38px',
              backgroundColor: 'var(--surface)',
              color: 'var(--text)',
              border: '1px solid var(--border)',
              borderRadius: 'var(--radius-md)',
              fontWeight: 600,
              fontSize: '13px',
              cursor: 'pointer',
            }}
          >
            <BarChart2 size={15} color="var(--primary)" />
            <span>Insights</span>
          </button>
        )}

        {/* Edit Mode Toggle */}
        <button
          onClick={onToggleEditMode}
          title="Toggle interactive graph edit mode (E)"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            padding: '0 12px',
            height: '38px',
            backgroundColor: isEditMode ? 'var(--primary)' : 'var(--surface)',
            color: isEditMode ? '#FFFFFF' : 'var(--text)',
            border: `1px solid ${isEditMode ? 'var(--primary-dark)' : 'var(--border)'}`,
            borderRadius: 'var(--radius-md)',
            fontWeight: 600,
            fontSize: '13px',
          }}
        >
          <Edit3 size={15} />
          <span>Edit Mode</span>
        </button>

        {/* Data Menu Dropdown */}
        <div style={{ position: 'relative' }} ref={dataMenuRef}>
          <button
            onClick={() => setShowDataMenu(!showDataMenu)}
            title="Export, import, or manage data"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '0 12px',
              height: '38px',
              backgroundColor: 'var(--surface)',
              color: 'var(--text)',
              border: '1px solid var(--border)',
              borderRadius: 'var(--radius-md)',
              fontWeight: 500,
              fontSize: '13px',
            }}
          >
            <Database size={15} color="var(--primary)" />
            <span>Data</span>
            <ChevronDown size={14} color="var(--muted)" />
          </button>

          {showDataMenu && (
            <div
              style={{
                position: 'absolute',
                top: '44px',
                right: 0,
                backgroundColor: 'var(--bg)',
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius-md)',
                boxShadow: 'var(--shadow-lg)',
                minWidth: '200px',
                padding: '6px 0',
                zIndex: 1000,
              }}
            >
              {onOpenTrash && (
                <div
                  onClick={() => {
                    setShowDataMenu(false);
                    onOpenTrash();
                  }}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '9px 14px',
                    fontSize: '13px',
                    cursor: 'pointer',
                    color: 'var(--text)',
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = 'var(--accent-soft)')}
                  onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = 'transparent')}
                >
                  <Archive size={14} color="var(--primary)" />
                  <span>Trash Bin</span>
                </div>
              )}

              {onOpenActivity && (
                <div
                  onClick={() => {
                    setShowDataMenu(false);
                    onOpenActivity();
                  }}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '9px 14px',
                    fontSize: '13px',
                    cursor: 'pointer',
                    color: 'var(--text)',
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = 'var(--accent-soft)')}
                  onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = 'transparent')}
                >
                  <History size={14} color="var(--primary)" />
                  <span>Activity & Backups</span>
                </div>
              )}

              <div style={{ height: '1px', backgroundColor: 'var(--border)', margin: '4px 0' }} />

              <div
                onClick={() => {
                  setShowDataMenu(false);
                  onOpenExportImport();
                }}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '9px 14px',
                  fontSize: '13px',
                  cursor: 'pointer',
                  color: 'var(--text)',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = 'var(--accent-soft)')}
                onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = 'transparent')}
              >
                <Download size={14} color="var(--primary)" />
                <span>Export / Import JSON</span>
              </div>

              <div style={{ height: '1px', backgroundColor: 'var(--border)', margin: '4px 0' }} />

              <div
                onClick={() => {
                  setShowDataMenu(false);
                  onResetDatabase();
                }}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '9px 14px',
                  fontSize: '13px',
                  cursor: 'pointer',
                  color: 'var(--danger)',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#FFF1F2')}
                onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = 'transparent')}
              >
                <Trash2 size={14} color="var(--danger)" />
                <span>Reset Database</span>
              </div>
            </div>
          )}
        </div>

        {/* New Note Button */}
        <button
          onClick={onNewNote}
          title="Create a new note (N)"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            padding: '0 16px',
            height: '38px',
            backgroundColor: 'var(--primary)',
            color: '#FFFFFF',
            border: '1px solid var(--primary-dark)',
            borderRadius: 'var(--radius-md)',
            fontWeight: 600,
            fontSize: '14px',
            boxShadow: 'var(--shadow-sm)',
          }}
        >
          <Plus size={16} />
          <span>New Note</span>
        </button>
      </div>
    </header>
  );
};
