# Personal Knowledge Graph System

A complete, high-performance, deterministic **Personal Knowledge Graph System** featuring a **FastAPI** backend with **SQLite FTS5**, a reactive **React + Vite** frontend with **Cytoscape.js** interactive graph visualization, a generated **Python SDK**, and pure-Python classical Information Retrieval & rule-based NLP—**with zero external AI, LLM, or embeddings dependencies**.

---

## Architecture Overview

```
+-----------------------------------------------------------------------------------+
|                              React Frontend (Vite)                                |
|  - Cytoscape.js Interactive Graph (Force-directed, Circular, Concentric)          |
|  - Real-time Markdown Editor with Live [[Wikilink]] clickable preview             |
|  - Global Search with Prefix/Substring/Fuzzy Typo-Tolerant Autocomplete           |
|  - Tag Input with Live Suggestions & Unresolved Link Badges                       |
|  - SSE (Server-Sent Events) live multi-client synchronization                     |
+-----------------------------------------+-----------------------------------------+
                                          | Axios HTTP / EventSource SSE
+-----------------------------------------v-----------------------------------------+
|                               FastAPI Backend (Port 8000)                         |
|  +-----------------------------------------------------------------------------+  |
|  | Routers: /notes, /graph, /tags, /search, /system, /events                   |  |
|  +-----------------------------------------------------------------------------+  |
|  | Business Services Layer:                                                    |  |
|  | - NoteService (Wikilink parser, Title rename rewriter, Pending links)       |  |
|  | - LinkService (Manual/Auto edge reconciliation, cycle & self-link checks)   |  |
|  | - SearchService (SQLite FTS5 BM25 ranking, column weights, fuzzy fallback)  |  |
|  | - GraphService (Cycle-safe BFS traversal, neighborhood, shortest path)      |  |
|  | - IOService (JSON export & duplicate-tolerant import)                       |  |
|  +-----------------------------------------------------------------------------+  |
|  | Pure Python NLP & Classic IR Engine:                                        |  |
|  | - Word Regex Tokenizer & Stopword Filter                                    |  |
|  | - Pure-Python Suffix/Porter Stemmer                                         |  |
|  | - In-Memory TF-IDF Vector Space Model & Cosine Similarity                   |  |
|  | - Difflib SequenceMatcher for Typo Tolerance & Fuzzy Search                 |  |
|  +-----------------------------------------------------------------------------+  |
|  | Repositories Layer (SQLAlchemy 2.x ORM & Direct SQL)                        |  |
+-----------------------------------------+-----------------------------------------+
                                          | SQLite PRAGMA foreign_keys=ON; WAL Mode
+-----------------------------------------v-----------------------------------------+
|                          SQLite Database Engine (FTS5)                            |
|  - notes (id, title, content, pinned, created_at, updated_at)                     |
|  - links (source_id, target_id, origin: 'auto' | 'manual')                        |
|  - tags (id, name), note_tags (note_id, tag_id)                                   |
|  - notes_fts (FTS5 Virtual Table: title, content, tags with BM25)                 |
|  - pending_links (source_id, target_title_lower)                                  |
+-----------------------------------------------------------------------------------+
```

---

## How Smart Features Work Without an LLM / Cloud AI

1. **[[Wikilink]] Extraction & Auto-Linking**:
   - Parses `[[Title]]` and `[[Title|Alias]]` using deterministic regexes.
   - Ignores code spans inside inline backticks (`` `...` ``) and fenced blocks (```` ```...``` ````).
   - Case-insensitively resolves titles to existing notes.
   - Automatically synchronizes `origin='auto'` links in the graph while preserving `origin='manual'` links.
2. **Pending Links & Automatic Resolution**:
   - Unresolved `[[Nonexistent]]` targets are stored in `pending_links` and badged in the UI.
   - When a note with that title is later created or renamed, the pending links instantly resolve into graph edges.
3. **Title Rename Propagation**:
   - Renaming note $A$ scans all notes referencing $[[A]]$ and rewrites them to $[[A_{new}]]$, keeping all aliases intact and re-indexing the FTS table.
4. **Full-Text Search with BM25 & Column Weights**:
   - SQLite FTS5 matches queries across `title`, `content`, and `tags`.
   - Column weights prioritize title matches ($10.0\times$), followed by tags ($5.0\times$), then content ($1.0\times$).
   - Multi-word prefix matching (`query*`) and `#tag` syntax (e.g. `python #algorithms`) are supported natively.
5. **Fuzzy Typo-Tolerant Fallback**:
   - If FTS returns few results, pure Python `difflib.SequenceMatcher` computes word-level and string similarity against all titles and tags (e.g., `"pyhton"` accurately finds `"Python Programming Language"`).
6. **TF-IDF Related Notes & Link Suggester**:
   - Computes document Term Frequency-Inverse Document Frequency vectors and cosine similarity across all notes in memory.
   - Boosts similarity by shared tags and excludes already-linked notes to suggest high-value new connections.
7. **Graph Traversal & Shortest Path**:
   - Cycle-safe Breadth-First Search (BFS) explores neighborhood subgraphs up to depth 4 and computes shortest paths between any two notes.

---

## Project Structure

