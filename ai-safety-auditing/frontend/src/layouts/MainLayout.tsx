/**
 * Main Layout Component
 */

import { Outlet } from 'react-router-dom';
import { Sidebar } from '@/components/Sidebar/Sidebar';
import './MainLayout.css';

export function MainLayout() {
  return (
    <div className="main-layout">
      <Sidebar />
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}
