/**
 * Settings Page - AI System Control Panel
 * 
 * High-tech configuration interface for AI model infrastructure
 * Architecture: Flat config structure (provider, model_name, api_key, temperature, max_tokens)
 */

import React, { useState, useEffect } from 'react';
import {
  Settings as SettingsIcon,
  Save,
  RefreshCw,
  Plus,
  Trash2,
  Upload,
  FileText,
  AlertCircle,
  CheckCircle,
  Cpu,
  Zap,
  Activity,
  Shield,
  Sliders,
} from 'lucide-react';
import { configService } from '@/api';
import { Card } from '@/components/Card/Card';
import { Button } from '@/components/Button/Button';
import { StatusBadge } from '@/components/StatusBadge/StatusBadge';
import type { ModelConfig } from '@/api/config';
import './Settings.css';

const DEFAULT_MODEL: ModelConfig = {
  provider: 'openai',
  model_name: '',
  api_key: '',
  temperature: 0.7,
  max_tokens: 1000,
};

export const Settings: React.FC = () => {
  const [config, setConfig] = useState<ModelConfig[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [configPath, setConfigPath] = useState<string>('');
  const [configExists, setConfigExists] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(
    null
  );

  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    setLoading(true);
    try {
      const result = await configService.getConfig();
      setConfigPath(result.file_path);
      setConfigExists(result.exists);
      if (result.exists && result.models) {
        setConfig(result.models);
      } else {
        // Load example config
        try {
          const example = await configService.getExampleConfig();
          if (example.models) {
            setConfig(example.models);
          }
        } catch {
          setConfig([{ ...DEFAULT_MODEL }]);
        }
      }
    } catch (err: any) {
      showMessage('error', '載入配置失敗: ' + err.message);
      setConfig([{ ...DEFAULT_MODEL }]);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveConfig = async () => {
    setSaving(true);
    try {
      const result = await configService.updateConfig(config);
      showMessage('success', result.message);
      await loadConfig();
    } catch (err: any) {
      showMessage('error', '儲存失敗: ' + err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleLoadConfig = async () => {
    try {
      const result = await configService.loadConfig();
      showMessage('success', result.message);
    } catch (err: any) {
      showMessage('error', '載入失敗: ' + err.message);
    }
  };

  const showMessage = (type: 'success' | 'error', text: string) => {
    setMessage({ type, text });
    setTimeout(() => setMessage(null), 5000);
  };

  const addModel = () => {
    setConfig([...config, { ...DEFAULT_MODEL }]);
  };

  const removeModel = (index: number) => {
    setConfig(config.filter((_, i) => i !== index));
  };

  const updateModel = (index: number, field: keyof ModelConfig, value: any) => {
    const newConfig = [...config];
    newConfig[index] = { ...newConfig[index], [field]: value };
    setConfig(newConfig);
  };

  return (
    <div className="settings-page control-panel">
      <header className="page-header system-header">
        <div className="header-title">
          <div className="title-icon-wrapper">
            <SettingsIcon size={32} />
            <span className="pulse-dot"></span>
          </div>
          <div>
            <h1>Ai模型控制中心</h1>
            <p className="page-subtitle">基礎架構配置與模型管理</p>
          </div>
        </div>
        <div className="header-actions">
          <Button variant="secondary" onClick={loadConfig} disabled={loading} className="control-btn">
            <RefreshCw size={18} />
            重新載入
          </Button>
          <Button onClick={handleSaveConfig} disabled={saving} className="control-btn primary-glow">
            {saving ? '儲存中...' : <><Save size={18} />提交變更</>}
          </Button>
        </div>
      </header>

      {message && (
        <div className={`message-banner system-alert ${message.type}`}>
          {message.type === 'success' ? (
            <CheckCircle size={20} />
          ) : (
            <AlertCircle size={20} />
          )}
          <span className="alert-text">{message.text}</span>
        </div>
      )}

      {/* Config File Status */}
      <Card className="info-card system-status">
        <div className="status-header">
          <div className="status-icon">
            <FileText size={24} />
          </div>
          <div className="status-content">
            <h3 className="status-title">配置檔案資訊</h3>
            <p className="config-path">{configPath}</p>
            <div className="status-meta">
              <StatusBadge
                status={configExists ? 'success' : 'warning'}
                label={configExists ? '已啟用' : '未初始化'}
              />
              <span className="meta-text">
                {configExists ? '系統配置已載入' : '等待初始化'}
              </span>
            </div>
          </div>
        </div>
        {configExists && (
          <div className="status-actions">
            <Button
              variant="secondary"
              size="sm"
              onClick={handleLoadConfig}
              className="system-btn"
            >
              <Upload size={16} />
              初始化模型
            </Button>
          </div>
        )}
      </Card>

      {/* Models Configuration */}
      <section className="settings-section control-section">
        <div className="section-header">
          <div className="section-title-group">
            <Cpu className="section-icon" size={24} />
            <h2 className="section-title">AI模型</h2>
            <span className="section-count">{config.length} 已配置</span>
          </div>
          <Button onClick={addModel} size="sm" className="add-model-btn">
            <Plus size={16} />
            新增模型
          </Button>
        </div>

        {config.length === 0 ? (
          <Card className="empty-state system-idle">
            <Activity size={48} className="idle-icon" />
            <h3>未配置模型</h3>
            <p>初始化你的第一個推理模型以開始</p>
            <Button onClick={addModel} className="init-btn">
              <Plus size={18} />
              初始化第一個模型
            </Button>
          </Card>
        ) : (
          <div className="models-config-list">
            {config.map((model, index) => (
              <Card key={index} className="model-config-card control-module">
                <div className="module-header">
                  <div className="module-title-group">
                    <div className="module-indicator">
                      <span className="indicator-light active"></span>
                    </div>
                    <div>
                      <h3 className="module-title">AI 模型 {String(index + 1).padStart(2, '0')}</h3>
                      <p className="module-subtitle">{model.provider.toUpperCase()} • {model.model_name || '未配置'}</p>
                    </div>
                  </div>
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => removeModel(index)}
                    className="remove-btn"
                  >
                    <Trash2 size={16} />
                    移除
                  </Button>
                </div>

                <div className="model-config-grid">
                  {/* Model Selection Section */}
                  <div className="config-section">
                    <div className="section-label">
                      <Cpu size={16} />
                      <span>模型選擇</span>
                    </div>
                    
                    <div className="control-group">
                      <label className="control-label">
                        Provider
                        <span className="label-required">*</span>
                      </label>
                      <div className="control-wrapper">
                        <select
                          className="control-select"
                          value={model.provider}
                          onChange={(e) => updateModel(index, 'provider', e.target.value)}
                        >
                          <option value="openai">OpenAI</option>
                          <option value="anthropic">Anthropic</option>
                          <option value="google">Google</option>
                          <option value="azure">Azure</option>
                          <option value="huggingface">HuggingFace</option>
                          <option value="local">Local</option>
                        </select>
                        <span className="control-hint">選擇 AI Provider</span>
                      </div>
                    </div>

                    <div className="control-group">
                      <label className="control-label">
                        模型名稱
                        <span className="label-required">*</span>
                      </label>
                      <div className="control-wrapper">
                        <input
                          type="text"
                          className="control-input mono"
                          value={model.model_name}
                          onChange={(e) => updateModel(index, 'model_name', e.target.value)}
                          placeholder="gpt-4-turbo"
                        />
                        <span className="control-hint">模型名稱或端點識別碼</span>
                      </div>
                    </div>

                    <div className="control-group">
                      <label className="control-label">
                        <Shield size={14} />
                        認證密鑰
                      </label>
                      <div className="control-wrapper">
                        <input
                          type="password"
                          className="control-input secure"
                          value={model.api_key || ''}
                          onChange={(e) => updateModel(index, 'api_key', e.target.value)}
                          placeholder="sk-..."
                        />
                        <span className="control-hint">API 認證憑證</span>
                      </div>
                    </div>
                  </div>

                  {/* Reasoning & Safety Controls */}
                  <div className="config-section">
                    <div className="section-label">
                      <Sliders size={16} />
                      <span>推理策略</span>
                    </div>

                    <div className="control-group">
                      <label className="control-label">
                        溫度係數
                      </label>
                      <div className="slider-control">
                        <div className="slider-header">
                          <span className="slider-value">{(model.temperature ?? 0.7).toFixed(2)}</span>
                          <span className="slider-range">0.0 - 2.0</span>
                        </div>
                        <input
                          type="range"
                          className="control-slider"
                          min="0"
                          max="2"
                          step="0.05"
                          value={model.temperature ?? 0.7}
                          onChange={(e) =>
                            updateModel(index, 'temperature', parseFloat(e.target.value))
                          }
                        />
                        <div className="slider-labels">
                          <span className="label-item">確定性</span>
                          <span className="label-item">平衡</span>
                          <span className="label-item">創造性</span>
                        </div>
                        <span className="control-hint">
                          {(model.temperature ?? 0.7) < 0.3
                            ? '低隨機性 - 一致、專注的輸出'
                            : (model.temperature ?? 0.7) < 1.0
                            ? '中等隨機性 - 平衡的探索'
                            : '高隨機性 - 創意、多樣化的回應'}
                        </span>
                      </div>
                    </div>

                    <div className="control-group">
                      <label className="control-label">
                        <Zap size={14} />
                        Token 限制
                      </label>
                      <div className="slider-control">
                        <div className="slider-header">
                          <span className="slider-value mono">{model.max_tokens ?? 1000}</span>
                          <span className="slider-range">1 - 32,000</span>
                        </div>
                        <input
                          type="range"
                          className="control-slider"
                          min="1"
                          max="32000"
                          step="100"
                          value={model.max_tokens ?? 1000}
                          onChange={(e) =>
                            updateModel(index, 'max_tokens', parseInt(e.target.value))
                          }
                        />
                        <div className="slider-labels">
                          <span className="label-item">最小</span>
                          <span className="label-item">標準</span>
                          <span className="label-item">擴展</span>
                        </div>
                        <span className="control-hint">
                          {(model.max_tokens ?? 1000) < 2000
                            ? '簡短回應 - 低延遲與成本'
                            : (model.max_tokens ?? 1000) < 8000
                            ? '中等回應 - 平衡吸量'
                            : '長篇回應 - 最大推理深度'}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </section>

      {/* Configuration Preview */}
      <section className="settings-section">
        <div className="section-header">
          <div className="section-title-group">
            <FileText className="section-icon" size={24} />
            <h2 className="section-title">配置檔案預覽</h2>
          </div>
        </div>
        <Card className="preview-card terminal-card">
          <div className="terminal-header">
            <span className="terminal-title">models_config.json</span>
            <span className="terminal-status">唯讀檢視</span>
          </div>
          <pre className="config-preview terminal-content">
            {JSON.stringify({ models: config }, null, 2)}
          </pre>
        </Card>
      </section>
    </div>
  );
};