```
knowledge-graph/
├── main.py                       # FastAPI application entrypoint & CORS setup
├── requirements.txt              # Backend dependencies
├── alembic.ini                   # Alembic database migration config
├── alembic/
│   ├── env.py
│   └── versions/
│       ├── 001_initial_schema.py           # Core schema (notes, links, tags, note_tags)
│       └── 002_add_fts_origins_pending.py  # FTS5, origins, pending_links, pinned
├── seed_data.sql                 # 16 rich interlinked seed notes
├── scripts/
│   └── load_seed.py              # Seed database loader script
├── app/
│   ├── core/                     # Database, config, DI, exceptions, error handlers
│   ├── models/                   # Note, Tag, Link, NoteTag, PendingLink
│   ├── schemas/                  # Pydantic v2 validation models
│   ├── repositories/             # NoteRepository, TagRepository, LinkRepository, FTSRepository
│   ├── services/                 # NoteService, LinkService, TagService, SearchService, GraphService, IOService
│   ├── nlp/                      # Normalizer, Tokenizer, Stopwords, Stemmer, Wikilinks, TF-IDF, Fuzzy
│   └── routers/                  # /notes, /graph, /tags, /search, /system
├── tests/                        # Comprehensive Pytest test suite (22 unit & integration tests)
├── knowledge_sdk/                # Python SDK generated via OpenAPI Generator CLI
├── examples/
│   └── sdk_demo.py               # SDK usage demonstration script
├── frontend/                     # React + Vite + Cytoscape.js application
│   ├── src/api/                  # Typed Axios API client
│   ├── src/components/           # TopBar, Sidebar, GraphCanvas, NoteDetailPanel, Modals
│   ├── src/context/              # Toast context & notification system
│   └── src/styles/               # White/light-blue theme & layout styles
├── setupdev.bat                  # One-click Windows development setup script
├── runapplication.bat            # Windows dual-process launcher
└── README.md
```

---

## Quick Start (Windows)

### 1. Automatic Setup
Run `setupdev.bat`:
```cmd
setupdev.bat
```
This script will:
- Check for Python 3.11+ and Node.js 18+.
- Create a Python virtual environment (`env`).
- Install all backend dependencies and the `knowledge_sdk`.
- Run database migrations (`alembic upgrade head`).
- Prompt to load the rich seed dataset.
- Install all frontend npm dependencies.

### 2. Run the Application
Run `runapplication.bat`:
```cmd
runapplication.bat
```
This starts both servers in their own dedicated command windows:
- **Frontend App**: [http://localhost:3000](http://localhost:3000)
- **FastAPI Backend**: [http://localhost:8000](http://localhost:8000)
- **Swagger Interactive API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **OpenAPI Schema**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

---

## Keyboard Shortcuts

| Key | Action |
| --- | --- |
| `/` | Focus global search bar |
| `N` | Create a new note |
| `E` | Toggle Graph Edit Mode |
| `Esc` | Close note detail panel |

---

## Python SDK Usage

The Python SDK in `knowledge_sdk/` was generated directly with OpenAPI Generator CLI.

> **Note**: Generating or updating the SDK via `generate_sdk.bat` requires Java 11+ and Node.js.

### Example Code
```python
from knowledge_sdk import ApiClient, Configuration
from knowledge_sdk.api.notes_api import NotesApi
from knowledge_sdk.models.note_create import NoteCreate
from knowledge_sdk.models.link_create import LinkCreate

# 1. Initialize API Client
client = ApiClient(Configuration(host="http://localhost:8000"))
api = NotesApi(client)

# 2. List Notes
notes = api.list_notes()
print(f"Total Notes: {len(notes)}")

# 3. Create Notes
note_a = api.create_note(NoteCreate(title="SDK Demo Note A", content="Created via SDK."))
note_b = api.create_note(NoteCreate(title="SDK Demo Note B", content="Target note."))

# 4. Link Notes
api.link_notes(note_id=note_a.id, link_create=LinkCreate(target_id=note_b.id))

# 5. Get Backlinks
backlinks = api.get_note_backlinks(note_id=note_b.id)
print(f"Backlinks for Note B: {[b.title for b in backlinks]}")
```

Run the built-in demo script:
```cmd
.\env\Scripts\python examples/sdk_demo.py
```

---

## Running Tests

Run the full pytest suite:
```cmd
.\env\Scripts\pytest -v
```

All 22 unit and integration tests cover:
- Note CRUD, case-insensitive title uniqueness, input bounds.
- Wikilink parsing, code block masking, alias resolution, self-link rejection.
- Automatic link synchronization, manual link preservation, pending link resolution.
- Rename propagation across referencing notes and cascade deletion.
- SQLite FTS5 search, #tag syntax, prefix queries, fuzzy typo fallback.
- TF-IDF similarity, tag co-occurrence suggestions, unlinked mentions.
- Graph BFS neighborhood, cycle resilience ($A \leftrightarrow B$), and shortest path traversal.
- Full JSON export and duplicate-tolerant import roundtrip.
- Standardized error handling ($400, 404, 409, 422, 500$).

---

## Standardized Error Response Format

All error responses from the API adhere to a consistent JSON structure:
```json
{
  "error": "CONFLICT",
  "message": "A note with title 'Graph Theory' already exists.",
  "details": {}
}
```

| HTTP Status | Error Code | Description |
| --- | --- | --- |
| `400` | `BAD_REQUEST` | Self-loop link or invalid operation |
| `404` | `NOT_FOUND` | Note or link does not exist |
| `409` | `CONFLICT` | Duplicate title or duplicate link |
| `422` | `VALIDATION_ERROR` | Malformed input, oversized text, or tag limits |
| `500` | `INTERNAL_SERVER_ERROR` | Unexpected server error (logged securely) |

---

## Future Extensions

1. **Hierarchical Tag Taxonomies**: Nested tags (e.g., `#math/graph-theory/trees`).
2. **Graph Clustering / Community Detection**: Pure-Python Louvain community detection for automatic note clustering.
3. **Markdown File Importer/Exporter**: Direct syncing with Obsidian or Logseq `.md` directories.
