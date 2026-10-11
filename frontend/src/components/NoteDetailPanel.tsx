import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  NoteDetail,
  notesApi,
  searchApi,
  assistApi,
  TitleSuggestItem,
  LinkSuggestionItem,
  ProofreadIssue,
} from '../api';
import { useToast } from '../context/ToastContext';
import {
  Pin,
  Trash2,
  Save,
  X,
  ArrowRight,
  ArrowLeft,
  AlertTriangle,
  Sparkles,
  ChevronLeft,
  Edit2,
  Check,
  CheckCircle,
  Eye,
  SpellCheck,
} from 'lucide-react';

interface NoteDetailPanelProps {
  noteId: number | null;
  isCreatingNew: boolean;
  onClose: () => void;
  onNavigateToNote: (id: number) => void;
  onRefreshAll: () => void;
  navigationHistory: number[];
  onGoBack: () => void;
}

export const NoteDetailPanel: React.FC<NoteDetailPanelProps> = ({
  noteId,
  isCreatingNew,
  onClose,
  onNavigateToNote,
  onRefreshAll,
  navigationHistory,
  onGoBack,
}) => {
  const { showToast } = useToast();

  const [note, setNote] = useState<NoteDetail | null>(null);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [tags, setTags] = useState<string[]>([]);
  const [isPinned, setIsPinned] = useState(false);

  // READ view by default, write mode only when creating new or when user clicks Edit
  const [isEditing, setIsEditing] = useState(isCreatingNew);

  // Tag input state
  const [tagInput, setTagInput] = useState('');
  const [tagSuggestions, setTagSuggestions] = useState<{ tag: string; reason: string }[]>([]);
  const [phraseMerges, setPhraseMerges] = useState<{ from: string[]; to: string }[]>([]);
  const [tagCorrections, setTagCorrections] = useState<{ from: string; to: string }[]>([]);

  // Proofreading state
  const [proofreadIssues, setProofreadIssues] = useState<ProofreadIssue[]>([]);
  const [isCheckingText, setIsCheckingText] = useState(false);
  const [ignoredWords, setIgnoredWords] = useState<string[]>(() => {
    try {
      const stored = localStorage.getItem('pkm_ignored_words');
      return stored ? JSON.parse(stored) : [];
    } catch {
      return [];
    }
  });

  // [[ title popup autocomplete state
  const [showWikilinkPopup, setShowWikilinkPopup] = useState(false);
  const [wikilinkSuggestions, setWikilinkSuggestions] = useState<TitleSuggestItem[]>([]);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Link suggestions state
  const [manualLinkTargetId, setManualLinkTargetId] = useState<string>('');
  const [allNoteTitles, setAllNoteTitles] = useState<TitleSuggestItem[]>([]);
  const [linkSuggestions, setLinkSuggestions] = useState<LinkSuggestionItem[]>([]);
  const [unlinkedMentions, setUnlinkedMentions] = useState<{ note_id: number; note_title: string; snippet: string }[]>([]);

  const [saving, setSaving] = useState(false);
  const [loading, setLoading] = useState(false);

  // Sync state when noteId or isCreatingNew changes
  useEffect(() => {
    if (isCreatingNew) {
      setNote(null);
      setTitle('');
      setContent('');
      setTags([]);
      setIsPinned(false);
      setIsEditing(true);
      setLinkSuggestions([]);
      setUnlinkedMentions([]);
      setProofreadIssues([]);
      return;
    }

    if (!noteId) return;

    setLoading(true);
    setIsEditing(false); // READ view by default for existing notes
    notesApi
      .get(noteId)
      .then((data) => {
        setNote(data);
        setTitle(data.title);
        setContent(data.content || '');
        setTags(data.tags || []);
        setIsPinned(data.pinned);
      })
      .catch((err) => {
        showToast({ type: 'error', message: err.message });
        onClose();
      })
      .finally(() => {
        setLoading(false);
      });

    // Fetch intelligent link suggestions and mentions
    assistApi.getLinkSuggestions(noteId).then(setLinkSuggestions).catch(() => {});
    notesApi.getMentions(noteId).then(setUnlinkedMentions).catch(() => {});
  }, [noteId, isCreatingNew]);

  // Fetch all note titles for manual linking and wikilink resolution
  useEffect(() => {
    notesApi
      .list({ limit: 100 })
      .then((notes) => {
        setAllNoteTitles(notes.map((n) => ({ id: n.id, title: n.title })));
      })
      .catch((err) => {
        console.error('Failed to load notes for linking:', err);
      });
  }, [noteId, isEditing]);

  // Tag intelligence assist (phrase merges, typo corrections, keyword suggestions)
  useEffect(() => {
    if (!isEditing) return;
    const timer = setTimeout(() => {
      assistApi
        .assistTags({ title, content, tags })
        .then((res) => {
          setPhraseMerges(res.merges || []);
          setTagCorrections(res.corrections || []);
          setTagSuggestions(res.suggestions || []);
        })
        .catch(() => {});
    }, 250);
    return () => clearTimeout(timer);
  }, [tags, title, content, isEditing]);

  // Proofread call
  const runProofread = () => {
    if (!content.trim()) {
      setProofreadIssues([]);
      return;
    }
    setIsCheckingText(true);
    assistApi
      .proofread(content, ignoredWords)
      .then((issues) => {
        setProofreadIssues(issues);
        if (issues.length === 0) {
          showToast({ type: 'success', message: 'No proofreading issues found!' });
        }
      })
      .catch(() => {})
      .finally(() => {
        setIsCheckingText(false);
      });
  };

  const handleApplyProofreadFix = (issue: ProofreadIssue) => {
    const before = content.substring(0, issue.start);
    const after = content.substring(issue.end);
    const newContent = `${before}${issue.suggestion}${after}`;
    setContent(newContent);
    setProofreadIssues((prev) => prev.filter((i) => i !== issue));
  };

  const handleIgnoreWord = (word: string) => {
    const clean = word.toLowerCase().trim();
    if (!ignoredWords.includes(clean)) {
      const updated = [...ignoredWords, clean];
      setIgnoredWords(updated);
      try {
        localStorage.setItem('pkm_ignored_words', JSON.stringify(updated));
      } catch {}
    }
    setProofreadIssues((prev) => prev.filter((i) => i.original.toLowerCase().trim() !== clean));
  };

  // Handle markdown textarea keyup / input for [[ detection
  const handleContentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const text = e.target.value;
    const cursorPos = e.target.selectionStart;
    setContent(text);

    // Check if cursor is right after [[
    const textBeforeCursor = text.substring(0, cursorPos);
    const lastOpenBracket = textBeforeCursor.lastIndexOf('[[');
    const lastCloseBracket = textBeforeCursor.lastIndexOf(']]');

    if (lastOpenBracket !== -1 && lastOpenBracket > lastCloseBracket) {
      const query = textBeforeCursor.substring(lastOpenBracket + 2);
      if (!query.includes('\n') && query.length <= 40) {
        setShowWikilinkPopup(true);
        searchApi.suggestTitles(query, 6).then((res) => setWikilinkSuggestions(res.results)).catch(() => {});
        return;
      }
    }
    setShowWikilinkPopup(false);
  };

  const insertWikilink = (suggestedTitle: string) => {
    if (!textareaRef.current) return;
    const cursorPos = textareaRef.current.selectionStart;
    const textBeforeCursor = content.substring(0, cursorPos);
    const lastOpenBracket = textBeforeCursor.lastIndexOf('[[');

    if (lastOpenBracket !== -1) {
      const beforeBracket = content.substring(0, lastOpenBracket);
      const afterCursor = content.substring(cursorPos);
      const newText = `${beforeBracket}[[${suggestedTitle}]]${afterCursor}`;
      setContent(newText);
      setShowWikilinkPopup(false);

      setTimeout(() => {
        if (textareaRef.current) {
          const newPos = lastOpenBracket + suggestedTitle.length + 4;
          textareaRef.current.selectionStart = newPos;
          textareaRef.current.selectionEnd = newPos;
          textareaRef.current.focus();
        }
      }, 50);
    }
  };

  // Tag Input normalization: only comma, Enter, Tab separate tags (space inside tag)
  const handleAddTagRaw = (rawInput: string) => {
    if (!rawInput.trim()) return;
    const parts = rawInput.split(/[\r\n\t,]+/);
    const updated = [...tags];

    parts.forEach((p) => {
      let clean = p.trim().toLowerCase();
      while (clean.startsWith('#')) clean = clean.substring(1).trim();
      clean = clean
        .replace(/[\s_]+/g, '-')
        .replace(/[^\w\-]/g, '')
        .replace(/-+/g, '-')
        .replace(/^-|-$/g, '')
        .slice(0, 30);

      if (clean && !updated.includes(clean)) {
        if (updated.length < 15) {
          updated.push(clean);
        } else {
          showToast({ type: 'error', message: 'A note can have at most 15 tags.' });
        }
      }
    });

    setTags(updated);
    setTagInput('');
  };

  const handleApplyPhraseMerge = (fromTags: string[], toTag: string) => {
    const updated = tags.filter((t) => !fromTags.includes(t));
    if (!updated.includes(toTag)) {
      updated.push(toTag);
    }
    setTags(updated);
    setPhraseMerges((prev) => prev.filter((m) => m.to !== toTag));
  };

  const handleApplyTagCorrection = (fromTag: string, toTag: string) => {
    const updated = tags.map((t) => (t === fromTag ? toTag : t));
    setTags(Array.from(new Set(updated)));
    setTagCorrections((prev) => prev.filter((c) => c.from !== fromTag));
  };

  const handleRemoveTag = (tagName: string) => {
    setTags(tags.filter((t) => t !== tagName));
  };

  // Check save-time unlinked mentions and prompt user
  const checkSaveTimePrompts = (savedNoteId: number, savedContent: string) => {
    const contentLower = savedContent.toLowerCase();
    for (const other of allNoteTitles) {
      if (other.id === savedNoteId) continue;
      const otherTitleLower = other.title.toLowerCase();
      // Check if whole-word mention exists without [[ ]]
      const pattern = new RegExp(`\\b${otherTitleLower}\\b`, 'i');
      const hasWikilink = savedContent.includes(`[[${other.title}]]`);
      if (!hasWikilink && pattern.test(contentLower)) {
        showToast({
          type: 'info',
          message: `This note mentions ${other.title}.`,
          actionLabel: 'Link',
          onAction: async () => {
            try {
              await notesApi.link(savedNoteId, other.id);
              showToast({ type: 'success', message: `Linked to '${other.title}'!` });
              onRefreshAll();
            } catch (err: any) {
              showToast({ type: 'error', message: err.message });
            }
          },
        });
        break; // Only show one prominent prompt at a time
      }
    }
  };

  // Save / Update Note
  const handleSave = async () => {
    if (!title.trim()) {
      showToast({ type: 'error', message: 'Note title cannot be empty.' });
      return;
    }

    setSaving(true);
    try {
      if (isCreatingNew) {
        const created = await notesApi.create({
          title: title.trim(),
          content,
          tags,
        });
        showToast({ type: 'success', message: `Note '${created.title}' created!` });
        setIsEditing(false);
        onRefreshAll();
        onNavigateToNote(created.id);
        checkSaveTimePrompts(created.id, content);
      } else if (noteId) {
        const updated = await notesApi.update(noteId, {
          title: title.trim(),
          content,
          tags,
        });
        setNote(updated);
        setIsEditing(false);
        showToast({ type: 'success', message: `Note saved successfully.` });
        onRefreshAll();
        checkSaveTimePrompts(noteId, content);
      }
    } catch (err: any) {
      showToast({ type: 'error', message: err.message });
    } finally {
      setSaving(false);
    }
  };

  // Cancel Editing
  const handleCancelEdit = () => {
    if (isCreatingNew) {
      onClose();
    } else if (note) {
      setTitle(note.title);
      setContent(note.content || '');
      setTags(note.tags || []);
      setIsEditing(false);
      setProofreadIssues([]);
    }
  };

  // Pin Toggle
  const handleTogglePin = async () => {
    if (!noteId) return;
    try {
      const updated = await notesApi.patch(noteId, { pinned: !isPinned });
      setIsPinned(updated.pinned);
      setNote(updated);
      showToast({
        type: 'success',
        message: updated.pinned ? 'Note pinned to top.' : 'Note unpinned.',
      });
      onRefreshAll();
    } catch (err: any) {
      showToast({ type: 'error', message: err.message });
    }
  };

  // Delete Note with Undo
  const handleDeleteNote = async () => {
    if (!noteId || !note) return;
    if (!window.confirm(`Are you sure you want to delete '${note.title}'?`)) return;

    const backupNote = { ...note };
    try {
      await notesApi.delete(noteId);
      onClose();
      onRefreshAll();

      showToast({
        type: 'info',
        message: `Deleted '${backupNote.title}'.`,
        actionLabel: 'Undo',
        onAction: async () => {
          try {
            await notesApi.create({
              title: backupNote.title,
              content: backupNote.content,
              tags: backupNote.tags,
            });
            showToast({ type: 'success', message: `Restored '${backupNote.title}'!` });
            onRefreshAll();
          } catch (restoreErr: any) {
            showToast({ type: 'error', message: `Failed to restore: ${restoreErr.message}` });
          }
        },
      });
    } catch (err: any) {
      showToast({ type: 'error', message: err.message });
    }
  };

  // Manual link note
  const handleCreateManualLink = async () => {
    if (!noteId || !manualLinkTargetId) return;
    const tgtId = parseInt(manualLinkTargetId, 10);
    try {
      await notesApi.link(noteId, tgtId);
      showToast({ type: 'success', message: 'Manual link added.' });
      setManualLinkTargetId('');
      const updated = await notesApi.get(noteId);
      setNote(updated);
      onRefreshAll();
    } catch (err: any) {
      showToast({ type: 'error', message: err.message });
    }
  };

  // Remove link
  const handleRemoveLink = async (targetId: number) => {
    if (!noteId) return;
    try {
      await notesApi.unlink(noteId, targetId);
      showToast({ type: 'success', message: 'Link removed.' });
      const updated = await notesApi.get(noteId);
      setNote(updated);
      setContent(updated.content || '');
      onRefreshAll();
    } catch (err: any) {
      showToast({ type: 'error', message: err.message });
    }
  };

  // Dismiss a suggested link permanently
  const handleDismissLinkSuggestion = async (targetId: number) => {
    if (!noteId) return;
    try {
      await assistApi.dismissLinkSuggestion(noteId, targetId);
      setLinkSuggestions((prev) => prev.filter((s) => s.note_id !== targetId));
      showToast({ type: 'info', message: 'Suggestion dismissed.' });
    } catch (err: any) {
      showToast({ type: 'error', message: err.message });
    }
  };

  // Convert suggested mention into wikilink
  const handleConvertSuggestionToWikilink = async (suggestedTitle: string, targetId: number) => {
    if (!noteId || !note) return;
    // Replace first whole-word occurrence of title with [[Title]]
    const regex = new RegExp(`\\b${suggestedTitle}\\b`, 'i');
    let newContent = content;
    if (regex.test(newContent)) {
      newContent = newContent.replace(regex, `[[${suggestedTitle}]]`);
    } else {
      newContent = `${newContent}\n\nReferenced [[${suggestedTitle}]]`;
    }
    setContent(newContent);
    try {
      const updated = await notesApi.update(noteId, {
        title: note.title,
        content: newContent,
        tags: note.tags,
      });
      setNote(updated);
      setLinkSuggestions((prev) => prev.filter((s) => s.note_id !== targetId));
      showToast({ type: 'success', message: `Linked to '${suggestedTitle}' via [[${suggestedTitle}]]!` });
      onRefreshAll();
    } catch (err: any) {
      showToast({ type: 'error', message: err.message });
    }
  };

  // Custom Markdown renderer for [[wikilinks]]
  const renderWikilinkText = (textStr: string) => {
    const parts = [];
    const regex = /\[\[([^\]\n]+?)\]\]/g;
    let lastIndex = 0;
    let match;

    while ((match = regex.exec(textStr)) !== null) {
      if (match.index > lastIndex) {
        parts.push(textStr.substring(lastIndex, match.index));
      }

      const raw = match[1];
      const [targetTitle, alias] = raw.split('|').map((s) => s.trim());
      const displayText = alias || targetTitle;
      const targetNoteMatch = allNoteTitles.find((n) => n.title.toLowerCase() === targetTitle.toLowerCase());

      parts.push(
        <span
          key={match.index}
          onClick={(e) => {
            e.stopPropagation();
            if (targetNoteMatch) {
              onNavigateToNote(targetNoteMatch.id);
            } else {
              showToast({
                type: 'info',
                message: `'${targetTitle}' is unresolved. Click to create it.`,
                actionLabel: 'Create',
                onAction: async () => {
                  try {
                    const created = await notesApi.create({ title: targetTitle, content: '' });
                    showToast({ type: 'success', message: `Note '${created.title}' created!` });
                    onRefreshAll();
                    onNavigateToNote(created.id);
                  } catch (err: any) {
                    showToast({ type: 'error', message: err.message });
                  }
                },
              });
            }
          }}
          style={{
            backgroundColor: targetNoteMatch ? 'var(--accent-soft)' : '#FEF3C7',
            color: targetNoteMatch ? 'var(--primary-dark)' : '#B45309',
            border: `1px solid ${targetNoteMatch ? 'var(--border)' : '#FDE68A'}`,
            borderRadius: '4px',
            padding: '1px 5px',
            fontWeight: 600,
            cursor: 'pointer',
            margin: '0 2px',
            textDecoration: 'none',
            fontSize: '13px',
          }}
          title={targetNoteMatch ? `Navigate to '${targetTitle}'` : `Unresolved reference to '${targetTitle}'`}
        >
          {displayText}
        </span>
      );

      lastIndex = regex.lastIndex;
    }

    if (lastIndex < textStr.length) {
      parts.push(textStr.substring(lastIndex));
    }

    return parts;
  };

  return (
    <div
      style={{
        width: '360px',
        minWidth: '360px',
        maxWidth: '360px',
        height: '100%',
        backgroundColor: 'var(--bg)',
        borderLeft: '1px solid var(--border)',
        display: 'flex',
        flexDirection: 'column',
        boxShadow: 'var(--shadow-md)',
        zIndex: 40,
        overflow: 'hidden',
      }}
    >
      {/* Top Header */}
      <div
        style={{
          padding: '10px 14px',
          borderBottom: '1px solid var(--border)',
          backgroundColor: 'var(--surface)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          {navigationHistory.length > 0 && (
            <button
              onClick={onGoBack}
              title="Back to previous note"
              style={{
                background: 'var(--bg)',
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius-sm)',
                padding: '3px 5px',
                display: 'flex',
                alignItems: 'center',
                cursor: 'pointer',
              }}
            >
              <ChevronLeft size={15} />
            </button>
          )}
          <span style={{ fontSize: '11px', fontWeight: 700, color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
            {isCreatingNew ? 'New Note' : isEditing ? 'Edit Note' : 'Note Details'}
          </span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
          {!isCreatingNew && !isEditing && (
            <>
              <button
                onClick={handleTogglePin}
                title={isPinned ? 'Unpin note' : 'Pin note'}
                style={{
                  padding: '5px',
                  backgroundColor: isPinned ? 'var(--accent-soft)' : 'var(--bg)',
                  border: `1px solid ${isPinned ? 'var(--primary)' : 'var(--border)'}`,
                  borderRadius: 'var(--radius-sm)',
                  color: isPinned ? 'var(--primary-dark)' : 'var(--muted)',
                }}
              >
                <Pin size={14} style={{ transform: isPinned ? 'rotate(45deg)' : 'none' }} />
              </button>
              <button
                onClick={handleDeleteNote}
                title="Delete note"
                style={{
                  padding: '5px',
                  backgroundColor: 'var(--bg)',
                  border: '1px solid var(--border)',
                  borderRadius: 'var(--radius-sm)',
                  color: 'var(--danger)',
                }}
              >
                <Trash2 size={14} />
              </button>
              <button
                onClick={() => setIsEditing(true)}
                title="Edit note"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px',
                  padding: '5px 10px',
                  backgroundColor: 'var(--primary)',
                  color: '#FFFFFF',
                  border: '1px solid var(--primary-dark)',
                  borderRadius: 'var(--radius-sm)',
                  fontWeight: 600,
                  fontSize: '12px',
                }}
              >
                <Edit2 size={13} />
                <span>Edit</span>
              </button>
            </>
          )}

          {isEditing && (
            <>
              <button
                onClick={handleCancelEdit}
                style={{
                  padding: '5px 8px',
                  backgroundColor: 'var(--bg)',
                  color: 'var(--muted)',
                  border: '1px solid var(--border)',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: '12px',
                  fontWeight: 500,
                }}
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                disabled={saving}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px',
                  padding: '5px 10px',
                  backgroundColor: 'var(--primary)',
                  color: '#FFFFFF',
                  border: '1px solid var(--primary-dark)',
                  borderRadius: 'var(--radius-sm)',
                  fontWeight: 600,
                  fontSize: '12px',
                }}
              >
                <Save size={13} />
                <span>{saving ? 'Saving...' : 'Save'}</span>
              </button>
            </>
          )}

          <button
            onClick={onClose}
            title="Close panel (Esc)"
            style={{
              padding: '4px',
              background: 'none',
              border: 'none',
              color: 'var(--muted)',
              cursor: 'pointer',
            }}
          >
            <X size={16} />
          </button>
        </div>
      </div>

      {/* Main Body */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '14px', display: 'flex', flexDirection: 'column', gap: '14px' }}>
        {/* Title */}
        {isEditing ? (
          <div>
            <label style={{ fontSize: '11px', fontWeight: 600, color: 'var(--muted)', display: 'block', marginBottom: '3px' }}>
              TITLE
            </label>
            <input
              type="text"
              placeholder="Note title..."
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              style={{
                width: '100%',
                padding: '6px 10px',
                fontSize: '15px',
                fontWeight: 700,
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius-md)',
                backgroundColor: 'var(--bg)',
                outline: 'none',
                color: 'var(--text)',
              }}
            />
          </div>
        ) : (
          <div>
            <h2 style={{ fontSize: '18px', fontWeight: 700, color: 'var(--text)', lineHeight: 1.3 }}>
              {note?.title || title}
            </h2>
          </div>
        )}


        {/* Tags Section */}
        {isEditing ? (
          <div>
            <label style={{ fontSize: '11px', fontWeight: 600, color: 'var(--muted)', display: 'block', marginBottom: '4px' }}>
              TAGS (MAX 15) &bull; COMMA OR ENTER TO ADD
            </label>

            {/* Phrase Merge Suggestions Banner */}
            {phraseMerges.length > 0 && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', marginBottom: '6px' }}>
                {phraseMerges.map((pm, idx) => (
                  <div
                    key={idx}
                    style={{
                      padding: '4px 8px',
                      backgroundColor: 'var(--accent-soft)',
                      border: '1px solid var(--border)',
                      borderRadius: 'var(--radius-sm)',
                      fontSize: '11px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      color: 'var(--primary-dark)',
                    }}
                  >
                    <span>Did you mean <strong>#{pm.to}</strong>?</span>
                    <button
                      onClick={() => handleApplyPhraseMerge(pm.from, pm.to)}
                      style={{
                        padding: '1px 6px',
                        backgroundColor: 'var(--primary)',
                        color: '#FFFFFF',
                        border: 'none',
                        borderRadius: '3px',
                        fontSize: '10px',
                        fontWeight: 600,
                      }}
                    >
                      Merge
                    </button>
                  </div>
                ))}
              </div>
            )}

            {/* Tag Typo Corrections Banner */}
            {tagCorrections.length > 0 && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', marginBottom: '6px' }}>
                {tagCorrections.map((tc, idx) => (
                  <div
                    key={idx}
                    style={{
                      padding: '4px 8px',
                      backgroundColor: '#FEF3C7',
                      border: '1px solid #FDE68A',
                      borderRadius: 'var(--radius-sm)',
                      fontSize: '11px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      color: '#B45309',
                    }}
                  >
                    <span>Typo: Did you mean <strong>#{tc.to}</strong> for #{tc.from}?</span>
                    <button
                      onClick={() => handleApplyTagCorrection(tc.from, tc.to)}
                      style={{
                        padding: '1px 6px',
                        backgroundColor: '#B45309',
                        color: '#FFFFFF',
                        border: 'none',
                        borderRadius: '3px',
                        fontSize: '10px',
                        fontWeight: 600,
                      }}
                    >
                      Apply
                    </button>
                  </div>
                ))}
              </div>
            )}

            {/* Tags Box */}
            <div
              style={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: '4px',
                padding: '4px 6px',
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius-md)',
                backgroundColor: 'var(--surface)',
                minHeight: '34px',
                alignItems: 'center',
              }}
            >
              {tags.map((tag) => (
                <span
                  key={tag}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '3px',
                    padding: '2px 6px',
                    backgroundColor: 'var(--accent-soft)',
                    border: '1px solid var(--border)',
                    borderRadius: '10px',
                    fontSize: '11px',
                    color: 'var(--primary-dark)',
                    fontWeight: 600,
                  }}
                >
                  #{tag}
                  <X
                    size={11}
                    onClick={() => handleRemoveTag(tag)}
                    style={{ cursor: 'pointer' }}
                  />
                </span>
              ))}
              <input
                type="text"
                placeholder="+ tag (comma/tab)..."
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ',' || e.key === 'Tab') {
                    e.preventDefault();
                    handleAddTagRaw(tagInput);
                  }
                }}
                onBlur={() => {
                  if (tagInput.trim()) handleAddTagRaw(tagInput);
                }}
                style={{
                  border: 'none',
                  background: 'transparent',
                  outline: 'none',
                  fontSize: '12px',
                  minWidth: '80px',
                  flex: 1,
                  padding: '2px',
                }}
              />
            </div>

            {/* Keyword tag suggestions */}
            {tagSuggestions.length > 0 && (
              <div
                style={{
                  marginTop: '4px',
                  padding: '6px 8px',
                  backgroundColor: 'var(--bg)',
                  border: '1px solid var(--border)',
                  borderRadius: 'var(--radius-md)',
                  display: 'flex',
                  flexWrap: 'wrap',
                  gap: '4px',
                  alignItems: 'center',
                }}
              >
                <Sparkles size={11} color="var(--primary)" />
                <span style={{ fontSize: '10px', color: 'var(--muted)', fontWeight: 600 }}>Suggested:</span>
                {tagSuggestions.slice(0, 5).map((s) => (
                  <button
                    key={s.tag}
                    onClick={() => handleAddTagRaw(s.tag)}
                    style={{
                      fontSize: '10px',
                      padding: '1px 5px',
                      backgroundColor: 'var(--surface)',
                      border: '1px solid var(--border)',
                      borderRadius: '8px',
                      color: 'var(--text)',
                      cursor: 'pointer',
                    }}
                    title={s.reason}
                  >
                    +{s.tag}
                  </button>
                ))}
              </div>
            )}
          </div>
        ) : (
          tags.length > 0 && (
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
              {tags.map((tag) => (
                <span
                  key={tag}
                  style={{
                    padding: '2px 7px',
                    backgroundColor: 'var(--accent-soft)',
                    border: '1px solid var(--border)',
                    borderRadius: '10px',
                    fontSize: '11px',
                    color: 'var(--primary-dark)',
                    fontWeight: 600,
                  }}
                >
                  #{tag}
                </span>
              ))}
            </div>
          )
        )}

        {/* Content Section & Proofreading */}
        {isEditing ? (
          <div style={{ position: 'relative', display: 'flex', flexDirection: 'column', flex: 1, minHeight: '180px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3px' }}>
              <label style={{ fontSize: '11px', fontWeight: 600, color: 'var(--muted)' }}>
                CONTENT (MARKDOWN)
              </label>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <button
                  type="button"
                  onClick={runProofread}
                  disabled={isCheckingText}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '3px',
                    background: 'none',
                    border: 'none',
                    color: 'var(--primary)',
                    fontSize: '11px',
                    cursor: 'pointer',
                    fontWeight: 600,
                  }}
                >
                  <SpellCheck size={12} />
                  <span>{isCheckingText ? 'Checking...' : 'Check Text'}</span>
                </button>
                <span style={{ fontSize: '10px', color: 'var(--muted)' }}>Type [[ to link</span>
              </div>
            </div>

            <textarea
              ref={textareaRef}
              value={content}
              onChange={handleContentChange}
              placeholder="Write note content in Markdown. Use [[Note Title]] to link..."
              style={{
                width: '100%',
                minHeight: '180px',
                flex: 1,
                padding: '8px 10px',
                fontSize: '13px',
                lineHeight: '1.5',
                fontFamily: 'Consolas, Monaco, "Courier New", monospace',
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius-md)',
                backgroundColor: 'var(--bg)',
                color: 'var(--text)',
                outline: 'none',
                resize: 'vertical',
              }}
            />

            {/* Proofreading Issues Panel */}
            {proofreadIssues.length > 0 && (
              <div
                style={{
                  marginTop: '6px',
                  padding: '8px 10px',
                  backgroundColor: '#FFFBEB',
                  border: '1px solid #FDE68A',
                  borderRadius: 'var(--radius-md)',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '5px',
                  maxHeight: '140px',
                  overflowY: 'auto',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <span style={{ fontSize: '11px', fontWeight: 700, color: '#B45309' }}>
                    Proofreading Suggestions ({proofreadIssues.length})
                  </span>
                  <button
                    onClick={() => setProofreadIssues([])}
                    style={{ background: 'none', border: 'none', color: '#B45309', cursor: 'pointer' }}
                  >
                    <X size={12} />
                  </button>
                </div>
                {proofreadIssues.map((issue, idx) => (
                  <div
                    key={idx}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      fontSize: '11px',
                      padding: '3px 0',
                      borderBottom: idx < proofreadIssues.length - 1 ? '1px solid #FEF3C7' : 'none',
                    }}
                  >
                    <div>
                      <span style={{ textDecoration: 'line-through', color: 'var(--danger)', marginRight: '4px' }}>
                        {issue.original}
                      </span>
                      &rarr;
                      <span style={{ fontWeight: 700, color: 'var(--success)', marginLeft: '4px' }}>
                        {issue.suggestion}
                      </span>
                      <span style={{ fontSize: '10px', color: 'var(--muted)', marginLeft: '6px' }}>
                        ({issue.reason})
                      </span>
                    </div>
                    <div style={{ display: 'flex', gap: '3px' }}>
                      <button
                        onClick={() => handleApplyProofreadFix(issue)}
                        style={{
                          padding: '1px 5px',
                          backgroundColor: 'var(--success)',
                          color: '#FFFFFF',
                          border: 'none',
                          borderRadius: '3px',
                          fontSize: '10px',
                          fontWeight: 600,
                        }}
                      >
                        Replace
                      </button>
                      <button
                        onClick={() => handleIgnoreWord(issue.original)}
                        style={{
                          padding: '1px 5px',
                          backgroundColor: 'var(--surface)',
                          color: 'var(--muted)',
                          border: '1px solid var(--border)',
                          borderRadius: '3px',
                          fontSize: '10px',
                        }}
                        title="Ignore this word permanently"
                      >
                        Ignore
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* [[ Autocomplete popup */}
            {showWikilinkPopup && (
              <div
                style={{
                  position: 'absolute',
                  bottom: '10px',
                  left: '6px',
                  right: '6px',
                  backgroundColor: 'var(--bg)',
                  border: '2px solid var(--primary)',
                  borderRadius: 'var(--radius-md)',
                  boxShadow: 'var(--shadow-lg)',
                  maxHeight: '160px',
                  overflowY: 'auto',
                  zIndex: 200,
                }}
              >
                <div style={{ padding: '5px 8px', backgroundColor: 'var(--accent-soft)', fontSize: '10px', fontWeight: 700, color: 'var(--primary-dark)' }}>
                  Link to existing note:
                </div>
                {wikilinkSuggestions.map((s) => (
                  <div
                    key={s.id}
                    onClick={() => insertWikilink(s.title)}
                    style={{
                      padding: '6px 10px',
                      fontSize: '12px',
                      fontWeight: 500,
                      cursor: 'pointer',
                      borderBottom: '1px solid var(--surface)',
                    }}
                    onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = 'var(--accent-soft)')}
                    onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = 'transparent')}
                  >
                    [[{s.title}]]
                  </div>
                ))}
                {wikilinkSuggestions.length === 0 && (
                  <div style={{ padding: '6px 10px', fontSize: '11px', color: 'var(--muted)' }}>
                    No matching note. Type ']]' to save as pending reference.
                  </div>
                )}
              </div>
            )}
          </div>
        ) : (
          <div
            style={{
              padding: '10px 12px',
              border: '1px solid var(--border)',
              borderRadius: 'var(--radius-md)',
              backgroundColor: 'var(--surface)',
              fontSize: '13px',
              lineHeight: '1.6',
              maxHeight: '260px',
              overflowY: 'auto',
            }}
          >
            {content.trim() ? (
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  p: ({ children }) => (
                    <p style={{ marginBottom: '8px' }}>
                      {React.Children.map(children, (child) => {
                        if (typeof child === 'string') {
                          return renderWikilinkText(child);
                        }
                        return child;
                      })}
                    </p>
                  ),
                  li: ({ children }) => (
                    <li>
                      {React.Children.map(children, (child) => {
                        if (typeof child === 'string') {
                          return renderWikilinkText(child);
                        }
                        return child;
                      })}
                    </li>
                  ),
                }}
              >
                {content}
              </ReactMarkdown>
            ) : (
              <span style={{ color: 'var(--muted)', fontStyle: 'italic', fontSize: '12px' }}>
                No content. Click Edit to write.
              </span>
            )}
          </div>
        )}

        {/* Unresolved Links Warning */}
        {note && note.unresolved_links && note.unresolved_links.length > 0 && (
          <div
            style={{
              padding: '8px 10px',
              backgroundColor: '#FEF3C7',
              border: '1px solid #FDE68A',
              borderRadius: 'var(--radius-md)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '5px', color: '#B45309', fontWeight: 600, fontSize: '11px', marginBottom: '5px' }}>
              <AlertTriangle size={13} />
              <span>Unresolved References ({note.unresolved_links.length})</span>
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
              {note.unresolved_links.map((uTitle, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    notesApi.create({ title: uTitle, content: '' }).then((created) => {
                      showToast({ type: 'success', message: `Resolved: Note '${created.title}' created!` });
                      onRefreshAll();
                      onNavigateToNote(created.id);
                    });
                  }}
                  style={{
                    fontSize: '10px',
                    padding: '2px 6px',
                    backgroundColor: '#FFFFFF',
                    border: '1px solid #FDE68A',
                    borderRadius: '8px',
                    color: '#B45309',
                    cursor: 'pointer',
                    fontWeight: 600,
                  }}
                  title="Click to create note for this unresolved title"
                >
                  + {uTitle}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Links & Backlinks Section */}
        {note && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', borderTop: '1px solid var(--border)', paddingTop: '12px' }}>
            {/* Outgoing Links */}
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '5px' }}>
                <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'var(--outgoing)' }} />
                <h4 style={{ fontSize: '11px', fontWeight: 700, color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                  Outgoing Links ({note.outgoing_links.length})
                </h4>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '3px' }}>
                {note.outgoing_links.map((l) => (
                  <div
                    key={`${l.source_id}_${l.target_id}`}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: '5px 8px',
                      backgroundColor: 'var(--surface)',
                      border: '1px solid var(--border)',
                      borderRadius: 'var(--radius-sm)',
                      fontSize: '12px',
                    }}
                  >
                    <span
                      onClick={() => onNavigateToNote(l.target_id)}
                      style={{ color: 'var(--primary-dark)', fontWeight: 600, cursor: 'pointer', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}
                    >
                      {l.target_title || `Note ${l.target_id}`}
                    </span>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '4px', flexShrink: 0 }}>
                      <span
                        style={{
                          fontSize: '9px',
                          padding: '1px 4px',
                          borderRadius: '3px',
                          backgroundColor: l.origin === 'manual' ? 'var(--accent-soft)' : '#F3EEFF',
                          color: 'var(--primary-dark)',
                          fontWeight: 600,
                        }}
                      >
                        {l.origin}
                      </span>
                      <button
                        onClick={() => handleRemoveLink(l.target_id)}
                        title="Remove link"
                        style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--muted)', padding: '2px' }}
                      >
                        <X size={12} />
                      </button>
                    </div>
                  </div>
                ))}
                {note.outgoing_links.length === 0 && (
                  <span style={{ fontSize: '11px', color: 'var(--muted)', fontStyle: 'italic' }}>No outgoing links</span>
                )}
              </div>
            </div>

            {/* Backlinks */}
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '5px' }}>
                <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'var(--backlink)' }} />
                <h4 style={{ fontSize: '11px', fontWeight: 700, color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                  Backlinks ({note.backlinks.length})
                </h4>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '3px' }}>
                {note.backlinks.map((b) => (
                  <div
                    key={b.id}
                    onClick={() => onNavigateToNote(b.id)}
                    style={{
                      padding: '5px 8px',
                      backgroundColor: 'var(--surface)',
                      border: '1px solid var(--border)',
                      borderRadius: 'var(--radius-sm)',
                      fontSize: '12px',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                    }}
                  >
                    <span style={{ color: 'var(--primary-dark)', fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {b.title}
                    </span>
                    <span style={{ fontSize: '9px', color: 'var(--muted)' }}>{b.origin}</span>
                  </div>
                ))}
                {note.backlinks.length === 0 && (
                  <span style={{ fontSize: '11px', color: 'var(--muted)', fontStyle: 'italic' }}>No backlinks referencing this note</span>
                )}
              </div>
            </div>

            {/* Add Manual Link */}
            <div style={{ backgroundColor: 'var(--surface)', padding: '8px 10px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border)' }}>
              <span style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text)', display: 'block', marginBottom: '4px' }}>
                Add Manual Link:
              </span>
              <div style={{ display: 'flex', gap: '4px' }}>
                <select
                  value={manualLinkTargetId}
                  onChange={(e) => setManualLinkTargetId(e.target.value)}
                  style={{
                    flex: 1,
                    padding: '4px 6px',
                    border: '1px solid var(--border)',
                    borderRadius: 'var(--radius-sm)',
                    backgroundColor: 'var(--bg)',
                    fontSize: '11px',
                  }}
                >
                  <option value="">Select target note...</option>
                  {allNoteTitles
                    .filter((n) => n.id !== noteId)
                    .map((n) => {
                      const isAlreadyLinked = note?.outgoing_links.some((l) => l.target_id === n.id);
                      return (
                        <option key={n.id} value={n.id} disabled={isAlreadyLinked}>
                          {n.title} {isAlreadyLinked ? '(already linked)' : ''}
                        </option>
                      );
                    })}
                </select>
                <button
                  onClick={handleCreateManualLink}
                  disabled={!manualLinkTargetId}
                  style={{
                    padding: '4px 10px',
                    backgroundColor: 'var(--primary)',
                    color: '#FFFFFF',
                    border: '1px solid var(--primary-dark)',
                    borderRadius: 'var(--radius-sm)',
                    fontWeight: 600,
                    fontSize: '11px',
                  }}
                >
                  Link
                </button>
              </div>
            </div>

            {/* Accurate Suggested Links with Reasons, Dismiss, and Convert */}
            {linkSuggestions.length > 0 && (
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '5px', marginBottom: '5px' }}>
                  <Sparkles size={12} color="var(--primary)" />
                  <h4 style={{ fontSize: '11px', fontWeight: 700, color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                    Suggested Links ({linkSuggestions.length})
                  </h4>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                  {linkSuggestions.map((sl) => {
                    const isMention = sl.reasons.some((r) => r.startsWith('mentions'));
                    return (
                      <div
                        key={sl.note_id}
                        style={{
                          padding: '6px 8px',
                          backgroundColor: 'var(--bg)',
                          border: '1px solid var(--border)',
                          borderRadius: 'var(--radius-sm)',
                          display: 'flex',
                          flexDirection: 'column',
                          gap: '4px',
                        }}
                      >
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                          <span style={{ fontWeight: 600, fontSize: '12px', color: 'var(--text)' }}>
                            {sl.title}
                          </span>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '3px' }}>
                            {isMention && (
                              <button
                                onClick={() => handleConvertSuggestionToWikilink(sl.title, sl.note_id)}
                                style={{
                                  padding: '2px 5px',
                                  backgroundColor: 'var(--accent-soft)',
                                  border: '1px solid var(--border)',
                                  borderRadius: '3px',
                                  fontSize: '10px',
                                  fontWeight: 600,
                                  color: 'var(--primary-dark)',
                                }}
                                title="Convert text mention to [[Title]]"
                              >
                                Convert to link
                              </button>
                            )}
                            <button
                              onClick={() => {
                                notesApi.link(noteId, sl.note_id).then(() => {
                                  showToast({ type: 'success', message: `Linked to '${sl.title}'` });
                                  notesApi.get(noteId).then(setNote);
                                  setLinkSuggestions((prev) => prev.filter((s) => s.note_id !== sl.note_id));
                                  onRefreshAll();
                                });
                              }}
                              style={{
                                padding: '2px 6px',
                                backgroundColor: 'var(--primary)',
                                border: 'none',
                                borderRadius: '3px',
                                fontWeight: 600,
                                fontSize: '10px',
                                color: '#FFFFFF',
                              }}
                            >
                              + Link
                            </button>
                            <button
                              onClick={() => handleDismissLinkSuggestion(sl.note_id)}
                              style={{
                                padding: '2px 4px',
                                background: 'none',
                                border: 'none',
                                color: 'var(--muted)',
                                cursor: 'pointer',
                              }}
                              title="Dismiss suggestion permanently"
                            >
                              <X size={12} />
                            </button>
                          </div>
                        </div>

                        {/* Reasons */}
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '3px' }}>
                          {sl.reasons.map((r, idx) => (
                            <span
                              key={idx}
                              style={{
                                fontSize: '9px',
                                padding: '1px 4px',
                                borderRadius: '3px',
                                backgroundColor: 'var(--surface)',
                                border: '1px solid var(--border)',
                                color: 'var(--muted)',
                              }}
                            >
                              {r}
                            </span>
                          ))}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Unlinked Mentions */}
            {unlinkedMentions.length > 0 && (
              <div>
                <h4 style={{ fontSize: '11px', fontWeight: 700, color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: '5px' }}>
                  Unlinked Mentions ({unlinkedMentions.length})
                </h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '3px' }}>
                  {unlinkedMentions.map((um) => (
                    <div
                      key={um.note_id}
                      style={{
                        padding: '5px 8px',
                        backgroundColor: 'var(--surface)',
                        border: '1px solid var(--border)',
                        borderRadius: 'var(--radius-sm)',
                        fontSize: '11px',
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '2px' }}>
                        <span
                          onClick={() => onNavigateToNote(um.note_id)}
                          style={{ fontWeight: 600, color: 'var(--primary-dark)', cursor: 'pointer' }}
                        >
                          {um.note_title}
                        </span>
                        <button
                          onClick={() => {
                            const newContent = `${content}\n\nReferenced in [[${um.note_title}]]`;
                            setContent(newContent);
                            notesApi.update(noteId, {
                              title: note.title,
                              content: newContent,
                              tags: note.tags,
                            }).then((updated) => {
                              setNote(updated);
                              showToast({ type: 'success', message: `Converted mention of '${um.note_title}' into a link!` });
                              onRefreshAll();
                            });
                          }}
                          style={{
                            padding: '1px 5px',
                            backgroundColor: 'var(--accent-soft)',
                            border: '1px solid var(--border)',
                            borderRadius: '3px',
                            fontSize: '9px',
                            fontWeight: 600,
                            color: 'var(--primary-dark)',
                          }}
                        >
                          Convert to Link
                        </button>
                      </div>
                      <p style={{ fontSize: '10px', color: 'var(--muted)', fontStyle: 'italic' }}>"{um.snippet}"</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
