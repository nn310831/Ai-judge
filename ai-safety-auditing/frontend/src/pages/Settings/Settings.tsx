/**
 * Settings Page - Configuration Management
 * 
 * 提供模型配置的管理界面
 * 配置格式：扁平結構，每個模型包含 provider、model_name、api_key、temperature、max_tokens
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
    <div className="settings-page">
      <header className="page-header">
        <div>
          <h1>
            <SettingsIcon size={32} />
            系統設定
          </h1>
          <p className="page-subtitle">配置模型和系統參數</p>
        </div>
        <div className="header-actions">
          <Button variant="secondary" onClick={loadConfig} disabled={loading}>
            <RefreshCw size={18} />
            重新載入
          </Button>
          <Button onClick={handleSaveConfig} disabled={saving}>
            {saving ? '儲存中...' : <><Save size={18} />儲存配置</>}
          </Button>
        </div>
      </header>

      {message && (
        <div className={`message-banner ${message.type}`}>
          {message.type === 'success' ? (
            <CheckCircle size={20} />
          ) : (
            <AlertCircle size={20} />
          )}
          {message.text}
        </div>
      )}

      {/* Config File Info */}
      <Card className="info-card">
        <div className="info-header">
          <FileText size={24} />
          <div>
            <h3>配置檔資訊</h3>
            <p className="config-path">{configPath}</p>
          </div>
          <StatusBadge
            status={configExists ? 'success' : 'warning'}
            label={configExists ? '已存在' : '尚未建立'}
          />
        </div>
        <div className="info-actions">
          <Button
            variant="secondary"
            size="sm"
            onClick={handleLoadConfig}
            disabled={!configExists}
          >
            <Upload size={16} />
            載入並初始化模型
          </Button>
        </div>
      </Card>

      {/* Models Configuration */}
      <section className="settings-section">
        <div className="section-header">
          <h2>模型配置</h2>
          <Button onClick={addModel} size="sm">
            <Plus size={16} />
            新增模型
          </Button>
        </div>

        {config.length === 0 ? (
          <Card className="empty-state">
            <AlertCircle size={48} />
            <h3>尚無模型配置</h3>
            <Button onClick={addModel}>新增第一個模型</Button>
          </Card>
        ) : (
          <div className="models-config-list">
            {config.map((model, index) => (
              <Card key={index} className="model-config-card">
                <div className="model-config-header">
                  <h3>模型 {index + 1}</h3>
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => removeModel(index)}
                  >
                    <Trash2 size={16} />
                    移除
                  </Button>
                </div>

                <div className="model-config-form">
                  <div className="form-group">
                    <label>Provider *</label>
                    <select
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
                  </div>

                  <div className="form-group">
                    <label>Model Name *</label>
                    <input
                      type="text"
                      value={model.model_name}
                      onChange={(e) => updateModel(index, 'model_name', e.target.value)}
                      placeholder="gpt-4"
                    />
                  </div>

                  <div className="form-group">
                    <label>API Key</label>
                    <input
                      type="password"
                      value={model.api_key || ''}
                      onChange={(e) => updateModel(index, 'api_key', e.target.value)}
                      placeholder="sk-..."
                    />
                  </div>

                  <div className="form-row">
                    <div className="form-group">
                      <label>Temperature</label>
                      <input
                        type="number"
                        min="0"
                        max="2"
                        step="0.1"
                        value={model.temperature}
                        onChange={(e) =>
                          updateModel(index, 'temperature', parseFloat(e.target.value))
                        }
                      />
                    </div>

                    <div className="form-group">
                      <label>Max Tokens</label>
                      <input
                        type="number"
                        min="1"
                        max="32000"
                        step="1"
                        value={model.max_tokens}
                        onChange={(e) =>
                          updateModel(index, 'max_tokens', parseInt(e.target.value))
                        }
                      />
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
        <h2>配置預覽 (JSON)</h2>
        <Card className="preview-card">
          <pre className="config-preview">
            {JSON.stringify({ models: config }, null, 2)}
          </pre>
        </Card>
      </section>

      {/* Save Actions */}
      <div className="save-actions">
        <Button
          variant="secondary"
          onClick={loadConfig}
          disabled={loading}
        >
          <RefreshCw size={18} />
          重置變更
        </Button>
        <Button
          onClick={handleSaveConfig}
          disabled={saving || config.length === 0}
        >
          {saving ? '儲存中...' : <><Save size={18} />儲存配置</>}
        </Button>
      </div>
    </div>
  );
};
