import React, { useState } from 'react';
import { NoteListItem, TagUsage } from '../api';
import { Pin, ArrowRight, ArrowLeft, Hash, Filter, ArrowDownUp, Plus, FileText, Trash2, X } from 'lucide-react';

interface SidebarProps {
  notes: NoteListItem[];
  tags: TagUsage[];
  selectedNoteId: number | null;
  selectedTag: string | null;
  sortBy: string;
  onSelectNote: (id: number) => void;
  onSelectTag: (tag: string | null) => void;
  onChangeSort: (sort: string) => void;
  onNewNote?: () => void;
  loading: boolean;
}

function formatRelativeTime(dateStr: string): string {
  try {
    const date = new Date(dateStr);
    const now = new Date();
    const diffSec = Math.floor((now.getTime() - date.getTime()) / 1000);
    if (diffSec < 60) return 'just now';
    const diffMin = Math.floor(diffSec / 60);
    if (diffMin < 60) return `${diffMin}m ago`;
    const diffHours = Math.floor(diffMin / 60);
    if (diffHours < 24) return `${diffHours}h ago`;
    const diffDays = Math.floor(diffHours / 24);
    if (diffDays === 1) return 'yesterday';
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
  } catch {
    return '';
  }
}

export const Sidebar: React.FC<SidebarProps> = ({
  notes,
  tags,
  selectedNoteId,
  selectedTag,
  sortBy,
  onSelectNote,
  onSelectTag,
  onChangeSort,
  onNewNote,
  loading,
}) => {
  return (
    <aside
      style={{
        width: '280px',
        minWidth: '280px',
        maxWidth: '280px',
        height: '100%',
        backgroundColor: 'var(--surface)',
        borderRight: '1px solid var(--border)',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
      }}
    >


      {/* Tag Filters Section */}
      <div
        style={{
          padding: '10px 14px 8px',
          borderBottom: '1px solid var(--border)',
          backgroundColor: 'var(--bg)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '11px', fontWeight: 700, color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
            <Filter size={12} color="var(--primary)" />
            <span>Tags Filter</span>
          </div>
          {selectedTag && (
            <button
              onClick={() => onSelectTag(null)}
              style={{
                background: 'none',
                border: 'none',
                fontSize: '11px',
                color: 'var(--primary)',
                cursor: 'pointer',
                fontWeight: 600,
                padding: '0 4px',
              }}
            >
              Clear
            </button>
          )}
        </div>

        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '5px',
            maxHeight: '68px',
            overflowY: 'auto',
          }}
        >
          {tags.length === 0 ? (
            <span style={{ fontSize: '11px', color: 'var(--muted)', fontStyle: 'italic' }}>No tags yet</span>
          ) : (
            tags.map((t) => {
              const isSelected = selectedTag?.toLowerCase() === t.name.toLowerCase();
              return (
                <button
                  key={t.id}
                  onClick={() => onSelectTag(isSelected ? null : t.name)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '3px',
                    padding: '2px 7px',
                    borderRadius: '12px',
                    fontSize: '11px',
                    backgroundColor: isSelected ? 'var(--primary)' : 'var(--accent-soft)',
                    color: isSelected ? '#FFFFFF' : 'var(--primary-dark)',
                    border: `1px solid ${isSelected ? 'var(--primary-dark)' : 'var(--border)'}`,
                    fontWeight: isSelected ? 600 : 500,
                    transition: 'all 0.15s ease',
                  }}
                >
                  <Hash size={10} />
                  <span>{t.name}</span>
                  <span
                    style={{
                      fontSize: '10px',
                      opacity: isSelected ? 0.9 : 0.6,
                      marginLeft: '2px',
                    }}
                  >
                    {t.count}
                  </span>
                </button>
              );
            })
          )}
        </div>
      </div>

      {/* Sort & Count Bar */}
      <div
        style={{
          padding: '8px 14px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          borderBottom: '1px solid var(--border)',
          backgroundColor: 'var(--surface)',
        }}
      >
        <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--muted)' }}>
          {notes.length} {notes.length === 1 ? 'Note' : 'Notes'}
        </span>
        <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
          <ArrowDownUp size={12} color="var(--muted)" />
          <select
            value={sortBy}
            onChange={(e) => onChangeSort(e.target.value)}
            style={{
              padding: '3px 6px',
              border: '1px solid var(--border)',
              borderRadius: 'var(--radius-sm)',
              backgroundColor: 'var(--bg)',
              color: 'var(--text)',
              fontSize: '11px',
              fontWeight: 500,
              outline: 'none',
              cursor: 'pointer',
            }}
          >
            <option value="updated">Updated</option>
            <option value="created">Created</option>
            <option value="title">Title (A-Z)</option>
            <option value="links">Links count</option>
          </select>
        </div>
      </div>

      {/* Notes List */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '10px 10px' }}>
        {loading ? (
          <div style={{ padding: '24px', textAlign: 'center', color: 'var(--muted)', fontSize: '13px' }}>
            Loading notes...
          </div>
        ) : notes.length === 0 ? (
          <div
            style={{
              padding: '36px 14px',
              textAlign: 'center',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: '10px',
            }}
          >
            <div
              style={{
                width: '42px',
                height: '42px',
                borderRadius: '50%',
                backgroundColor: 'var(--accent-soft)',
                border: '1px solid var(--border)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'var(--primary)',
              }}
            >
              <FileText size={20} />
            </div>
            <div>
              <p style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text)' }}>
                {selectedTag ? `No notes tagged #${selectedTag}` : 'No notes yet'}
              </p>
              <p style={{ fontSize: '12px', color: 'var(--muted)', marginTop: '2px' }}>
                {selectedTag ? 'Clear filter to see all notes' : 'Create your first note to start your graph'}
              </p>
            </div>
            {onNewNote && !selectedTag && (
              <button
                onClick={onNewNote}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '6px 14px',
                  backgroundColor: 'var(--primary)',
                  color: '#FFFFFF',
                  border: '1px solid var(--primary-dark)',
                  borderRadius: 'var(--radius-md)',
                  fontSize: '12px',
                  fontWeight: 600,
                  marginTop: '4px',
                }}
              >
                <Plus size={14} />
                <span>+ New note</span>
              </button>
            )}
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            {notes.map((note) => {
              const isSelected = selectedNoteId === note.id;
              return (
                <div
                  key={note.id}
                  onClick={() => onSelectNote(note.id)}
                  style={{
                    padding: '10px 12px',
                    backgroundColor: isSelected ? 'var(--accent-soft)' : 'var(--bg)',
                    borderRadius: 'var(--radius-md)',
                    border: `1px solid ${isSelected ? 'var(--primary)' : 'var(--border)'}`,
                    borderLeft: isSelected ? '3px solid var(--primary)' : '1px solid var(--border)',
                    boxShadow: isSelected ? 'var(--shadow-sm)' : 'none',
                    cursor: 'pointer',
                    transition: 'all 0.15s ease',
                  }}
                  onMouseEnter={(e) => {
                    if (!isSelected) e.currentTarget.style.borderColor = 'var(--primary)';
                  }}
                  onMouseLeave={(e) => {
                    if (!isSelected) e.currentTarget.style.borderColor = 'var(--border)';
                  }}
                >
                  {/* Title & Pin / Time */}
                  <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '6px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '5px', flex: 1, minWidth: 0 }}>
                      <h3
                        style={{
                          fontSize: '13px',
                          fontWeight: 600,
                          color: isSelected ? 'var(--primary-dark)' : 'var(--text)',
                          lineHeight: 1.3,
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap',
                          flex: 1,
                        }}
                        title={note.title}
                      >
                        {note.title}
                      </h3>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '4px', flexShrink: 0 }}>
                      {note.pinned && (
                        <Pin size={12} color="var(--primary)" style={{ transform: 'rotate(45deg)' }} />
                      )}
                      <span style={{ fontSize: '10px', color: 'var(--muted)', whiteSpace: 'nowrap' }}>
                        {formatRelativeTime(note.updated_at)}
                      </span>
                    </div>
                  </div>

                  {/* Preview snippet */}
                  {note.content_snippet && (
                    <p
                      style={{
                        fontSize: '11px',
                        color: 'var(--muted)',
                        marginTop: '3px',
                        lineHeight: 1.4,
                        display: '-webkit-box',
                        WebkitLineClamp: 1,
                        WebkitBoxOrient: 'vertical',
                        overflow: 'hidden',
                      }}
                    >
                      {note.content_snippet}
                    </p>
                  )}

                  {/* Tag chips & Link badges */}
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '6px' }}>
                    <div style={{ display: 'flex', gap: '3px', flexWrap: 'wrap', overflow: 'hidden', maxHeight: '18px' }}>
                      {note.tags.slice(0, 2).map((tag, idx) => (
                        <span
                          key={idx}
                          style={{
                            fontSize: '10px',
                            backgroundColor: 'var(--accent-soft)',
                            border: '1px solid var(--border)',
                            color: 'var(--primary-dark)',
                            padding: '1px 5px',
                            borderRadius: '10px',
                            fontWeight: 500,
                          }}
                        >
                          #{tag}
                        </span>
                      ))}
                      {note.tags.length > 2 && (
                        <span style={{ fontSize: '9px', color: 'var(--muted)', alignSelf: 'center' }}>
                          +{note.tags.length - 2}
                        </span>
                      )}
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '10px', color: 'var(--muted)' }}>
                      <span title="Outgoing links" style={{ display: 'flex', alignItems: 'center', gap: '1px' }}>
                        <ArrowRight size={10} color="var(--outgoing)" /> {note.outgoing_link_count}
                      </span>
                      <span title="Backlinks" style={{ display: 'flex', alignItems: 'center', gap: '1px' }}>
                        <ArrowLeft size={10} color="var(--backlink)" /> {note.backlink_count}
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </aside>
  );
};
