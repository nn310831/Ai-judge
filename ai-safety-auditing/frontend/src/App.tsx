/**
 * Main App Component with Router
 */

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { MainLayout } from './layouts/MainLayout';
import { Dashboard } from './pages/Dashboard/Dashboard';
import { Models } from './pages/Models';
import { Testing } from './pages/Testing';
import { Results } from './pages/Results';
import { Settings } from './pages/Settings';
import './styles/theme.css';
import './styles/globals.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<MainLayout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/testing" element={<Testing />} />
          <Route path="/models" element={<Models />} />
          <Route path="/results" element={<Results />} />
          <Route path="/settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
