-- Calmer, compact seed data for Personal Knowledge Graph System (8 notes, 7 links, 2 orphans)

-- 1. Insert Tags
INSERT INTO tags (id, name) VALUES
(1, 'computer-science'),
(2, 'math'),
(3, 'algorithms'),
(4, 'search'),
(5, 'nlp'),
(6, 'database'),
(7, 'productivity'),
(8, 'quantum'),
(9, 'hobby');

-- 2. Insert Notes
INSERT INTO notes (id, title, content, pinned, created_at, updated_at) VALUES
(1, 'Graph Theory', 'Study of graphs and networks. Foundation for [[Breadth-First Search]].', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'Knowledge Graphs', 'Interlinked graph structures for knowledge representation. Related to [[Graph Theory]] and [[Information Retrieval]].', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 'Breadth-First Search', 'Traversal algorithm for graphs. Connects back to [[Graph Theory]].', 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(4, 'Information Retrieval', 'Techniques for searching and indexing text collections like [[Full-Text Search]].', 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(5, 'Full-Text Search', 'Fast text search engines relying on [[Information Retrieval]].', 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(6, 'Personal Knowledge Management', 'Methods for organizing notes using tools like [[Knowledge Graphs]].', 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(7, 'Quantum Computing', 'Quantum mechanical phenomena applied to computation.', 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(8, 'Gardening Notes', 'Seasonal care tips for indoor houseplants and herbs.', 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 3. Note Tags
INSERT INTO note_tags (note_id, tag_id) VALUES
(1, 1), (1, 2),
(2, 1), (2, 7),
(3, 1), (3, 3),
(4, 4), (4, 5),
(5, 4), (5, 6),
(6, 7),
(7, 8),
(8, 9);

-- 4. Links (Directed, including two-way mutual connections)
INSERT INTO links (source_id, target_id, origin) VALUES
(1, 3, 'auto'),
(3, 1, 'auto'),
(2, 1, 'auto'),
(2, 4, 'auto'),
(4, 5, 'auto'),
(5, 4, 'auto'),
(6, 2, 'auto');

-- 5. FTS Index
INSERT INTO notes_fts (rowid, title, content, tags) VALUES
(1, 'Graph Theory', 'Study of graphs and networks. Foundation for [[Breadth-First Search]].', 'computer-science math'),
(2, 'Knowledge Graphs', 'Interlinked graph structures for knowledge representation. Related to [[Graph Theory]] and [[Information Retrieval]].', 'computer-science productivity'),
(3, 'Breadth-First Search', 'Traversal algorithm for graphs. Connects back to [[Graph Theory]].', 'computer-science algorithms'),
(4, 'Information Retrieval', 'Techniques for searching and indexing text collections like [[Full-Text Search]].', 'search nlp'),
(5, 'Full-Text Search', 'Fast text search engines relying on [[Information Retrieval]].', 'search database'),
(6, 'Personal Knowledge Management', 'Methods for organizing notes using tools like [[Knowledge Graphs]].', 'productivity'),
(7, 'Quantum Computing', 'Quantum mechanical phenomena applied to computation.', 'quantum'),
(8, 'Gardening Notes', 'Seasonal care tips for indoor houseplants and herbs.', 'hobby');
