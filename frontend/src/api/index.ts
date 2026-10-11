import { apiClient } from './client';
import axios, { CancelTokenSource } from 'axios';

export interface NoteListItem {
  id: number;
  title: string;
  content_snippet: string;
  tags: string[];
  outgoing_link_count: number;
  backlink_count: number;
  pinned: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface LinkRead {
  source_id: number;
  target_id: number;
  origin: string;
  source_title?: string;
  target_title?: string;
}

export interface NoteBacklinkItem {
  id: number;
  title: string;
  origin: string;
}

export interface RelatedNoteItem {
  id: number;
  title: string;
  score: number;
  shared_tags: string[];
}

export interface UnlinkedMentionItem {
  note_id: number;
  note_title: string;
  snippet: string;
}

export interface NoteDetail {
  id: number;
  title: string;
  content: string;
  tags: string[];
  pinned: boolean;
  created_at?: string;
  updated_at?: string;
  outgoing_links: LinkRead[];
  backlinks: NoteBacklinkItem[];
  unresolved_links: string[];
  related_notes: RelatedNoteItem[];
}

export interface NoteCreatePayload {
  title: string;
  content?: string;
  tags?: string[];
}

export interface NoteUpdatePayload {
  title: string;
  content?: string;
  tags?: string[];
}

export interface NotePatchPayload {
  title?: string;
  content?: string;
  tags?: string[];
  pinned?: boolean;
}

export interface GraphNode {
  id: string;
  label: string;
  tags: string[];
  connection_count: number;
  pinned: boolean;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  origin: string;
  mutual?: boolean;
  direction?: string;
}

export interface GraphResponse {
  nodes: GraphNode[];
  edges: GraphEdge[];
  adjacency_list: Record<string, string[]>;
  outgoing_ids?: string[];
  backlink_ids?: string[];
  mutual_ids?: string[];
}

export interface HubStat {
  id: number;
  title: string;
  link_count: number;
}

export interface TagDistributionStat {
  tag: string;
  count: number;
}

export interface GraphStats {
  total_notes: number;
  total_links: number;
  total_tags: number;
  orphan_count: number;
  orphans: string[];
  hubs: HubStat[];
  tag_distribution: TagDistributionStat[];
}

export interface ShortestPathResponse {
  source_id: number;
  target_id: number;
  found: boolean;
  path: number[];
  path_titles: string[];
  length: number;
}

export interface NotesByTagItem {
  tag: string;
  count: number;
}

export interface NotesByGroupItem {
  group: string;
  count: number;
}

export interface NotesPerDayItem {
  date: string;
  count: number;
}

export interface TopConnectedItem {
  id: number;
  title: string;
  degree: number;
}

export interface ConnectedVsOrphans {
  connected: number;
  orphans: number;
}

export interface LinkTypes {
  auto: number;
  manual: number;
  mutual: number;
}

export interface GraphInsightsResponse {
  notes_by_tag: NotesByTagItem[];
  notes_by_group: NotesByGroupItem[];
  notes_per_day: NotesPerDayItem[];
  top_connected: TopConnectedItem[];
  connected_vs_orphans: ConnectedVsOrphans;
  link_types: LinkTypes;
}

export interface TagUsage {
  id: number;
  name: string;
  count: number;
}

export interface TagSuggestion {
  name: string;
  count: number;
  score: number;
}

export interface TagSuggestResponse {
  query: string;
  suggestions: TagSuggestion[];
}

export interface SearchResultItem {
  id: number;
  title: string;
  snippet: string;
  tags: string[];
  score: number;
  match_type: string;
}

export interface SearchResponse {
  query: string;
  total: number;
  results: SearchResultItem[];
}

export interface AutocompleteItem {
  type: 'note' | 'tag';
  id?: number;
  title: string;
  score: number;
}

export interface AutocompleteResponse {
  query: string;
  results: AutocompleteItem[];
}

export interface TitleSuggestItem {
  id: number;
  title: string;
}

export interface TitleSuggestResponse {
  query: string;
  results: TitleSuggestItem[];
}

export interface SuggestedLinkRead {
  target_id: number;
  target_title: string;
  similarity_score: number;
  shared_tags: string[];
}

// Global active autocomplete token for request cancellation
let autocompleteCancelSource: CancelTokenSource | null = null;

// API calls
export const notesApi = {
  list: (params?: { tag?: string; q?: string; limit?: number; offset?: number; sort?: string; pinned?: boolean }) =>
    apiClient.get<NoteListItem[]>('/notes/', { params }).then((r) => r.data),

  get: (id: number) =>
    apiClient.get<NoteDetail>(`/notes/${id}`).then((r) => r.data),

  create: (payload: NoteCreatePayload) =>
    apiClient.post<NoteDetail>('/notes/', payload).then((r) => r.data),

  update: (id: number, payload: NoteUpdatePayload) =>
    apiClient.put<NoteDetail>(`/notes/${id}`, payload).then((r) => r.data),

  patch: (id: number, payload: NotePatchPayload) =>
    apiClient.patch<NoteDetail>(`/notes/${id}`, payload).then((r) => r.data),

  delete: (id: number) =>
    apiClient.delete<{ id: number; title: string; message: string }>(`/notes/${id}`).then((r) => r.data),

  link: (sourceId: number, targetId: number) =>
    apiClient.patch<LinkRead>(`/notes/${sourceId}/link`, { target_id: targetId }).then((r) => r.data),

  unlink: (sourceId: number, targetId: number) =>
    apiClient.delete<{ source_id: number; target_id: number; message: string }>(`/notes/${sourceId}/link/${targetId}`).then((r) => r.data),

  getBacklinks: (id: number) =>
    apiClient.get<NoteBacklinkItem[]>(`/notes/${id}/backlinks`).then((r) => r.data),

  getRelated: (id: number, limit = 5) =>
    apiClient.get<RelatedNoteItem[]>(`/notes/${id}/related`, { params: { limit } }).then((r) => r.data),

  getMentions: (id: number) =>
    apiClient.get<UnlinkedMentionItem[]>(`/notes/${id}/mentions`).then((r) => r.data),
};

export const graphApi = {
  getFullGraph: (tag?: string) =>
    apiClient.get<GraphResponse>('/graph/', { params: { tag } }).then((r) => r.data),

  getNeighborhood: (noteId: number, depth = 1) =>
    apiClient.get<GraphResponse>(`/graph/neighbors/${noteId}`, { params: { depth } }).then((r) => r.data),

  getShortestPath: (source: number, target: number) =>
    apiClient.get<ShortestPathResponse>('/graph/path', { params: { source, target } }).then((r) => r.data),

  getStats: () =>
    apiClient.get<GraphStats>('/graph/stats').then((r) => r.data),

  getInsights: () =>
    apiClient.get<GraphInsightsResponse>('/graph/insights').then((r) => r.data),
};

export const tagsApi = {
  list: () =>
    apiClient.get<TagUsage[]>('/tags/').then((r) => r.data),

  suggest: (q: string, selected?: string[], content?: string, limit = 10) =>
    apiClient.get<TagSuggestResponse>('/tags/suggest', {
      params: { q, selected, content, limit },
    }).then((r) => r.data),
};

export const searchApi = {
  search: (q: string, tag?: string, limit = 50) =>
    apiClient.get<SearchResponse>('/search/', { params: { q, tag, limit } }).then((r) => r.data),

  autocomplete: (q: string, limit = 10) => {
    if (autocompleteCancelSource) {
      autocompleteCancelSource.cancel('Stale autocomplete request cancelled');
    }
    autocompleteCancelSource = axios.CancelToken.source();
    return apiClient
      .get<AutocompleteResponse>('/search/suggest', {
        params: { q, limit },
        cancelToken: autocompleteCancelSource.token,
      })
      .then((r) => r.data)
      .catch((err) => {
        if (axios.isCancel(err)) {
          return { query: q, results: [] };
        }
        throw err;
      });
  },

  suggestTitles: (q: string, limit = 10) =>
    apiClient.get<TitleSuggestResponse>('/titles/suggest', { params: { q, limit } }).then((r) => r.data),

  suggestLinks: (noteId: number, limit = 5) =>
    apiClient.get<SuggestedLinkRead[]>('/suggest/links', { params: { note_id: noteId, limit } }).then((r) => r.data),
};

export interface BackupItemRead {
  filename: string;
  size_bytes: number;
  created_at: string;
}

export interface ActivityLogRead {
  id: number;
  ts: string;
  action: string;
  entity: string;
  entity_id?: number | null;
  title?: string | null;
  detail?: string | null;
}

export const systemApi = {
  exportData: () =>
    apiClient.get<any>('/export').then((r) => r.data),

  importData: (payload: any) =>
    apiClient.post<any>('/import', payload).then((r) => r.data),

  resetDatabase: (confirm = 'DELETE ALL') =>
    apiClient.delete<{ status: string; message: string }>('/system/reset', { data: { confirm } }).then((r) => r.data),

  health: () =>
    apiClient.get<{ status: string; service: string; database_path?: string; backups_count?: number }>('/health').then((r) => r.data),

  getBackups: () =>
    apiClient.get<BackupItemRead[]>('/system/backups').then((r) => r.data),

  restoreBackup: (filename: string, confirm = 'RESTORE') =>
    apiClient.post<{ status: string; message: string }>('/system/backups/restore', { filename, confirm }).then((r) => r.data),

  getActivity: (limit = 50) =>
    apiClient.get<ActivityLogRead[]>('/system/activity', { params: { limit } }).then((r) => r.data),
};

export interface TrashItemRead {
  id: number;
  original_note_id: number;
  title: string;
  deleted_at: string;
}

export const trashApi = {
  list: () =>
    apiClient.get<TrashItemRead[]>('/trash/').then((r) => r.data),

  get: (id: number) =>
    apiClient.get<TrashItemRead & { snapshot_json: any }>(`/trash/${id}`).then((r) => r.data),

  restore: (id: number) =>
    apiClient.post<NoteDetail>(`/trash/${id}/restore`).then((r) => r.data),

  purge: () =>
    apiClient.post<{ purged_count: number; message: string }>('/trash/purge').then((r) => r.data),

  permanentDelete: (id: number) =>
    apiClient.delete<{ id: number; message: string }>(`/trash/${id}`).then((r) => r.data),
};

export interface TagAssistResponse {
  normalized: string[];
  suggestions: { tag: string; reason: string }[];
  merges: { from: string[]; to: string }[];
  corrections: { from: string; to: string }[];
}

export interface ProofreadIssue {
  start: number;
  end: number;
  original: string;
  suggestion: string;
  reason: string;
}

export interface LinkSuggestionItem {
  note_id: number;
  title: string;
  score: number;
  reasons: string[];
}

export interface AssistStatusResponse {
  enabled: boolean;
  provider: string;
  model: string | null;
}

export const assistApi = {
  assistTags: (payload: { title?: string; content?: string; tags?: string[] }) =>
    apiClient.post<TagAssistResponse>('/assist/tags', payload).then((r) => r.data),

  proofread: (text: string, ignored_words?: string[]) =>
    apiClient.post<ProofreadIssue[]>('/assist/proofread', { text, ignored_words }).then((r) => r.data),

  getLinkSuggestions: (noteId: number) =>
    apiClient.get<LinkSuggestionItem[]>('/assist/link-suggestions', { params: { note_id: noteId } }).then((r) => r.data),

  dismissLinkSuggestion: (noteId: number, otherId: number) =>
    apiClient.post<{ status: string; message: string }>('/assist/link-suggestions/dismiss', { note_id: noteId, other_id: otherId }).then((r) => r.data),

  getStatus: () =>
    apiClient.get<AssistStatusResponse>('/assist/status').then((r) => r.data),
};

