import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  NoteListItem,
  TagUsage,
  GraphResponse,
  GraphStats,
  GraphInsightsResponse,
  notesApi,
  tagsApi,
  graphApi,
  systemApi,
} from './api';
import { TopBar } from './components/TopBar';
import { Sidebar } from './components/Sidebar';
import { GraphCanvas } from './components/GraphCanvas';
import { NoteDetailPanel } from './components/NoteDetailPanel';
import { ExportImportModal } from './components/ExportImportModal';
import { TrashModal } from './components/TrashModal';
import { ActivityModal } from './components/ActivityModal';
import { InsightsPanel } from './components/InsightsPanel';
import { ToastContainer } from './components/ToastContainer';
import { useToast } from './context/ToastContext';
import { useSSE } from './hooks/useSSE';

export const App: React.FC = () => {
  const { showToast } = useToast();

  // State
  const [notes, setNotes] = useState<NoteListItem[]>([]);
  const [tags, setTags] = useState<TagUsage[]>([]);
  const [graphData, setGraphData] = useState<GraphResponse | null>(null);
  const [stats, setStats] = useState<GraphStats | null>(null);
  const [insightsData, setInsightsData] = useState<GraphInsightsResponse | null>(null);
  const [loadingInsights, setLoadingInsights] = useState(false);

  const [selectedNoteId, setSelectedNoteId] = useState<number | null>(null);
  const [isCreatingNew, setIsCreatingNew] = useState(false);
  const [selectedTag, setSelectedTag] = useState<string | null>(null);
  const [sortBy, setSortBy] = useState<string>('updated');
  const [isEditMode, setIsEditMode] = useState(false);
  const [isExportImportOpen, setIsExportImportOpen] = useState(false);
  const [isTrashOpen, setIsTrashOpen] = useState(false);
  const [isActivityOpen, setIsActivityOpen] = useState(false);
  const [isInsightsOpen, setIsInsightsOpen] = useState(false);
  const [neighborhoodDepth, setNeighborhoodDepth] = useState<number>(2);
  const [graphTagFilter, setGraphTagFilter] = useState<string | null>(null);
  const [navigationHistory, setNavigationHistory] = useState<number[]>([]);

  const [loadingNotes, setLoadingNotes] = useState(false);
  const searchInputRef = useRef<HTMLInputElement>(null);

  // Fetch Notes
  const fetchNotes = useCallback(async () => {
    setLoadingNotes(true);
    try {
      const data = await notesApi.list({
        tag: selectedTag || undefined,
        sort: sortBy,
      });
      setNotes(data);
    } catch (err: any) {
      showToast({ type: 'error', message: err.message });
    } finally {
      setLoadingNotes(false);
    }
  }, [selectedTag, sortBy, showToast]);

  // Fetch Tags
  const fetchTags = useCallback(async () => {
    try {
      const data = await tagsApi.list();
      setTags(data);
    } catch (err: any) {
      console.error('Failed to fetch tags:', err);
    }
  }, []);

  // Fetch Graph
  const fetchGraph = useCallback(async () => {
    try {
      if (selectedNoteId && neighborhoodDepth > 0) {
        const data = await graphApi.getNeighborhood(selectedNoteId, neighborhoodDepth);
        setGraphData(data);
      } else {
        const data = await graphApi.getFullGraph(graphTagFilter || selectedTag || undefined);
        setGraphData(data);
      }
    } catch (err: any) {
      console.error('Failed to fetch graph:', err);
    }
  }, [selectedNoteId, neighborhoodDepth, graphTagFilter, selectedTag]);

  // Fetch Stats
  const fetchStats = useCallback(async () => {
    try {
      const data = await graphApi.getStats();
      setStats(data);
    } catch (err: any) {
      console.error('Failed to fetch stats:', err);
    }
  }, []);

  // Fetch Insights
  const fetchInsights = useCallback(async () => {
    setLoadingInsights(true);
    try {
      const data = await graphApi.getInsights();
      setInsightsData(data);
    } catch (err: any) {
      console.error('Failed to fetch insights:', err);
    } finally {
      setLoadingInsights(false);
    }
  }, []);

  const refreshAll = useCallback(() => {
    fetchNotes();
    fetchTags();
    fetchGraph();
    fetchStats();
    fetchInsights();
  }, [fetchNotes, fetchTags, fetchGraph, fetchStats, fetchInsights]);

  // Initial Load
  useEffect(() => {
    refreshAll();
  }, [selectedTag, sortBy]);

  useEffect(() => {
    fetchGraph();
  }, [selectedNoteId, neighborhoodDepth, graphTagFilter]);

  // SSE Real-Time Sync with Selective Refetching
  const { status: sseStatus } = useSSE(
    useCallback(
      (event: string, data: any) => {
        console.log('SSE event received:', event, data);
        if (event === 'note_created' || event === 'note_updated' || event === 'note_deleted') {
          fetchNotes();
          fetchGraph();
          fetchStats();
          fetchTags();
          fetchInsights();
        } else if (event === 'link_created' || event === 'link_deleted') {
          fetchGraph();
          fetchStats();
          fetchInsights();
        } else if (event === 'group_changed') {
          fetchNotes();
          fetchInsights();
        } else if (event === 'database_reset') {
          refreshAll();
        }
      },
      [fetchNotes, fetchGraph, fetchStats, fetchTags, fetchInsights, refreshAll]
    )
  );

  // Reset Database Handler
  const handleResetDatabase = async () => {
    if (
      !window.confirm(
        'Are you sure you want to reset the database?\n\nThis will permanently delete all notes, links, and tags, returning the graph to an empty state (0 notes).'
      )
    ) {
      return;
    }

    try {
      const res = await systemApi.resetDatabase();
      showToast({
        type: 'info',
        message: res.message || 'Database reset successfully to 0 notes.',
      });
      setSelectedNoteId(null);
      setIsCreatingNew(false);
      setNavigationHistory([]);
      refreshAll();
    } catch (err: any) {
      showToast({ type: 'error', message: `Reset failed: ${err.message}` });
    }
  };

  // Navigation handlers
  const handleSelectNote = (id: number) => {
    if (selectedNoteId && selectedNoteId !== id) {
      setNavigationHistory((prev) => [...prev, selectedNoteId]);
    }
    setSelectedNoteId(id);
    setIsCreatingNew(false);
  };

  const handleGoBack = () => {
    if (navigationHistory.length === 0) return;
    const prevId = navigationHistory[navigationHistory.length - 1];
    setNavigationHistory((prev) => prev.slice(0, prev.length - 1));
    setSelectedNoteId(prevId);
    setIsCreatingNew(false);
  };

  const handleNewNote = () => {
    setSelectedNoteId(null);
    setIsCreatingNew(true);
  };

  const handleClosePanel = () => {
    setSelectedNoteId(null);
    setIsCreatingNew(false);
  };

  // Global Keyboard Shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const tag = (e.target as HTMLElement)?.tagName?.toLowerCase();
      if (tag === 'input' || tag === 'textarea') {
        if (e.key === 'Escape') {
          (e.target as HTMLElement).blur();
        }
        return;
      }

      if (e.key === '/') {
        e.preventDefault();
        searchInputRef.current?.focus();
      } else if (e.key === 'n' || e.key === 'N') {
        e.preventDefault();
        handleNewNote();
      } else if (e.key === 'e' || e.key === 'E') {
        e.preventDefault();
        setIsEditMode((prev) => !prev);
      } else if (e.key === 'Escape') {
        handleClosePanel();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', width: '100vw', height: '100vh', overflow: 'hidden' }}>
      {/* Top Navigation Bar */}
      <TopBar
        onNewNote={handleNewNote}
        onSelectNote={handleSelectNote}
        onSelectTag={(tag) => setSelectedTag(tag)}
        isEditMode={isEditMode}
        onToggleEditMode={() => setIsEditMode(!isEditMode)}
        onOpenExportImport={() => setIsExportImportOpen(true)}
        onResetDatabase={handleResetDatabase}
        onOpenTrash={() => setIsTrashOpen(true)}
        onOpenActivity={() => setIsActivityOpen(true)}
        onOpenInsights={() => {
          setIsInsightsOpen(true);
          fetchInsights();
        }}
        sseStatus={sseStatus}
        searchInputRef={searchInputRef}
      />

      {/* Slim Stats Bar under toolbar */}
      <div
        style={{
          height: '26px',
          backgroundColor: 'var(--surface)',
          borderBottom: '1px solid var(--border)',
          display: 'flex',
          alignItems: 'center',
          padding: '0 20px',
          gap: '18px',
          fontSize: '11px',
          color: 'var(--muted)',
          fontWeight: 500,
          zIndex: 10,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
          <span>Notes:</span>
          <span style={{ fontWeight: 700, color: 'var(--primary-dark)' }}>{stats?.total_notes ?? notes.length}</span>
        </div>
        <div style={{ width: '1px', height: '12px', backgroundColor: 'var(--border)' }} />
        <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
          <span>Links:</span>
          <span style={{ fontWeight: 700, color: 'var(--primary-dark)' }}>{stats?.total_links ?? 0}</span>
        </div>
        <div style={{ width: '1px', height: '12px', backgroundColor: 'var(--border)' }} />
        <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
          <span>Orphans:</span>
          <span
            style={{
              fontWeight: 700,
              color: (stats?.orphan_count ?? 0) > 0 ? 'var(--danger)' : 'var(--muted)',
            }}
          >
            {stats?.orphan_count ?? 0}
          </span>
        </div>
        <div style={{ width: '1px', height: '12px', backgroundColor: 'var(--border)' }} />
        <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
          <span>Tags:</span>
          <span style={{ fontWeight: 700, color: 'var(--primary-dark)' }}>{stats?.total_tags ?? tags.length}</span>
        </div>
      </div>

      {/* Main Workspace Layout */}
      <div style={{ display: 'flex', flex: 1, height: 'calc(100vh - 82px)', overflow: 'hidden' }}>
        {/* Left Sidebar */}
        <Sidebar
          notes={notes}
          tags={tags}
          selectedNoteId={selectedNoteId}
          selectedTag={selectedTag}
          sortBy={sortBy}
          onSelectNote={handleSelectNote}
          onSelectTag={(tag) => setSelectedTag(tag)}
          onChangeSort={(sort) => setSortBy(sort)}
          onNewNote={handleNewNote}
          loading={loadingNotes}
        />

        {/* Center Cytoscape Graph Canvas */}
        <GraphCanvas
          graphData={graphData}
          stats={stats}
          selectedNoteId={selectedNoteId}
          isEditMode={isEditMode}
          onSelectNote={handleSelectNote}
          onNewNote={handleNewNote}
          onRefreshGraph={refreshAll}
          neighborhoodDepth={neighborhoodDepth}
          onChangeDepth={setNeighborhoodDepth}
          graphTagFilter={graphTagFilter}
          onChangeGraphTagFilter={setGraphTagFilter}
          onClearSelection={() => setSelectedNoteId(null)}
        />

        {/* Right Note Detail / Editor Panel */}
        {(selectedNoteId !== null || isCreatingNew) && (
          <NoteDetailPanel
            noteId={selectedNoteId}
            isCreatingNew={isCreatingNew}
            onClose={handleClosePanel}
            onNavigateToNote={handleSelectNote}
            onRefreshAll={refreshAll}
            navigationHistory={navigationHistory}
            onGoBack={handleGoBack}
          />
        )}
      </div>

      {/* Export / Import Modal */}
      <ExportImportModal
        isOpen={isExportImportOpen}
        onClose={() => setIsExportImportOpen(false)}
        onRefreshAll={refreshAll}
      />

      {/* Trash Modal */}
      <TrashModal
        isOpen={isTrashOpen}
        onClose={() => setIsTrashOpen(false)}
        onRefreshAll={refreshAll}
      />

      {/* Activity & Backups Modal */}
      <ActivityModal
        isOpen={isActivityOpen}
        onClose={() => setIsActivityOpen(false)}
        onRefreshAll={refreshAll}
      />

      {/* Graph Insights Panel */}
      <InsightsPanel
        isOpen={isInsightsOpen}
        onClose={() => setIsInsightsOpen(false)}
        insights={insightsData}
        loading={loadingInsights}
        onRefresh={fetchInsights}
        onSelectTag={(tag) => setSelectedTag(tag)}
        onSelectGroup={(group) => setSelectedTag(group)}
      />

      {/* Toast Notifications */}
      <ToastContainer />
    </div>
  );
};
