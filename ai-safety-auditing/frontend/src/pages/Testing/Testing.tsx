/**
 * Testing Page - Attack Generation and Test Execution
 */

import React, { useState, useEffect } from 'react';
import {
  Zap,
  Play,
  RefreshCw,
  Loader,
  CheckCircle,
  AlertCircle,
  Filter,
  Trash2,
} from 'lucide-react';
import { attackService, testService, modelService } from '@/api';
import { Card } from '@/components/Card/Card';
import { Button } from '@/components/Button/Button';
import { StatusBadge } from '@/components/StatusBadge/StatusBadge';
import type { AttackPrompt, AttackCategory } from '@/types/api';
import type { TestProgress } from '@/api/test';
import './Testing.css';

const CATEGORIES: AttackCategory[] = [
  'prompt_injection',
  'jailbreak',
  'roleplay',
  'scenario',
  'encoding',
  'multilingual',
];

export const Testing: React.FC = () => {
  const [attacks, setAttacks] = useState<AttackPrompt[]>([]);
  const [filteredAttacks, setFilteredAttacks] = useState<AttackPrompt[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<AttackCategory | 'all'>('all');
  const [selectedAttacks, setSelectedAttacks] = useState<Set<string>>(new Set());
  const [selectedModels, setSelectedModels] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [testing, setTesting] = useState(false);
  const [activeTests, setActiveTests] = useState<TestProgress[]>([]);
  const [loadedModels, setLoadedModels] = useState<any[]>([]);

  // Generation form
  const [genCategory, setGenCategory] = useState<AttackCategory>('prompt_injection');
  const [genCount, setGenCount] = useState(10);
  const [useLLM, setUseLLM] = useState(false);

  useEffect(() => {
    loadData();
    loadActiveTests();
  }, []);

    useEffect(() => {
    const interval = setInterval(() => {
      loadActiveTests();
    }, 2000); // 每 2 秒更新一次

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (selectedCategory === 'all') {
      setFilteredAttacks(attacks);
    } else {
      setFilteredAttacks(attacks.filter((a) => a.category === selectedCategory));
    }
  }, [selectedCategory, attacks]);

  const loadData = async () => {
    setLoading(true);
    try {
      const [attacksData, modelsData] = await Promise.all([
        attackService.getAllAttacks(),
        modelService.getLoadedModels(),
      ]);
      setAttacks(attacksData);
      setLoadedModels(modelsData.models);
      // 預設選擇所有模型
      setSelectedModels(new Set(modelsData.models.map((m: any) => m.model_name)));
    } catch (err) {
      console.error('Failed to load data:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadActiveTests = async () => {
    try {
      const result = await testService.listTests();
      setActiveTests(result.tests.filter((t) => t.status === 'running' || t.status === 'pending'));
    } catch (err) {
      console.error('Failed to load tests:', err);
    }
  };

  const handleGenerateAttacks = async () => {
    setGenerating(true);
    try {
      console.log('發送請求:', { category: genCategory, count: genCount, use_llm: useLLM });
      const result = await attackService.generateAttacks({
        category: genCategory,
        count: genCount,
        use_llm: useLLM,
      });

      if (result.success) {
        // 將新攻擊附加到現有列表而不是替換
        setAttacks(prevAttacks => [...prevAttacks, ...result.attacks]);
        alert(`成功生成 ${result.total} 個攻擊提示詞`);
      }
    } catch (err: any) {
      console.error('生成攻擊失敗:', err);
      alert('生成失敗: ' + (err.message || JSON.stringify(err)));
    } finally {
      setGenerating(false);
    }
  };

  const handleRunTest = async () => {
    if (loadedModels.length === 0) {
      alert('請先載入模型');
      return;
    }

    if (selectedModels.size === 0) {
      alert('請至少選擇一個模型');
      return;
    }

    const attacksToTest =
      selectedAttacks.size > 0
        ? attacks.filter((a) => selectedAttacks.has(a.id))
        : attacks;

    if (attacksToTest.length === 0) {
      alert('請選擇或生成攻擊提示詞');
      return;
    }

    setTesting(true);
    try {
      console.log('執行測試:', {
        attacks: attacksToTest.length,
        models: Array.from(selectedModels),
      });
      
      const result = await testService.runTest({
        attacks: attacksToTest,
        model_names: Array.from(selectedModels),
      });

      console.log('測試已開始:', result);
      alert(`測試已開始\nTest ID: ${result.test_id}\n總測試數: ${result.total_tests}\n\n測試在後台執行中，請查看「執行中的測試」區塊`);
      await loadActiveTests();
    } catch (err: any) {
      console.error('執行測試失敗:', err);
      
      if (err.code === 'ECONNABORTED') {
        alert('測試請求超時。\n\n但測試可能已在後台開始執行，請稍後刷新頁面查看結果。');
      } else {
        alert('執行測試失敗: ' + (err.message || JSON.stringify(err)));
      }
    } finally {
      setTesting(false);
    }
  };

  const toggleAttackSelection = (id: string) => {
    const newSelection = new Set(selectedAttacks);
    if (newSelection.has(id)) {
      newSelection.delete(id);
    } else {
      newSelection.add(id);
    }
    setSelectedAttacks(newSelection);
  };

  const selectAll = () => {
    setSelectedAttacks(new Set(filteredAttacks.map((a) => a.id)));
  };

  const clearSelection = () => {
    setSelectedAttacks(new Set());
  };

  const deleteAttack = (attackId: string) => {
    setAttacks(prevAttacks => prevAttacks.filter(a => a.id !== attackId));
    // 同時從選取中移除
    setSelectedAttacks(prev => {
      const newSet = new Set(prev);
      newSet.delete(attackId);
      return newSet;
    });
  };

  const deleteSelectedAttacks = () => {
    if (selectedAttacks.size === 0) {
      alert('請先選擇要刪除的攻擊');
      return;
    }
    
    if (window.confirm(`確定要刪除 ${selectedAttacks.size} 個已選取的攻擊嗎？`)) {
      setAttacks(prevAttacks => prevAttacks.filter(a => !selectedAttacks.has(a.id)));
      setSelectedAttacks(new Set());
    }
  };

  const toggleModelSelection = (modelName: string) => {
    const newSelection = new Set(selectedModels);
    if (newSelection.has(modelName)) {
      newSelection.delete(modelName);
    } else {
      newSelection.add(modelName);
    }
    setSelectedModels(newSelection);
  };

  const selectAllModels = () => {
    setSelectedModels(new Set(loadedModels.map((m) => m.model_name)));
  };

  const clearModelSelection = () => {
    setSelectedModels(new Set());
  };

  const getCategoryStats = () => {
    const stats: Record<string, number> = {};
    attacks.forEach((attack) => {
      stats[attack.category] = (stats[attack.category] || 0) + 1;
    });
    return stats;
  };

  const categoryStats = getCategoryStats();

  return (
    <div className="testing-page">
      <header className="page-header">
        <div>
          <h1>攻擊測試</h1>
          <p className="page-subtitle">生成攻擊提示詞並執行安全性測試</p>
        </div>
        <div className="header-actions">
          <Button variant="secondary" onClick={loadData} disabled={loading}>
            <RefreshCw size={18} />
            重新整理
          </Button>
          <Button onClick={handleRunTest} disabled={testing || attacks.length === 0}>
            {testing ? <Loader className="spinner" size={18} /> : <Play size={18} />}
            執行測試
          </Button>
        </div>
      </header>

      {/* System Status */}
      <div className="status-bar">
        <div className="status-item">
          <span className="status-label">已載入模型:</span>
          <StatusBadge
            status={loadedModels.length > 0 ? 'success' : 'danger'}
            label={`${loadedModels.length} 個`}
          />
        </div>
        <div className="status-item">
          <span className="status-label">已選擇模型:</span>
          <StatusBadge
            status={selectedModels.size > 0 ? 'success' : 'warning'}
            label={`${selectedModels.size} 個`}
          />
        </div>
        <div className="status-item">
          <span className="status-label">攻擊總數:</span>
          <StatusBadge status="info" label={`${attacks.length} 個`} />
        </div>
        <div className="status-item">
          <span className="status-label">已選擇:</span>
          <StatusBadge status="info" label={`${selectedAttacks.size} 個`} />
        </div>
        <div className="status-item">
          <span className="status-label">執行中的測試:</span>
          <StatusBadge
            status={activeTests.length > 0 ? 'warning' : 'success'}
            label={`${activeTests.length} 個`}
          />
        </div>
      </div>

      {/* Attack Generator */}
      <section className="testing-section">
        <h2>攻擊生成器</h2>
        <Card className="generator-card">
          <div className="generator-form">
            <div className="form-row">
              <div className="form-group">
                <label>類別</label>
                <select
                  value={genCategory}
                  onChange={(e) => setGenCategory(e.target.value as AttackCategory)}
                >
                  <option value="prompt_injection">提示詞注入</option>
                  <option value="jailbreak">越獄</option>
                  <option value="roleplay">角色扮演</option>
                  <option value="scenario">場景模擬</option>
                  <option value="encoding">編碼攻擊</option>
                  <option value="multilingual">多語言</option>
                  <option value="all">所有類別</option>
                </select>
              </div>

              <div className="form-group">
                <label>數量</label>
                <input
                  type="number"
                  min="1"
                  max="100"
                  value={genCount}
                  onChange={(e) => setGenCount(parseInt(e.target.value))}
                />
              </div>

              <div className="form-group checkbox-group">
                <label>
                  <input
                    type="checkbox"
                    checked={useLLM}
                    onChange={(e) => setUseLLM(e.target.checked)}
                  />
                  使用 LLM 生成
                </label>
              </div>
            </div>

            <Button
              onClick={handleGenerateAttacks}
              disabled={generating}
              className="generate-btn"
            >
              {generating ? (
                <>
                  <Loader className="spinner" size={18} />
                  生成中...
                </>
              ) : (
                <>
                  <Zap size={18} />
                  生成攻擊
                </>
              )}
            </Button>
          </div>
        </Card>
      </section>

      {/* Model Selection */}
      <section className="testing-section">
        <div className="section-header">
          <h2>選擇測試模型</h2>
          <div className="section-actions">
            <Button variant="secondary" size="sm" onClick={selectAllModels}>
              全選
            </Button>
            <Button variant="secondary" size="sm" onClick={clearModelSelection}>
              <Trash2 size={16} />
              清除選擇
            </Button>
          </div>
        </div>

        {loadedModels.length === 0 ? (
          <Card className="empty-state">
            <AlertCircle size={48} />
            <h3>尚未載入模型</h3>
            <p>請在設定頁面配置並載入模型</p>
          </Card>
        ) : (
          <div className="models-grid">
            {loadedModels.map((model: any) => (
              <Card
                key={model.model_name}
                className={`model-select-card ${
                  selectedModels.has(model.model_name) ? 'selected' : ''
                }`}
                onClick={() => toggleModelSelection(model.model_name)}
              >
                <div className="model-select-header">
                  <div className="model-checkbox">
                    {selectedModels.has(model.model_name) && <CheckCircle size={20} />}
                  </div>
                  <div className="model-info">
                    <h3 className="model-name">{model.model_name}</h3>
                    <div className="model-meta">
                      <StatusBadge status="info" label={model.provider} />
                      <span className="model-param">temp: {model.temperature}</span>
                      <span className="model-param">tokens: {model.max_tokens}</span>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </section>

      {/* Active Tests */}
      {activeTests.length > 0 && (
        <section className="testing-section">
          <h2>執行中的測試</h2>
          <div className="tests-grid">
            {activeTests.map((test) => (
              <Card key={test.test_id} className="test-card">
                <div className="test-header">
                  <div>
                    <h3>Test ID: {test.test_id}</h3>
                    <StatusBadge status={test.status === 'running' ? 'warning' : 'info'} label={test.status} />
                  </div>
                  <Loader className="spinner" size={24} />
                </div>
                <div className="test-progress">
                  <div className="progress-bar">
                    <div
                      className="progress-fill"
                      style={{ width: `${(test.current / test.total) * 100}%` }}
                    />
                  </div>
                  <div className="progress-text">
                    {test.current} / {test.total} ({Math.round((test.current / test.total) * 100)}%)
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </section>
      )}

      {/* Attacks List */}
      <section className="testing-section">
        <div className="section-header">
          <h2>攻擊列表</h2>
          <div className="section-actions">
            <div className="filter-group">
              <Filter size={18} />
              <select
                value={selectedCategory}
                onChange={(e) =>
                  setSelectedCategory(e.target.value as AttackCategory | 'all')
                }
              >
                <option value="all">全部 ({attacks.length})</option>
                {CATEGORIES.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat} ({categoryStats[cat] || 0})
                  </option>
                ))}
              </select>
            </div>
            <Button variant="secondary" size="sm" onClick={selectAll}>
              全選
            </Button>
            <Button variant="secondary" size="sm" onClick={clearSelection}>
              清除選擇
            </Button>
            <Button variant="danger" size="sm" onClick={deleteSelectedAttacks}>
              <Trash2 size={16} />
              刪除已選取
            </Button>
          </div>
        </div>

        {filteredAttacks.length === 0 ? (
          <Card className="empty-state">
            <AlertCircle size={48} />
            <h3>尚無攻擊提示詞</h3>
            <p>請使用上方的生成器創建攻擊提示詞</p>
          </Card>
        ) : (
          <div className="attacks-list">
            {filteredAttacks.map((attack) => (
              <Card
                key={attack.id}
                className={`attack-card ${
                  selectedAttacks.has(attack.id) ? 'selected' : ''
                }`}
              >
                <div className="attack-header">
                  <div className="attack-checkbox" onClick={() => toggleAttackSelection(attack.id)}>
                    {selectedAttacks.has(attack.id) && <CheckCircle size={20} />}
                  </div>
                  <div className="attack-info" onClick={() => toggleAttackSelection(attack.id)}>
                    <div className="attack-meta">
                      <span className="attack-id">#{attack.id}</span>
                      <StatusBadge status="info" label={attack.category} />
                    </div>
                  </div>
                  <button 
                    className="delete-attack-btn"
                    onClick={(e) => {
                      e.stopPropagation();
                      if (window.confirm('確定要刪除此攻擊嗎？')) {
                        deleteAttack(attack.id);
                      }
                    }}
                    title="刪除攻擊"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
                <p className="attack-prompt" onClick={() => toggleAttackSelection(attack.id)}>{attack.prompt}</p>
              </Card>
            ))}
          </div>
        )}
      </section>
    </div>
  );
};
