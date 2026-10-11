import React, { useEffect, useRef, useState, useCallback, useMemo } from 'react';
import cytoscape from 'cytoscape';
// @ts-ignore
import coseBilkent from 'cytoscape-cose-bilkent';
import { GraphResponse, GraphStats, graphApi, notesApi } from '../api';
import { useToast } from '../context/ToastContext';
import {
  ZoomIn,
  ZoomOut,
  Maximize2,
  Layers,
  Route,
  HelpCircle,
  Eye,
  ChevronDown,
  ChevronUp,
  X,
  FileText,
  Plus,
  Sliders,
} from 'lucide-react';

try {
  cytoscape.use(coseBilkent);
} catch (e) {
  // Already registered
}

interface GraphCanvasProps {
  graphData: GraphResponse | null;
  stats: GraphStats | null;
  selectedNoteId: number | null;
  isEditMode: boolean;
  onSelectNote: (id: number) => void;
  onNewNote?: () => void;
  onRefreshGraph: () => void;
  neighborhoodDepth: number;
  onChangeDepth: (d: number) => void;
  graphTagFilter: string | null;
  onChangeGraphTagFilter: (tag: string | null) => void;
  onClearSelection?: () => void;
}

export const GraphCanvas: React.FC<GraphCanvasProps> = ({
  graphData,
  stats,
  selectedNoteId,
  isEditMode,
  onSelectNote,
  onNewNote,
  onRefreshGraph,
  neighborhoodDepth,
  onChangeDepth,
  graphTagFilter,
  onChangeGraphTagFilter,
  onClearSelection,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<cytoscape.Core | null>(null);
  const savedPositions = useRef<Record<string, { x: number; y: number }>>({});
  const initialLayoutRun = useRef<boolean>(false);
  const { showToast } = useToast();

  const [layoutName, setLayoutName] = useState<'cose' | 'circle' | 'concentric' | 'breadthfirst'>('cose');
  const [showLegend, setShowLegend] = useState(true);
  const [showUnlinkedTray, setShowUnlinkedTray] = useState(false);
  const [linkSourceNode, setLinkSourceNode] = useState<{ id: string; label: string } | null>(null);
  const [pathSource, setPathSource] = useState<number | null>(null);
  const [pathTarget, setPathTarget] = useState<number | null>(null);
  const [isPathMode, setIsPathMode] = useState(false);

  // Identify unlinked nodes (0 connections)
  const unlinkedNodes = useMemo(() => {
    if (!graphData) return [];
    return graphData.nodes.filter((n) => n.connection_count === 0);
  }, [graphData]);

  // Compute focus stats when a note is selected
  const focusStats = useMemo(() => {
    if (!selectedNoteId || !graphData) {
      return null;
    }
    const selStr = `${selectedNoteId}`;
    let outgoingCount = 0;
    let backlinkCount = 0;
    let mutualCount = 0;

    graphData.edges.forEach((e) => {
      if (e.mutual && (e.source === selStr || e.target === selStr)) {
        mutualCount++;
      } else if (e.source === selStr) {
        outgoingCount++;
      } else if (e.target === selStr) {
        backlinkCount++;
      }
    });

    return {
      outgoing: outgoingCount,
      backlinks: backlinkCount,
      mutual: mutualCount,
      unlinked: unlinkedNodes.length,
    };
  }, [selectedNoteId, graphData, unlinkedNodes]);

  // Build / Update Cytoscape instance
  useEffect(() => {
    if (!containerRef.current || !graphData) return;

    // Build Cytoscape elements
    const elements: cytoscape.ElementDefinition[] = [];

    // Nodes
    graphData.nodes.forEach((n) => {
      const pos = savedPositions.current[n.id];
      elements.push({
        group: 'nodes',
        data: {
          id: n.id,
          label: n.label,
          connectionCount: n.connection_count,
          pinned: n.pinned,
          tags: n.tags,
        },
        position: pos ? { x: pos.x, y: pos.y } : undefined,
      });
    });

    // Edges
    graphData.edges.forEach((e) => {
      elements.push({
        group: 'edges',
        data: {
          id: e.id,
          source: e.source,
          target: e.target,
          origin: e.origin,
          mutual: !!e.mutual || e.direction === 'mutual',
          direction: e.direction || (e.mutual ? 'mutual' : 'directed'),
        },
      });
    });

    if (cyRef.current) {
      cyRef.current.destroy();
    }

    const cy = cytoscape({
      container: containerRef.current,
      elements,
      boxSelectionEnabled: false,
      style: [
        // Base Node Style
        {
          selector: 'node',
          style: {
            'label': 'data(label)',
            'font-family': 'Inter, system-ui, sans-serif',
            'font-size': '11px',
            'font-weight': 600,
            'color': '#1F1B2E',
            'text-valign': 'bottom',
            'text-margin-y': 6,
            'text-wrap': 'ellipsis',
            'text-max-width': '110px',
            'text-background-color': '#FFFFFF',
            'text-background-opacity': 0.85,
            'text-background-padding': '3px',
            'text-background-shape': 'roundrectangle',
            'background-color': '#FFFFFF',
            'border-width': 2,
            'border-color': '#7C3AED',
            'width': 'mapData(connectionCount, 0, 10, 28, 56)',
            'height': 'mapData(connectionCount, 0, 10, 28, 56)',
            'transition-property': 'background-color, border-color, width, height, opacity',
            'transition-duration': 0.2,
          },
        },
        // Low Zoom: Hide labels to keep viewport clean
        {
          selector: '.low-zoom node:unselected',
          style: {
            'text-opacity': 0,
            'text-background-opacity': 0,
          },
        },
        // Pinned Node
        {
          selector: 'node[?pinned]',
          style: {
            'background-color': '#F3EEFF',
            'border-color': '#5B21B6',
            'border-width': 3,
          },
        },
        // Edges: STRAIGHT LINES ONLY, NO CURVED OR DASHED
        {
          selector: 'edge',
          style: {
            'curve-style': 'straight',
            'line-style': 'solid',
            'width': 1.8,
            'line-color': '#DDD6FE',
            'target-arrow-shape': 'triangle',
            'target-arrow-color': '#7C3AED',
            'arrow-scale': 1.0,
            'transition-property': 'line-color, width, opacity',
            'transition-duration': 0.2,
          },
        },
        // Manual Links: Solid Primary Violet
        {
          selector: 'edge[origin = "manual"]',
          style: {
            'line-color': '#7C3AED',
            'target-arrow-color': '#7C3AED',
            'width': 2.2,
          },
        },
        // Mutual Edges: Indigo with Double Arrowheads
        {
          selector: 'edge[?mutual]',
          style: {
            'curve-style': 'straight',
            'line-style': 'solid',
            'line-color': '#4F46E5',
            'source-arrow-shape': 'triangle',
            'target-arrow-shape': 'triangle',
            'source-arrow-color': '#4F46E5',
            'target-arrow-color': '#4F46E5',
            'width': 2.5,
          },
        },
        // Focus Mode Styles with Calm Soft Glow
        {
          selector: 'node.focused-selected',
          style: {
            'background-color': '#7C3AED',
            'border-color': '#5B21B6',
            'border-width': 3,
            'color': '#FFFFFF',
            'text-background-color': '#7C3AED',
            'text-background-opacity': 1.0,
            'underlay-color': '#7C3AED',
            'underlay-opacity': 0.18,
            'underlay-padding': 8,
            'underlay-shape': 'ellipse',
            'z-index': 1000,
          },
        },
        {
          selector: 'node.focused-outgoing',
          style: {
            'border-color': '#7C3AED',
            'border-width': 3,
            'background-color': '#F3EEFF',
            'underlay-color': '#7C3AED',
            'underlay-opacity': 0.15,
            'underlay-padding': 6,
            'underlay-shape': 'ellipse',
            'z-index': 900,
          },
        },
        {
          selector: 'node.focused-backlink',
          style: {
            'border-color': '#EC4899',
            'border-width': 3,
            'background-color': '#FDF2F8',
            'underlay-color': '#EC4899',
            'underlay-opacity': 0.15,
            'underlay-padding': 6,
            'underlay-shape': 'ellipse',
            'z-index': 900,
          },
        },
        {
          selector: 'node.focused-mutual',
          style: {
            'border-color': '#4F46E5',
            'border-width': 3,
            'background-color': '#EEF2FF',
            'underlay-color': '#4F46E5',
            'underlay-opacity': 0.15,
            'underlay-padding': 6,
            'underlay-shape': 'ellipse',
            'z-index': 900,
          },
        },
        {
          selector: 'edge.focused-edge-outgoing',
          style: {
            'line-color': '#7C3AED',
            'target-arrow-color': '#7C3AED',
            'width': 2.6,
            'z-index': 800,
          },
        },
        {
          selector: 'edge.focused-edge-backlink',
          style: {
            'line-color': '#EC4899',
            'target-arrow-color': '#EC4899',
            'width': 2.6,
            'z-index': 800,
          },
        },
        {
          selector: 'edge.focused-edge-mutual',
          style: {
            'line-color': '#4F46E5',
            'source-arrow-color': '#4F46E5',
            'target-arrow-color': '#4F46E5',
            'width': 2.8,
            'z-index': 800,
          },
        },
        // Dimmed Non-focused Elements (fade to 35% opacity keeping context)
        {
          selector: '.dimmed',
          style: {
            'opacity': 0.35,
          },
        },
        // Path Highlight Mode
        {
          selector: '.path-highlighted',
          style: {
            'border-color': '#E5484D',
            'border-width': 4,
            'background-color': '#FFF1F2',
            'line-color': '#E5484D',
            'target-arrow-color': '#E5484D',
            'width': 3.5,
            'z-index': 1000,
          },
        },
      ],
    });

    cyRef.current = cy;

    // Zoom listener to hide labels when zoom < 0.6
    cy.on('zoom', () => {
      const z = cy.zoom();
      if (z < 0.6) {
        cy.container()?.classList.add('low-zoom');
        cy.elements().addClass('low-zoom');
      } else {
        cy.container()?.classList.remove('low-zoom');
        cy.elements().removeClass('low-zoom');
      }
    });

    // Check if we need to run layout: only run layout initially or if nodes don't have positions
    const hasUnpositioned = graphData.nodes.some((n) => !savedPositions.current[n.id]);
    if (!initialLayoutRun.current || hasUnpositioned) {
      initialLayoutRun.current = true;
      runLayout();
    }

    // Save positions when nodes move
    cy.on('dragfree', 'node', (evt) => {
      const node = evt.target;
      savedPositions.current[node.id()] = { ...node.position() };
    });

    // Node click handler
    cy.on('tap', 'node', (evt) => {
      const node = evt.target;
      const id = parseInt(node.id(), 10);

      if (isPathMode) {
        if (!pathSource) {
          setPathSource(id);
          showToast({ type: 'info', message: `Start node: ${node.data('label')}. Now click target node.` });
        } else if (!pathTarget && id !== pathSource) {
          setPathTarget(id);
          highlightShortestPath(pathSource, id);
        }
        return;
      }

      if (isEditMode && linkSourceNode) {
        const srcId = parseInt(linkSourceNode.id, 10);
        if (srcId === id) {
          showToast({ type: 'error', message: 'Cannot link a note to itself.' });
          setLinkSourceNode(null);
          return;
        }

        notesApi
          .link(srcId, id)
          .then(() => {
            showToast({ type: 'success', message: `Linked '${linkSourceNode.label}' -> '${node.data('label')}'` });
            onRefreshGraph();
          })
          .catch((err) => {
            showToast({ type: 'error', message: err.message });
          })
          .finally(() => {
            setLinkSourceNode(null);
          });
        return;
      }

      onSelectNote(id);
    });

    // Edge click handler in Edit Mode (delete link)
    cy.on('tap', 'edge', (evt) => {
      if (!isEditMode) return;
      const edge = evt.target;
      const srcId = parseInt(edge.data('source'), 10);
      const tgtId = parseInt(edge.data('target'), 10);

      if (window.confirm(`Delete link between Note ${srcId} and Note ${tgtId}?`)) {
        notesApi
          .unlink(srcId, tgtId)
          .then(() => {
            showToast({ type: 'success', message: 'Link removed.' });
            onRefreshGraph();
          })
          .catch((err) => {
            showToast({ type: 'error', message: err.message });
          });
      }
    });

    // Double click empty canvas to create new note
    cy.on('dbltap', (evt) => {
      if (evt.target === cy) {
        const title = prompt('Enter title for new note:');
        if (title && title.trim()) {
          notesApi
            .create({ title: title.trim(), content: '' })
            .then((newNote) => {
              showToast({ type: 'success', message: `Note '${newNote.title}' created!` });
              onRefreshGraph();
              onSelectNote(newNote.id);
            })
            .catch((err) => {
              showToast({ type: 'error', message: err.message });
            });
        }
      }
    });

    // Tap on empty canvas clears selection
    cy.on('tap', (evt) => {
      if (evt.target === cy) {
        if (onClearSelection) {
          onClearSelection();
        }
      }
    });

    return () => {
      if (cyRef.current) {
        // Save current positions before destroying
        cyRef.current.nodes().forEach((n) => {
          savedPositions.current[n.id()] = { ...n.position() };
        });
      }
      cy.destroy();
    };
  }, [graphData, isEditMode, isPathMode, pathSource, pathTarget]);

  // Execute Calibrated Layout
  const runLayout = useCallback(() => {
    if (!cyRef.current) return;
    const cy = cyRef.current;

    let layoutOptions: any;
    if (layoutName === 'cose') {
      layoutOptions = {
        name: 'cose-bilkent',
        animate: true,
        animationDuration: 600,
        idealEdgeLength: 140,
        nodeRepulsion: 12000,
        nodeOverlap: 30,
        gravity: 0.25,
        numIter: 1500,
        padding: 40,
        stop: () => {
          cy.nodes().forEach((n) => {
            savedPositions.current[n.id()] = { ...n.position() };
          });
        },
      };
    } else {
      layoutOptions = {
        name: layoutName,
        animate: true,
        animationDuration: 500,
        padding: 40,
        stop: () => {
          cy.nodes().forEach((n) => {
            savedPositions.current[n.id()] = { ...n.position() };
          });
        },
      };
    }

    try {
      const layout = cy.layout(layoutOptions);
      layout.run();
    } catch {
      // Fallback to standard cose
      const fallback = cy.layout({ name: 'cose', animate: true, padding: 40 });
      fallback.run();
    }
  }, [layoutName]);

  // Focus Mode Logic: Outgoing (violet), Backlink (pink), Mutual (indigo), others dimmed to 35%
  useEffect(() => {
    if (!cyRef.current) return;
    const cy = cyRef.current;

    // Clear all focus / dimming classes
    cy.elements().removeClass(
      'focused-selected focused-outgoing focused-backlink focused-mutual focused-edge-outgoing focused-edge-backlink focused-edge-mutual dimmed'
    );

    if (!selectedNoteId) {
      return;
    }

    const selStr = `${selectedNoteId}`;
    const selectedNode = cy.$(`node[id = "${selStr}"]`);
    if (selectedNode.length === 0) return;

    selectedNode.addClass('focused-selected');

    const focusCollection = cy.collection().add(selectedNode);

    // Inspect edges connected to selectedNode
    const connectedEdges = selectedNode.connectedEdges();
    connectedEdges.forEach((edge) => {
      const isMutual = edge.data('mutual') === true || edge.data('direction') === 'mutual';
      const isOutgoing = edge.data('source') === selStr;
      const isBacklink = edge.data('target') === selStr;
      const otherId = edge.data('source') === selStr ? edge.data('target') : edge.data('source');
      const otherNode = cy.$(`node[id = "${otherId}"]`);

      if (isMutual) {
        edge.addClass('focused-edge-mutual');
        otherNode.addClass('focused-mutual');
      } else if (isOutgoing) {
        edge.addClass('focused-edge-outgoing');
        otherNode.addClass('focused-outgoing');
      } else if (isBacklink) {
        edge.addClass('focused-edge-backlink');
        otherNode.addClass('focused-backlink');
      }

      focusCollection.merge(edge);
      focusCollection.merge(otherNode);
    });

    // Dim everything else to 35% opacity so user keeps context
    cy.elements().difference(focusCollection).addClass('dimmed');

    // Only pan the view if the selected node is off-screen (no forced camera zoom)
    try {
      const extent = cy.extent();
      const pos = selectedNode.position();
      const margin = 45;
      const isOffscreen = (
        pos.x < extent.x1 + margin ||
        pos.x > extent.x2 - margin ||
        pos.y < extent.y1 + margin ||
        pos.y > extent.y2 - margin
      );

      if (isOffscreen) {
        cy.animate({
          center: { eles: selectedNode },
          duration: 180,
          easing: 'ease-in-out',
        });
      }
    } catch {
      // Ignored
    }
  }, [selectedNoteId, neighborhoodDepth]);

  // Highlight shortest path
  const highlightShortestPath = useCallback(
    async (src: number, tgt: number) => {
      if (!cyRef.current) return;
      const cy = cyRef.current;
      cy.elements().removeClass('path-highlighted dimmed');

      try {
        const res = await graphApi.getShortestPath(src, tgt);
        if (!res.found || res.path.length === 0) {
          showToast({ type: 'info', message: 'No directed path found between selected notes.' });
          return;
        }

        const pathNodeIds = res.path.map((id) => `${id}`);
        const pathEdges: string[] = [];
        for (let i = 0; i < pathNodeIds.length - 1; i++) {
          pathEdges.push(`e_${pathNodeIds[i]}_${pathNodeIds[i + 1]}`);
        }

        const pathElements = cy.collection();
        pathNodeIds.forEach((id) => {
          pathElements.merge(cy.$(`node[id = "${id}"]`));
        });
        pathEdges.forEach((id) => {
          pathElements.merge(cy.$(`edge[id = "${id}"]`));
        });

        cy.elements().difference(pathElements).addClass('dimmed');
        pathElements.addClass('path-highlighted');

        showToast({
          type: 'success',
          message: `Shortest Path (${res.length} hops): ${res.path_titles.join(' → ')}`,
        });
      } catch (err: any) {
        showToast({ type: 'error', message: err.message });
      }
    },
    [showToast]
  );

  const resetPathMode = () => {
    setIsPathMode(false);
    setPathSource(null);
    setPathTarget(null);
    if (cyRef.current) {
      cyRef.current.elements().removeClass('path-highlighted dimmed');
    }
  };

  const isEmptyGraph = !graphData || graphData.nodes.length === 0;

  return (
    <div style={{ flex: 1, position: 'relative', height: '100%', overflow: 'hidden', backgroundColor: 'var(--bg)' }}>
      {/* Cytoscape Container */}
      <div ref={containerRef} style={{ width: '100%', height: '100%', backgroundColor: '#FFFFFF' }} />

      {/* Empty State Clean Hint */}
      {isEmptyGraph && (
        <div
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            textAlign: 'center',
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius-lg)',
            padding: '32px 36px',
            boxShadow: 'var(--shadow-md)',
            zIndex: 20,
            maxWidth: '420px',
          }}
        >
          <div
            style={{
              width: '48px',
              height: '48px',
              borderRadius: '50%',
              backgroundColor: 'var(--accent-soft)',
              color: 'var(--primary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 14px',
            }}
          >
            <Layers size={24} />
          </div>
          <h3 style={{ fontSize: '16px', fontWeight: 700, color: 'var(--text)', marginBottom: '8px' }}>
            Your graph is empty
          </h3>
          <p style={{ fontSize: '13px', color: 'var(--muted)', lineHeight: 1.5, marginBottom: '18px' }}>
            Add notes or create links with <code style={{ backgroundColor: 'var(--accent-soft)', color: 'var(--primary-dark)', padding: '2px 5px', borderRadius: '4px' }}>[[Note Title]]</code> to see knowledge connections.
          </p>
          {onNewNote && (
            <button
              onClick={onNewNote}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                padding: '8px 16px',
                backgroundColor: 'var(--primary)',
                color: '#FFFFFF',
                border: '1px solid var(--primary-dark)',
                borderRadius: 'var(--radius-md)',
                fontWeight: 600,
                fontSize: '13px',
              }}
            >
              <Plus size={15} />
              <span>Create First Note</span>
            </button>
          )}
        </div>
      )}

      {/* Focus Mode Caption Bar */}
      {selectedNoteId && focusStats && (
        <div
          style={{
            position: 'absolute',
            top: '16px',
            left: '50%',
            transform: 'translateX(-50%)',
            backgroundColor: 'rgba(255, 255, 255, 0.96)',
            backdropFilter: 'blur(8px)',
            border: '1px solid var(--border)',
            borderRadius: '24px',
            padding: '6px 16px',
            display: 'flex',
            alignItems: 'center',
            gap: '14px',
            boxShadow: 'var(--shadow-md)',
            zIndex: 30,
            fontSize: '12px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'var(--outgoing)' }} />
            <span style={{ fontWeight: 600, color: 'var(--text)' }}>Outgoing: {focusStats.outgoing}</span>
          </div>
          <div style={{ width: '1px', height: '14px', backgroundColor: 'var(--border)' }} />
          <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'var(--backlink)' }} />
            <span style={{ fontWeight: 600, color: 'var(--text)' }}>Backlinks: {focusStats.backlinks}</span>
          </div>
          <div style={{ width: '1px', height: '14px', backgroundColor: 'var(--border)' }} />
          <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'var(--mutual)' }} />
            <span style={{ fontWeight: 600, color: 'var(--text)' }}>Mutual: {focusStats.mutual}</span>
          </div>

          {onClearSelection && (
            <button
              onClick={onClearSelection}
              title="Clear focus (Esc)"
              style={{
                marginLeft: '6px',
                padding: '2px 8px',
                borderRadius: '12px',
                backgroundColor: 'var(--surface)',
                border: '1px solid var(--border)',
                fontSize: '11px',
                color: 'var(--muted)',
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: '3px',
              }}
            >
              <span>Show all</span>
              <X size={11} />
            </button>
          )}
        </div>
      )}

      {/* Graph Control Bar (Top Left) */}
      <div
        style={{
          position: 'absolute',
          top: '16px',
          left: '16px',
          display: 'flex',
          gap: '8px',
          zIndex: 25,
        }}
      >
        {/* Layout Selector */}
        <div
          style={{
            backgroundColor: 'var(--bg)',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius-md)',
            padding: '3px 8px',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            boxShadow: 'var(--shadow-sm)',
          }}
        >
          <Layers size={13} color="var(--primary)" />
          <select
            value={layoutName}
            onChange={(e) => {
              setLayoutName(e.target.value as any);
              setTimeout(runLayout, 50);
            }}
            style={{
              border: 'none',
              background: 'transparent',
              fontSize: '12px',
              fontWeight: 600,
              color: 'var(--text)',
              outline: 'none',
              cursor: 'pointer',
            }}
          >
            <option value="cose">Force-Directed (CoSE)</option>
            <option value="concentric">Concentric</option>
            <option value="circle">Circle</option>
            <option value="breadthfirst">Hierarchical</option>
          </select>
        </div>

        {/* Neighborhood Depth Slider (1-3 hops) */}
        <div
          style={{
            backgroundColor: 'var(--bg)',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius-md)',
            padding: '3px 10px',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            boxShadow: 'var(--shadow-sm)',
            fontSize: '12px',
          }}
        >
          <Sliders size={13} color="var(--muted)" />
          <span style={{ fontWeight: 500, color: 'var(--muted)' }}>Depth:</span>
          <input
            type="range"
            min="1"
            max="3"
            value={neighborhoodDepth}
            onChange={(e) => onChangeDepth(parseInt(e.target.value, 10))}
            style={{ width: '50px', accentColor: 'var(--primary)' }}
          />
          <span style={{ fontWeight: 700, color: 'var(--primary-dark)', width: '10px' }}>{neighborhoodDepth}</span>
        </div>

        {/* Shortest Path Mode Toggle */}
        <button
          onClick={() => {
            if (isPathMode) {
              resetPathMode();
            } else {
              setIsPathMode(true);
              showToast({ type: 'info', message: 'Path Mode: Click source note, then click target note.' });
            }
          }}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '5px',
            padding: '0 10px',
            height: '32px',
            backgroundColor: isPathMode ? '#FFF1F2' : 'var(--bg)',
            color: isPathMode ? 'var(--danger)' : 'var(--text)',
            border: `1px solid ${isPathMode ? 'var(--danger)' : 'var(--border)'}`,
            borderRadius: 'var(--radius-md)',
            fontWeight: 600,
            fontSize: '12px',
            boxShadow: 'var(--shadow-sm)',
          }}
        >
          <Route size={13} />
          <span>{isPathMode ? 'Exit Path Mode' : 'Shortest Path'}</span>
        </button>
      </div>

      {/* Edit Mode Instructions Banner */}
      {isEditMode && (
        <div
          style={{
            position: 'absolute',
            top: '56px',
            left: '16px',
            backgroundColor: 'var(--accent-soft)',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius-md)',
            padding: '6px 12px',
            fontSize: '11px',
            color: 'var(--primary-dark)',
            fontWeight: 500,
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            zIndex: 25,
            boxShadow: 'var(--shadow-sm)',
          }}
        >
          <HelpCircle size={14} color="var(--primary)" />
          <span>
            {linkSourceNode
              ? `Source: '${linkSourceNode.label}'. Click target note to link.`
              : 'Edit Mode: Click a note to link, click an edge to remove, double-click canvas to create note.'}
          </span>
          {linkSourceNode && (
            <button
              onClick={() => setLinkSourceNode(null)}
              style={{
                marginLeft: '6px',
                padding: '2px 5px',
                backgroundColor: 'var(--bg)',
                border: '1px solid var(--border)',
                borderRadius: '3px',
                fontSize: '10px',
              }}
            >
              Cancel
            </button>
          )}
        </div>
      )}

      {/* Zoom / Viewport Buttons (Bottom Left) */}
      <div
        style={{
          position: 'absolute',
          bottom: showUnlinkedTray ? '80px' : '20px',
          left: '16px',
          display: 'flex',
          flexDirection: 'column',
          gap: '5px',
          zIndex: 25,
          transition: 'bottom 0.2s ease',
        }}
      >
        <button
          onClick={() => cyRef.current?.zoom(cyRef.current.zoom() * 1.25)}
          title="Zoom In"
          style={{
            width: '32px',
            height: '32px',
            backgroundColor: 'var(--bg)',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius-md)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: 'var(--shadow-sm)',
            color: 'var(--text)',
          }}
        >
          <ZoomIn size={15} />
        </button>
        <button
          onClick={() => cyRef.current?.zoom(cyRef.current.zoom() * 0.8)}
          title="Zoom Out"
          style={{
            width: '32px',
            height: '32px',
            backgroundColor: 'var(--bg)',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius-md)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: 'var(--shadow-sm)',
            color: 'var(--text)',
          }}
        >
          <ZoomOut size={15} />
        </button>
        <button
          onClick={() => cyRef.current?.fit(undefined, 40)}
          title="Fit View"
          style={{
            width: '32px',
            height: '32px',
            backgroundColor: 'var(--bg)',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius-md)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: 'var(--shadow-sm)',
            color: 'var(--text)',
          }}
        >
          <Maximize2 size={15} />
        </button>
      </div>

      {/* Collapsible Legend (Bottom Right) */}
      <div
        style={{
          position: 'absolute',
          bottom: showUnlinkedTray ? '80px' : '20px',
          right: '16px',
          zIndex: 25,
          transition: 'bottom 0.2s ease',
        }}
      >
        {showLegend ? (
          <div
            style={{
              backgroundColor: 'rgba(255, 255, 255, 0.96)',
              backdropFilter: 'blur(6px)',
              border: '1px solid var(--border)',
              borderRadius: 'var(--radius-md)',
              padding: '8px 12px',
              fontSize: '11px',
              display: 'flex',
              flexDirection: 'column',
              gap: '6px',
              boxShadow: 'var(--shadow-sm)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px' }}>
              <span style={{ fontWeight: 700, color: 'var(--muted)', textTransform: 'uppercase', fontSize: '10px' }}>
                Legend
              </span>
              <button
                onClick={() => setShowLegend(false)}
                style={{ background: 'none', border: 'none', padding: 0, color: 'var(--muted)', cursor: 'pointer' }}
                title="Collapse legend"
              >
                <ChevronDown size={13} />
              </button>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'var(--outgoing)' }} />
              <span>Outgoing (Violet)</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'var(--backlink)' }} />
              <span>Backlink (Pink)</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'var(--mutual)' }} />
              <span>Mutual (Indigo double-arrow)</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#E5484D' }} />
              <span>Shortest Path (Red)</span>
            </div>
          </div>
        ) : (
          <button
            onClick={() => setShowLegend(true)}
            style={{
              backgroundColor: 'var(--bg)',
              border: '1px solid var(--border)',
              borderRadius: 'var(--radius-md)',
              padding: '4px 8px',
              fontSize: '11px',
              fontWeight: 600,
              color: 'var(--muted)',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
              boxShadow: 'var(--shadow-sm)',
            }}
          >
            <span>Legend</span>
            <ChevronUp size={13} />
          </button>
        )}
      </div>

      {/* Unlinked Notes Tray Toggle & Container (Docked at Bottom) */}
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          backgroundColor: 'rgba(255, 255, 255, 0.98)',
          borderTop: '1px solid var(--border)',
          zIndex: 35,
          transition: 'all 0.2s ease',
        }}
      >
        {/* Toggle Bar */}
        <div
          onClick={() => setShowUnlinkedTray(!showUnlinkedTray)}
          style={{
            padding: '4px 16px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            cursor: 'pointer',
            backgroundColor: 'var(--surface)',
            borderBottom: showUnlinkedTray ? '1px solid var(--border)' : 'none',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '11px', fontWeight: 600, color: 'var(--muted)' }}>
            <span>Unlinked Notes ({unlinkedNodes.length})</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '11px', color: 'var(--primary)' }}>
            <span>{showUnlinkedTray ? 'Hide tray' : 'Show tray'}</span>
            {showUnlinkedTray ? <ChevronDown size={13} /> : <ChevronUp size={13} />}
          </div>
        </div>

        {/* Chips Tray */}
        {showUnlinkedTray && (
          <div
            style={{
              padding: '8px 16px',
              maxHeight: '120px',
              overflowY: 'auto',
              display: 'flex',
              flexWrap: 'wrap',
              gap: '6px',
              alignItems: 'center',
            }}
          >
            {unlinkedNodes.length === 0 ? (
              <span style={{ fontSize: '12px', color: 'var(--muted)', fontStyle: 'italic' }}>
                All notes are connected! No orphan notes in the graph.
              </span>
            ) : (
              unlinkedNodes.map((n) => (
                <button
                  key={n.id}
                  onClick={() => onSelectNote(parseInt(n.id, 10))}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px',
                    padding: '3px 8px',
                    backgroundColor: selectedNoteId === parseInt(n.id, 10) ? 'var(--accent-soft)' : 'var(--bg)',
                    border: `1px solid ${selectedNoteId === parseInt(n.id, 10) ? 'var(--primary)' : 'var(--border)'}`,
                    borderRadius: '12px',
                    fontSize: '11px',
                    fontWeight: 500,
                    color: 'var(--text)',
                    cursor: 'pointer',
                  }}
                >
                  <FileText size={11} color="var(--muted)" />
                  <span>{n.label}</span>
                </button>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
};
