/**
 * Models Management Page
 * 
 * 模型管理頁面，顯示已載入的模型和外掛
 * 模型配置來自 config/models_config.json（扁平格式）
 */

import React, { useState, useEffect } from 'react';
import { RefreshCw, Package, CheckCircle, XCircle, Loader } from 'lucide-react';
import { modelService, configService } from '@/api';
import { Card } from '@/components/Card/Card';
import { Button } from '@/components/Button/Button';
import { StatusBadge } from '@/components/StatusBadge/StatusBadge';
import type { ModelConfig } from '@/api/config';
import './Models.css';

interface LoadedModel {
  provider: string;
  model_name: string;
  temperature: number;
  max_tokens: number;
}

export const Models: React.FC = () => {
  const [loadedModels, setLoadedModels] = useState<LoadedModel[]>([]);
  const [config, setConfig] = useState<ModelConfig[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingConfig, setLoadingConfig] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [modelsRes, configRes] = await Promise.all([
        modelService.getLoadedModels(),
        configService.getConfig(),
      ]);

      setLoadedModels((modelsRes.models as unknown as LoadedModel[]) || []);
      if (configRes.exists && configRes.models) {
        setConfig(configRes.models);
      }
    } catch (err: any) {
      setError(err.message || '載入資料失敗');
    } finally {
      setLoading(false);
    }
  };

  const handleLoadConfig = async () => {
    setLoadingConfig(true);
    try {
      const result = await configService.loadConfig();
      if (result.success) {
        await loadData();
        alert(result.message);
      }
    } catch (err: any) {
      alert('載入配置失敗: ' + err.message);
    } finally {
      setLoadingConfig(false);
    }
  };

  if (loading) {
    return (
      <div className="models-page">
        <div className="loading-container">
          <Loader className="spinner" size={48} />
          <p>載入中...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="models-page">
      <header className="page-header">
        <div>
          <h1>模型管理</h1>
          <p className="page-subtitle">管理 Target Models、Providers 和外掛</p>
        </div>
        <div className="header-actions">
          <Button
            variant="secondary"
            onClick={loadData}
            disabled={loading}
          >
            <RefreshCw size={18} />
            重新整理
          </Button>
          <Button
            onClick={handleLoadConfig}
            disabled={loadingConfig}
          >
            {loadingConfig ? <Loader className="spinner" size={18} /> : <Package size={18} />}
            載入配置
          </Button>
        </div>
      </header>

      {error && (
        <div className="error-banner">
          <XCircle size={20} />
          {error}
        </div>
      )}

      {/* Loaded Models */}
      <section className="models-section">
        <div className="section-header">
          <h2>已載入的模型</h2>
          <StatusBadge
            status={loadedModels.length > 0 ? 'success' : 'warning'}
            label={`${loadedModels.length} 個模型`}
          />
        </div>

        {loadedModels.length === 0 ? (
          <Card className="empty-state">
            <XCircle size={48} />
            <h3>尚未載入任何模型</h3>
            <p>請先配置並載入模型</p>
            <Button onClick={handleLoadConfig}>載入配置</Button>
          </Card>
        ) : (
          <div className="models-grid">
            {loadedModels.map((model, index) => (
              <Card key={index} className="model-card">
                <div className="model-header">
                  <CheckCircle className="model-icon" size={24} />
                  <div>
                    <h3>{model.model_name}</h3>
                    <span className="model-provider">{model.provider}</span>
                  </div>
                </div>
                <div className="model-details">
                  <div className="detail-item">
                    <span className="detail-label">Temperature:</span>
                    <span className="detail-value">{model.temperature}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Max Tokens:</span>
                    <span className="detail-value">{model.max_tokens}</span>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </section>

      {/* Configuration Preview */}
      {config.length > 0 && (
        <section className="models-section">
          <div className="section-header">
            <h2>配置檔預覽</h2>
            <StatusBadge status="info" label={`${config.length} 個配置`} />
          </div>

          <Card className="config-card">
            <pre className="config-preview">
              {JSON.stringify(config, null, 2)}
            </pre>
          </Card>
        </section>
      )}
    </div>
  );
};
