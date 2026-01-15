/**
 * Button Component - System Style
 */

import { ButtonHTMLAttributes, ReactNode } from 'react';
import { clsx } from 'clsx';
import './Button.css';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  icon?: ReactNode;
  fullWidth?: boolean;
}

export function Button({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  icon,
  fullWidth = false,
  className,
  disabled,
  ...props
}: ButtonProps) {
  return (
    <button
      className={clsx(
        'btn',
        `btn-${variant}`,
        `btn-${size}`,
        fullWidth && 'btn-full-width',
        loading && 'btn-loading',
        className
      )}
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <svg className="btn-spinner" viewBox="0 0 24 24">
          <circle
            className="btn-spinner-circle"
            cx="12"
            cy="12"
            r="10"
            fill="none"
            strokeWidth="3"
          />
        </svg>
      )}
      {!loading && icon && <span className="btn-icon">{icon}</span>}
      {children}
    </button>
  );
}
