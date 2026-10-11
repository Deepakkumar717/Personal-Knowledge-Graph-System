import React from 'react';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend,
} from 'recharts';
import {
  X,
  BarChart2,
  PieChart as PieIcon,
  TrendingUp,
  Share2,
  RefreshCw,
  Info,
  GitCommit,
  Layers,
} from 'lucide-react';
import { GraphInsightsResponse } from '../api';

interface InsightsPanelProps {
  isOpen: boolean;
  onClose: () => void;
  insights: GraphInsightsResponse | null;
  loading: boolean;
  onRefresh: () => void;
  onSelectTag: (tag: string) => void;
  onSelectGroup?: (group: string) => void;
}

const VIOLET_PALETTE = ['#7C3AED', '#8B5CF6', '#A78BFA', '#C4B5FD', '#6D28D9', '#4C1D95', '#DDD6FE'];

export const InsightsPanel: React.FC<InsightsPanelProps> = ({
  isOpen,
  onClose,
  insights,
  loading,
  onRefresh,
  onSelectTag,
  onSelectGroup,
}) => {
  if (!isOpen) return null;

  const connectedCount = insights?.connected_vs_orphans?.connected ?? 0;
  const orphansCount = insights?.connected_vs_orphans?.orphans ?? 0;
  const totalNotes = connectedCount + orphansCount;

  const connectedVsOrphansData = [
    { name: 'Connected', value: connectedCount, color: '#7C3AED' },
    { name: 'Orphans', value: orphansCount, color: '#DDD6FE' },
  ].filter((d) => d.value > 0);

  const notesByGroupData = (insights?.notes_by_group ?? []).filter((g) => g.count > 0);
  const notesByTagData = insights?.notes_by_tag ?? [];
  const topConnectedData = insights?.top_connected ?? [];
  const notesPerDayData = insights?.notes_per_day ?? [];

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(15, 23, 42, 0.55)',
        backdropFilter: 'blur(3px)',
        zIndex: 200,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '20px',
      }}
      onClick={onClose}
    >
      <div
        style={{
          width: '100%',
          maxWidth: '1100px',
          maxHeight: '90vh',
          backgroundColor: '#FFFFFF',
          borderRadius: '16px',
          boxShadow: '0 25px 50px -12px rgba(124, 58, 237, 0.25)',
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
          border: '1px solid #E9D5FF',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '18px 24px',
            borderBottom: '1px solid #F3E8FF',
            backgroundColor: '#FAF5FF',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div
              style={{
                width: '36px',
                height: '36px',
                borderRadius: '10px',
                backgroundColor: '#7C3AED',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#FFFFFF',
              }}
            >
              <BarChart2 size={20} />
            </div>
            <div>
              <h2 style={{ margin: 0, fontSize: '18px', fontWeight: 700, color: '#4C1D95' }}>
                Knowledge Graph Insights & Analytics
              </h2>
              <p style={{ margin: 0, fontSize: '12px', color: '#6D28D9' }}>
                Live network metrics, activity trends, and connectivity distribution
              </p>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <button
              onClick={onRefresh}
              title="Refresh Insights"
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                padding: '7px 12px',
                backgroundColor: '#FFFFFF',
                border: '1px solid #D8B4FE',
                borderRadius: '8px',
                color: '#7C3AED',
                fontSize: '13px',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
              <span>Refresh</span>
            </button>
            <button
              onClick={onClose}
              style={{
                background: 'none',
                border: 'none',
                color: '#6B7280',
                cursor: 'pointer',
                padding: '6px',
                borderRadius: '8px',
              }}
            >
              <X size={20} />
            </button>
          </div>
        </div>

        {/* Top Summary Bar */}
        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '12px',
            padding: '14px 24px',
            backgroundColor: '#FFFFFF',
            borderBottom: '1px solid #F3E8FF',
          }}
        >
          <div
            style={{
              flex: '1 1 180px',
              padding: '10px 14px',
              backgroundColor: '#FAF5FF',
              borderRadius: '10px',
              border: '1px solid #E9D5FF',
            }}
          >
            <div style={{ fontSize: '11px', color: '#6D28D9', fontWeight: 600, textTransform: 'uppercase' }}>
              Total Notes
            </div>
            <div style={{ fontSize: '20px', fontWeight: 700, color: '#4C1D95', marginTop: '2px' }}>
              {totalNotes}
            </div>
          </div>

          <div
            style={{
              flex: '1 1 180px',
              padding: '10px 14px',
              backgroundColor: '#FAF5FF',
              borderRadius: '10px',
              border: '1px solid #E9D5FF',
            }}
          >
            <div style={{ fontSize: '11px', color: '#6D28D9', fontWeight: 600, textTransform: 'uppercase' }}>
              Connected Notes
            </div>
            <div style={{ fontSize: '20px', fontWeight: 700, color: '#7C3AED', marginTop: '2px' }}>
              {connectedCount}{' '}
              <span style={{ fontSize: '12px', fontWeight: 500, color: '#6B7280' }}>
                ({totalNotes > 0 ? Math.round((connectedCount / totalNotes) * 100) : 0}%)
              </span>
            </div>
          </div>

          <div
            style={{
              flex: '1 1 180px',
              padding: '10px 14px',
              backgroundColor: '#FAF5FF',
              borderRadius: '10px',
              border: '1px solid #E9D5FF',
            }}
          >
            <div style={{ fontSize: '11px', color: '#6D28D9', fontWeight: 600, textTransform: 'uppercase' }}>
              Orphan Notes
            </div>
            <div
              style={{
                fontSize: '20px',
                fontWeight: 700,
                color: orphansCount > 0 ? '#DC2626' : '#059669',
                marginTop: '2px',
              }}
            >
              {orphansCount}{' '}
              <span style={{ fontSize: '12px', fontWeight: 500, color: '#6B7280' }}>
                ({totalNotes > 0 ? Math.round((orphansCount / totalNotes) * 100) : 0}%)
              </span>
            </div>
          </div>

          <div
            style={{
              flex: '2 1 260px',
              padding: '10px 14px',
              backgroundColor: '#FAF5FF',
              borderRadius: '10px',
              border: '1px solid #E9D5FF',
            }}
          >
            <div style={{ fontSize: '11px', color: '#6D28D9', fontWeight: 600, textTransform: 'uppercase' }}>
              Link Types Breakdown
            </div>
            <div style={{ display: 'flex', gap: '14px', marginTop: '4px', fontSize: '13px', fontWeight: 600 }}>
              <span style={{ color: '#7C3AED' }}>
                Auto: <strong>{insights?.link_types?.auto ?? 0}</strong>
              </span>
              <span style={{ color: '#4C1D95' }}>
                Manual: <strong>{insights?.link_types?.manual ?? 0}</strong>
              </span>
              <span style={{ color: '#9333EA' }}>
                Mutual: <strong>{insights?.link_types?.mutual ?? 0}</strong>
              </span>
            </div>
          </div>
        </div>

        {/* Scrollable Content Body */}
        <div
          style={{
            flex: 1,
            overflowY: 'auto',
            padding: '24px',
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(460px, 1fr))',
            gap: '20px',
            backgroundColor: '#FBFBFE',
          }}
        >
          {loading && !insights ? (
            // Loading Skeletons
            [1, 2, 3, 4, 5].map((i) => (
              <div
                key={i}
                style={{
                  height: '280px',
                  backgroundColor: '#FFFFFF',
                  borderRadius: '12px',
                  border: '1px solid #F3E8FF',
                  padding: '18px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '12px',
                  animation: 'pulse 1.5s infinite',
                }}
              >
                <div style={{ width: '40%', height: '18px', backgroundColor: '#EDE9FE', borderRadius: '4px' }} />
                <div style={{ width: '100%', flex: 1, backgroundColor: '#FAF5FF', borderRadius: '8px' }} />
              </div>
            ))
          ) : (
            <>
              {/* Chart 1: Notes by Tag (Vertical Bar Chart) */}
              <div
                style={{
                  backgroundColor: '#FFFFFF',
                  borderRadius: '12px',
                  border: '1px solid #E9D5FF',
                  padding: '18px',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
                  display: 'flex',
                  flexDirection: 'column',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <BarChart2 size={16} color="#7C3AED" />
                    <span style={{ fontSize: '14px', fontWeight: 700, color: '#374151' }}>
                      Notes by Tag (Top 10)
                    </span>
                  </div>
                  <span style={{ fontSize: '11px', color: '#6B7280' }}>Click bar to filter list</span>
                </div>

                {notesByTagData.length === 0 ? (
                  <div
                    style={{
                      flex: 1,
                      minHeight: '220px',
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      justifyContent: 'center',
                      backgroundColor: '#FAF5FF',
                      borderRadius: '8px',
                      padding: '20px',
                      textAlign: 'center',
                    }}
                  >
                    <Info size={24} color="#A78BFA" style={{ marginBottom: '8px' }} />
                    <div style={{ fontSize: '13px', fontWeight: 600, color: '#4C1D95' }}>No tagged notes yet</div>
                    <div style={{ fontSize: '12px', color: '#6D28D9', marginTop: '4px', maxWidth: '300px' }}>
                      Add tags to notes (e.g. #python, #project) to view tag distribution here.
                    </div>
                  </div>
                ) : (
                  <div style={{ height: '230px', width: '100%' }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={notesByTagData} margin={{ top: 10, right: 10, left: -20, bottom: 25 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#F3E8FF" />
                        <XAxis
                          dataKey="tag"
                          tick={{ fill: '#4B5563', fontSize: 11 }}
                          angle={-25}
                          textAnchor="end"
                          interval={0}
                        />
                        <YAxis allowDecimals={false} tick={{ fill: '#4B5563', fontSize: 11 }} />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: '#FFFFFF',
                            border: '1px solid #DDD6FE',
                            borderRadius: '8px',
                            boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)',
                            fontSize: '12px',
                          }}
                        />
                        <Bar
                          dataKey="count"
                          fill="#8B5CF6"
                          radius={[4, 4, 0, 0]}
                          cursor="pointer"
                          onClick={(entry: any) => {
                            if (entry && entry.tag) {
                              onSelectTag(entry.tag);
                              onClose();
                            }
                          }}
                        />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                )}
              </div>

              {/* Chart 2: Notes by Group (Donut Chart) */}
              <div
                style={{
                  backgroundColor: '#FFFFFF',
                  borderRadius: '12px',
                  border: '1px solid #E9D5FF',
                  padding: '18px',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
                  display: 'flex',
                  flexDirection: 'column',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <PieIcon size={16} color="#7C3AED" />
                    <span style={{ fontSize: '14px', fontWeight: 700, color: '#374151' }}>
                      Notes by Group (Donut)
                    </span>
                  </div>
                  <span style={{ fontSize: '11px', color: '#6B7280' }}>Click slice to filter</span>
                </div>

                {notesByGroupData.length === 0 ? (
                  <div
                    style={{
                      flex: 1,
                      minHeight: '220px',
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      justifyContent: 'center',
                      backgroundColor: '#FAF5FF',
                      borderRadius: '8px',
                      padding: '20px',
                      textAlign: 'center',
                    }}
                  >
                    <Layers size={24} color="#A78BFA" style={{ marginBottom: '8px' }} />
                    <div style={{ fontSize: '13px', fontWeight: 600, color: '#4C1D95' }}>No grouped notes yet</div>
                    <div style={{ fontSize: '12px', color: '#6D28D9', marginTop: '4px', maxWidth: '300px' }}>
                      Assign notes to topics or groups to visualize categorical clusters here.
                    </div>
                  </div>
                ) : (
                  <div style={{ height: '230px', width: '100%' }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={notesByGroupData}
                          dataKey="count"
                          nameKey="group"
                          cx="50%"
                          cy="50%"
                          innerRadius={55}
                          outerRadius={85}
                          paddingAngle={3}
                          cursor="pointer"
                          onClick={(entry: any) => {
                            if (entry && entry.group) {
                              if (onSelectGroup) onSelectGroup(entry.group);
                              else onSelectTag(entry.group);
                              onClose();
                            }
                          }}
                        >
                          {notesByGroupData.map((_, index) => (
                            <Cell key={`cell-group-${index}`} fill={VIOLET_PALETTE[index % VIOLET_PALETTE.length]} />
                          ))}
                        </Pie>
                        <Tooltip
                          contentStyle={{
                            backgroundColor: '#FFFFFF',
                            border: '1px solid #DDD6FE',
                            borderRadius: '8px',
                            fontSize: '12px',
                          }}
                        />
                        <Legend wrapperStyle={{ fontSize: '11px', color: '#4B5563' }} />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                )}
              </div>

              {/* Chart 3: Notes per Day (Line Chart - Last 30 Days) */}
              <div
                style={{
                  backgroundColor: '#FFFFFF',
                  borderRadius: '12px',
                  border: '1px solid #E9D5FF',
                  padding: '18px',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
                  display: 'flex',
                  flexDirection: 'column',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <TrendingUp size={16} color="#7C3AED" />
                    <span style={{ fontSize: '14px', fontWeight: 700, color: '#374151' }}>
                      Notes Created Per Day (Last 30 Days UTC)
                    </span>
                  </div>
                </div>

                <div style={{ height: '230px', width: '100%' }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={notesPerDayData} margin={{ top: 10, right: 15, left: -20, bottom: 25 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#F3E8FF" />
                      <XAxis
                        dataKey="date"
                        tick={{ fill: '#4B5563', fontSize: 10 }}
                        tickFormatter={(v) => (typeof v === 'string' && v.length >= 10 ? v.slice(5) : v)}
                        angle={-30}
                        textAnchor="end"
                        interval={3}
                      />
                      <YAxis allowDecimals={false} tick={{ fill: '#4B5563', fontSize: 11 }} />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: '#FFFFFF',
                          border: '1px solid #DDD6FE',
                          borderRadius: '8px',
                          fontSize: '12px',
                        }}
                      />
                      <Line
                        type="monotone"
                        dataKey="count"
                        stroke="#7C3AED"
                        strokeWidth={2.5}
                        dot={{ fill: '#8B5CF6', r: 3 }}
                        activeDot={{ r: 5, fill: '#6D28D9' }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Chart 4: Top Connected Notes (Horizontal Bar Chart) */}
              <div
                style={{
                  backgroundColor: '#FFFFFF',
                  borderRadius: '12px',
                  border: '1px solid #E9D5FF',
                  padding: '18px',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
                  display: 'flex',
                  flexDirection: 'column',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <GitCommit size={16} color="#7C3AED" />
                    <span style={{ fontSize: '14px', fontWeight: 700, color: '#374151' }}>
                      Top Connected Notes (Top 5 Hubs)
                    </span>
                  </div>
                </div>

                {topConnectedData.length === 0 || topConnectedData.every((n) => n.degree === 0) ? (
                  <div
                    style={{
                      flex: 1,
                      minHeight: '220px',
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      justifyContent: 'center',
                      backgroundColor: '#FAF5FF',
                      borderRadius: '8px',
                      padding: '20px',
                      textAlign: 'center',
                    }}
                  >
                    <Share2 size={24} color="#A78BFA" style={{ marginBottom: '8px' }} />
                    <div style={{ fontSize: '13px', fontWeight: 600, color: '#4C1D95' }}>No connected hubs yet</div>
                    <div style={{ fontSize: '12px', color: '#6D28D9', marginTop: '4px', maxWidth: '300px' }}>
                      Link notes via [[wikilinks]] or manual links to discover network hubs.
                    </div>
                  </div>
                ) : (
                  <div style={{ height: '230px', width: '100%' }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart
                        layout="vertical"
                        data={topConnectedData}
                        margin={{ top: 10, right: 20, left: 10, bottom: 5 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" stroke="#F3E8FF" />
                        <XAxis type="number" allowDecimals={false} tick={{ fill: '#4B5563', fontSize: 11 }} />
                        <YAxis
                          type="category"
                          dataKey="title"
                          width={110}
                          tick={{ fill: '#4B5563', fontSize: 11 }}
                          tickFormatter={(t) => (t.length > 14 ? t.slice(0, 12) + '...' : t)}
                        />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: '#FFFFFF',
                            border: '1px solid #DDD6FE',
                            borderRadius: '8px',
                            fontSize: '12px',
                          }}
                        />
                        <Bar dataKey="degree" fill="#6D28D9" radius={[0, 4, 4, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                )}
              </div>

              {/* Chart 5: Connected vs Orphans (Donut Chart) */}
              <div
                style={{
                  gridColumn: '1 / -1',
                  backgroundColor: '#FFFFFF',
                  borderRadius: '12px',
                  border: '1px solid #E9D5FF',
                  padding: '18px',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
                  display: 'flex',
                  flexDirection: 'column',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <Share2 size={16} color="#7C3AED" />
                    <span style={{ fontSize: '14px', fontWeight: 700, color: '#374151' }}>
                      Connected vs. Orphan Notes
                    </span>
                  </div>
                </div>

                {totalNotes === 0 ? (
                  <div
                    style={{
                      minHeight: '200px',
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      justifyContent: 'center',
                      backgroundColor: '#FAF5FF',
                      borderRadius: '8px',
                      padding: '20px',
                      textAlign: 'center',
                    }}
                  >
                    <Info size={24} color="#A78BFA" style={{ marginBottom: '8px' }} />
                    <div style={{ fontSize: '13px', fontWeight: 600, color: '#4C1D95' }}>Database is empty</div>
                    <div style={{ fontSize: '12px', color: '#6D28D9', marginTop: '4px' }}>
                      Create notes to evaluate connectivity and orphan ratios.
                    </div>
                  </div>
                ) : (
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '220px' }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={connectedVsOrphansData}
                          dataKey="value"
                          nameKey="name"
                          cx="50%"
                          cy="50%"
                          innerRadius={55}
                          outerRadius={85}
                          paddingAngle={4}
                        >
                          {connectedVsOrphansData.map((entry, index) => (
                            <Cell key={`cell-cov-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip
                          contentStyle={{
                            backgroundColor: '#FFFFFF',
                            border: '1px solid #DDD6FE',
                            borderRadius: '8px',
                            fontSize: '12px',
                          }}
                        />
                        <Legend wrapperStyle={{ fontSize: '12px', color: '#4B5563' }} />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};
