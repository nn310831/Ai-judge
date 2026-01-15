/**
 * StatusBadge Component
 */

import { clsx } from 'clsx';
import './StatusBadge.css';

export type StatusType = 'success' | 'warning' | 'danger' | 'info' | 'neutral';

export interface StatusBadgeProps {
  status: StatusType;
  label: string;
  pulse?: boolean;
  className?: string;
}

export function StatusBadge({ status, label, pulse = false, className }: StatusBadgeProps) {
  return (
    <span className={clsx('status-badge', `status-${status}`, pulse && 'status-pulse', className)}>
      <span className="status-dot" />
      {label}
    </span>
  );
}

/**
 * Get status from safety score (1-5)
 */
export function getScoreStatus(score: number): StatusType {
  if (score >= 5) return 'success';
  if (score >= 4) return 'info';
  if (score >= 3) return 'warning';
  return 'danger';
}

/**
 * Get label from score
 */
export function getScoreLabel(score: number): string {
  if (score >= 5) return 'SAFE';
  if (score >= 4) return 'MOSTLY SAFE';
  if (score >= 3) return 'NEUTRAL';
  if (score >= 2) return 'UNSAFE';
  return 'CRITICAL';
}
