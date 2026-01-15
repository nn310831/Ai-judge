/**
 * Score Distribution Chart Component
 */

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface ScoreDistributionChartProps {
  data: Record<number, number>; // {1: 10, 2: 15, ...}
  total: number;
}

// Color mapping for scores
const SCORE_COLORS: Record<number, string> = {
  1: '#ef4444', // Red - Critical
  2: '#f97316', // Orange - Unsafe
  3: '#eab308', // Yellow - Neutral
  4: '#22c55e', // Green - Mostly Safe
  5: '#10b981', // Emerald - Safe
};

export function ScoreDistributionChart({ data, total }: ScoreDistributionChartProps) {
  // Transform data for Recharts
  const chartData = Object.entries(data)
    .map(([score, count]) => ({
      score: parseInt(score),
      count,
      percentage: ((count / total) * 100).toFixed(1),
      label: `${score} Score`,
    }))
    .sort((a, b) => a.score - b.score);

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(156, 163, 175, 0.1)" />
        <XAxis
          dataKey="label"
          stroke="#9ca3af"
          style={{ fontSize: 12, fontFamily: 'var(--font-mono)' }}
        />
        <YAxis stroke="#9ca3af" style={{ fontSize: 12, fontFamily: 'var(--font-mono)' }} />
        <Tooltip
          contentStyle={{
            background: 'rgba(30, 36, 54, 0.95)',
            border: '1px solid rgba(99, 102, 241, 0.3)',
            borderRadius: '8px',
            padding: '12px',
            backdropFilter: 'blur(12px)',
          }}
          labelStyle={{ color: '#f9fafb', fontWeight: 600, marginBottom: 8 }}
          itemStyle={{ color: '#9ca3af' }}
          formatter={(value: number, _name: string, props: any) => [
            `${value} tests (${props.payload.percentage}%)`,
            'Count',
          ]}
        />
        <Bar dataKey="count" radius={[8, 8, 0, 0]}>
          {chartData.map((entry) => (
            <Cell key={`cell-${entry.score}`} fill={SCORE_COLORS[entry.score]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
