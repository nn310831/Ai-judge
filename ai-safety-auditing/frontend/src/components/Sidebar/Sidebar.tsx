/**
 * Sidebar Component - System Navigation
 */

import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Shield, 
  Target, 
  Settings,
  Database
} from 'lucide-react';
import './Sidebar.css';

const navigation = [
  { name: 'Dashboard', path: '/', icon: LayoutDashboard },
  { name: 'Testing', path: '/testing', icon: Target },
  { name: 'Models', path: '/models', icon: Database },
  { name: 'Results', path: '/results', icon: Shield },
  { name: 'Settings', path: '/settings', icon: Settings },
];

export function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <Shield className="sidebar-logo-icon" size={32} />
          <div className="sidebar-logo-text">
            <h1 className="sidebar-logo-title">AI SAFETY</h1>
            <p className="sidebar-logo-subtitle">Auditing System</p>
          </div>
        </div>
      </div>

      <nav className="sidebar-nav">
        {navigation.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `sidebar-nav-item ${isActive ? 'sidebar-nav-item-active' : ''}`
            }
          >
            <item.icon size={20} className="sidebar-nav-icon" />
            <span className="sidebar-nav-label">{item.name}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-status">
          <div className="sidebar-status-dot" />
          <span className="sidebar-status-text">System Online</span>
        </div>
      </div>
    </aside>
  );
}
