/**
 * Card Component - Glassmorphism Style
 */

import { HTMLAttributes, ReactNode } from 'react';
import { clsx } from 'clsx';
import './Card.css';

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  hover?: boolean;
  glow?: boolean;
  padding?: 'sm' | 'md' | 'lg';
}

export function Card({
  children,
  hover = false,
  glow = false,
  padding = 'md',
  className,
  ...props
}: CardProps) {
  return (
    <div
      className={clsx(
        'card',
        `card-padding-${padding}`,
        hover && 'card-hover',
        glow && 'card-glow',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export interface CardHeaderProps {
  title: string;
  subtitle?: string;
  action?: ReactNode;
}

export function CardHeader({ title, subtitle, action }: CardHeaderProps) {
  return (
    <div className="card-header">
      <div className="card-header-text">
        <h3 className="card-title">{title}</h3>
        {subtitle && <p className="card-subtitle">{subtitle}</p>}
      </div>
      {action && <div className="card-header-action">{action}</div>}
    </div>
  );
}

export function CardBody({ children, className }: HTMLAttributes<HTMLDivElement>) {
  return <div className={clsx('card-body', className)}>{children}</div>;
}

export function CardFooter({ children, className }: HTMLAttributes<HTMLDivElement>) {
  return <div className={clsx('card-footer', className)}>{children}</div>;
}
