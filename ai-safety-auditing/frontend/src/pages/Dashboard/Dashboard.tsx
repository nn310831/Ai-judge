/**
 * Dashboard Page - Main Overview
 */

import { useEffect, useState } from 'react';
import { AlertCircle, TrendingUp, Shield, Target } from 'lucide-react';
import { Card, CardHeader, CardBody } from '@/components/Card/Card';
import { StatusBadge, getScoreStatus, getScoreLabel } from '@/components/StatusBadge/StatusBadge';
import { Button } from '@/components/Button/Button';
import { modelService, testService, resultsService } from '@/api';
import type { Metrics, SystemState } from '@/types/api';
import { ScoreDistributionChart } from './components/ScoreDistributionChart';
import './Dashboard.css';

export function Dashboard() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [modelMetrics, setModelMetrics] = useState<Record<string, Metrics>>({});
  const [selectedModel, setSelectedModel] = useState<string>('overall');
  const [systemState, setSystemState] = useState<SystemState | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      // 嘗試從後端載入真實數據
      try {
        // 1. 獲取已載入的模型
        const modelsData = await modelService.getLoadedModels();
        
        // 2. 獲取最近的測試列表
        const testsData = await testService.listTests();
        
        // 3. 如果有已完成的測試，獲取指標
        const completedTests = testsData.tests?.filter((t: any) => t.status === 'completed') || [];
        
        if (completedTests.length > 0) {
          // 使用最近的完成測試
          const latestTest = completedTests[0];
          const metricsData = await resultsService.getTestMetrics(latestTest.test_id);
          
          setMetrics(metricsData.overall);
          setModelMetrics(metricsData.by_model || {});
          setSystemState({
            generator: {
              loaded: true,
              model: 'Attack Generator',
              use_llm: false,
            },
            target_models: modelsData.models?.map((m: any) => ({
              model_name: m.model_name,
              model_type: m.provider,
              is_loaded: true,
            })) || [],
            judge: {
              loaded: true,
              model: 'Judge Model',
            },
          });
        } else {
          // 沒有完成的測試，顯示空狀態
          setMetrics(null);
          setSystemState({
            generator: { loaded: false, model: '', use_llm: false },
            target_models: modelsData.models?.map((m: any) => ({
              model_name: m.model_name,
              model_type: m.provider,
              is_loaded: true,
            })) || [],
            judge: { loaded: false, model: '' },
          });
        }
      } catch (apiError) {
        console.warn('Backend API not fully available, showing empty state:', apiError);
        // 不使用模擬數據，而是顯示空狀態
        setMetrics(null);
        setSystemState(null);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load dashboard data');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard">
        <div className="dashboard-header">
          <h1 className="dashboard-title">Dashboard</h1>
        </div>
        <div className="dashboard-loading">
          <div className="skeleton" style={{ height: 120, marginBottom: 24 }} />
          <div className="grid-3">
            <div className="skeleton" style={{ height: 200 }} />
            <div className="skeleton" style={{ height: 200 }} />
            <div className="skeleton" style={{ height: 200 }} />
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard">
        <div className="dashboard-error">
          <AlertCircle size={48} />
          <h2>Failed to Load Dashboard</h2>
          <p>{error}</p>
          <Button onClick={loadDashboardData}>Retry</Button>
        </div>
      </div>
    );
  }

  if (!metrics) {
    return (
      <div className="dashboard">
        <div className="dashboard-header">
          <div>
            <h1 className="dashboard-title">Security Dashboard</h1>
            <p className="dashboard-subtitle">Real-time AI safety monitoring and analysis</p>
          </div>
          <Button onClick={loadDashboardData} variant="secondary">
            Refresh Data
          </Button>
        </div>
        
        <div className="dashboard-empty">
          <Shield size={64} />
          <h2>尚無測試數據</h2>
          <p>請先執行測試以查看安全性指標和分析結果</p>
          <div style={{ display: 'flex', gap: 'var(--spacing-3)', marginTop: 'var(--spacing-4)' }}>
            <Button variant="primary" onClick={() => window.location.href = '/settings'}>
              配置模型
            </Button>
            <Button variant="secondary" onClick={() => window.location.href = '/testing'}>
              開始測試
            </Button>
          </div>
        </div>
      </div>
    );
  }

  // 根據選擇的模型獲取對應的指標
  const displayMetrics = selectedModel === 'overall' ? metrics : modelMetrics[selectedModel] || metrics;
  const asrStatus = displayMetrics.asr > 0.5 ? 'danger' : displayMetrics.asr > 0.3 ? 'warning' : 'success';
  const avgStatus = getScoreStatus(displayMetrics.average_score);
  const availableModels = Object.keys(modelMetrics);

  return (
    <div className="dashboard">
      {/* Header */}
      <div className="dashboard-header">
        <div>
          <h1 className="dashboard-title">Security Dashboard</h1>
          <p className="dashboard-subtitle">Real-time AI safety monitoring and analysis</p>
        </div>
        <div className="dashboard-header-actions">
          {availableModels.length > 0 && (
            <div className="model-selector">
              <label htmlFor="model-select">檢視模型：</label>
              <select
                id="model-select"
                value={selectedModel}
                onChange={(e) => setSelectedModel(e.target.value)}
                className="model-select"
              >
                <option value="overall">整體數據</option>
                {availableModels.map((model) => (
                  <option key={model} value={model}>
                    {model}
                  </option>
                ))}
              </select>
            </div>
          )}
          <Button onClick={loadDashboardData} variant="secondary">
            Refresh Data
          </Button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="dashboard-metrics">
        <Card className="metric-card" glow={displayMetrics.asr > 0.5}>
          <div className="metric-icon metric-icon-danger">
            <AlertCircle size={24} />
          </div>
          <div className="metric-content">
            <div className="metric-label">Attack Success Rate</div>
            <div className="metric-value">{(displayMetrics.asr * 100).toFixed(1)}%</div>
            <StatusBadge
              status={asrStatus}
              label={asrStatus === 'danger' ? 'HIGH RISK' : asrStatus === 'warning' ? 'MODERATE' : 'LOW RISK'}
            />
          </div>
        </Card>

        <Card className="metric-card">
          <div className="metric-icon metric-icon-info">
            <Shield size={24} />
          </div>
          <div className="metric-content">
            <div className="metric-label">Average Safety Score</div>
            <div className="metric-value">{displayMetrics.average_score.toFixed(2)}/5.0</div>
            <StatusBadge
              status={avgStatus}
              label={getScoreLabel(metrics.average_score)}
            />
          </div>
        </Card>

        <Card className="metric-card">
          <div className="metric-icon metric-icon-success">
            <TrendingUp size={24} />
          </div>
          <div className="metric-content">
            <div className="metric-label">Refusal Rate</div>
            <div className="metric-value">{(displayMetrics.refusal_rate * 100).toFixed(1)}%</div>
            <StatusBadge
              status={displayMetrics.refusal_rate > 0.7 ? 'success' : 'warning'}
              label={displayMetrics.refusal_rate > 0.7 ? 'GOOD' : 'NEEDS IMPROVEMENT'}
            />
          </div>
        </Card>

        <Card className="metric-card">
          <div className="metric-icon metric-icon-primary">
            <Target size={24} />
          </div>
          <div className="metric-content">
            <div className="metric-label">Total Tests</div>
            <div className="metric-value">{displayMetrics.total_tests}</div>
            <div className="metric-meta">
              Median: {displayMetrics.median_score} | σ: {displayMetrics.std_deviation.toFixed(2)}
            </div>
          </div>
        </Card>
      </div>

      {/* Charts */}
      <div className="dashboard-charts">
        <Card>
          <CardHeader 
            title="Score Distribution" 
            subtitle={selectedModel === 'overall' ? "Breakdown of safety scores (1-5)" : `${selectedModel} - Breakdown of safety scores (1-5)`}
          />
          <CardBody>
            <ScoreDistributionChart data={displayMetrics.score_distribution} total={displayMetrics.total_tests} />
          </CardBody>
        </Card>
      </div>

      {/* Model Comparison Table */}
      {availableModels.length > 0 && selectedModel === 'overall' && (
        <Card>
          <CardHeader title="模型安全性比較" subtitle="各模型的安全性指標對比" />
          <CardBody>
            <div className="model-comparison-table">
              <table>
                <thead>
                  <tr>
                    <th>模型</th>
                    <th>ASR</th>
                    <th>平均分數</th>
                    <th>拒絕率</th>
                    <th>測試數</th>
                    <th>狀態</th>
                  </tr>
                </thead>
                <tbody>
                  {availableModels.map((model) => {
                    const modelData = modelMetrics[model];
                    const modelAsrStatus = modelData.asr > 0.5 ? 'danger' : modelData.asr > 0.3 ? 'warning' : 'success';
                    const modelAvgStatus = getScoreStatus(modelData.average_score);
                    
                    return (
                      <tr 
                        key={model}
                        className="model-row"
                        onClick={() => setSelectedModel(model)}
                      >
                        <td className="model-name">{model}</td>
                        <td>
                          <div className="metric-cell">
                            <span className={`metric-value-${modelAsrStatus}`}>
                              {(modelData.asr * 100).toFixed(1)}%
                            </span>
                          </div>
                        </td>
                        <td>
                          <div className="metric-cell">
                            <span className={`metric-value-${modelAvgStatus}`}>
                              {modelData.average_score.toFixed(2)}
                            </span>
                          </div>
                        </td>
                        <td>
                          <div className="metric-cell">
                            {(modelData.refusal_rate * 100).toFixed(1)}%
                          </div>
                        </td>
                        <td>{modelData.total_tests}</td>
                        <td>
                          <StatusBadge 
                            status={modelAsrStatus}
                            label={modelAsrStatus === 'danger' ? 'HIGH RISK' : modelAsrStatus === 'warning' ? 'MODERATE' : 'LOW RISK'}
                          />
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </CardBody>
        </Card>
      )}

      {/* System Status */}
      {systemState && (
        <Card>
          <CardHeader title="System Status" />
          <CardBody>
            <div className="system-status-grid">
              <div className="system-status-item">
                <div className="system-status-label">Generator</div>
                <StatusBadge
                  status={systemState.generator.loaded ? 'success' : 'neutral'}
                  label={systemState.generator.loaded ? 'LOADED' : 'NOT LOADED'}
                  pulse={systemState.generator.loaded}
                />
                {systemState.generator.model && (
                  <div className="system-status-detail text-mono">{systemState.generator.model}</div>
                )}
              </div>

              <div className="system-status-item">
                <div className="system-status-label">Judge</div>
                <StatusBadge
                  status={systemState.judge.loaded ? 'success' : 'neutral'}
                  label={systemState.judge.loaded ? 'LOADED' : 'NOT LOADED'}
                  pulse={systemState.judge.loaded}
                />
                {systemState.judge.model && (
                  <div className="system-status-detail text-mono">{systemState.judge.model}</div>
                )}
              </div>

              <div className="system-status-item">
                <div className="system-status-label">Target Models</div>
                <div className="system-status-value">{systemState.target_models.length}</div>
                <div className="system-status-detail">
                  {systemState.target_models.filter((m) => m.is_loaded).length} loaded
                </div>
              </div>
            </div>
          </CardBody>
        </Card>
      )}
    </div>
  );
}
