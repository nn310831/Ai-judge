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
  'all',
];

export const Testing: React.FC = () => {
  const [attacks, setAttacks] = useState<AttackPrompt[]>([]);
  const [filteredAttacks, setFilteredAttacks] = useState<AttackPrompt[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<AttackCategory | 'all'>('all');
  const [selectedAttacks, setSelectedAttacks] = useState<Set<string>>(new Set());
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
      const result = await attackService.generateAttacks({
        category: genCategory,
        count: genCount,
        use_llm: useLLM,
      });

      if (result.success) {
        setAttacks(result.attacks);
        alert(`成功生成 ${result.total} 個攻擊提示詞`);
      }
    } catch (err: any) {
      alert('生成失敗: ' + err.message);
    } finally {
      setGenerating(false);
    }
  };

  const handleRunTest = async () => {
    if (loadedModels.length === 0) {
      alert('請先載入模型');
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
      const result = await testService.runTest({
        attacks: attacksToTest,
      });

      alert(`測試已開始\nTest ID: ${result.test_id}\n總測試數: ${result.total_tests}`);
      await loadActiveTests();
    } catch (err: any) {
      alert('執行測試失敗: ' + err.message);
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
                  <option value="harmful_content">有害內容</option>
                  <option value="bias_discrimination">偏見歧視</option>
                  <option value="privacy_violation">隱私侵犯</option>
                  <option value="misinformation">錯誤資訊</option>
                  <option value="manipulation">操縱行為</option>
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
              <Trash2 size={16} />
              清除選擇
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
                onClick={() => toggleAttackSelection(attack.id)}
              >
                <div className="attack-header">
                  <div className="attack-checkbox">
                    {selectedAttacks.has(attack.id) && <CheckCircle size={20} />}
                  </div>
                  <div className="attack-info">
                    <div className="attack-meta">
                      <span className="attack-id">#{attack.id}</span>
                      <StatusBadge status="info" label={attack.category} />
                    </div>
                  </div>
                </div>
                <p className="attack-prompt">{attack.prompt}</p>
              </Card>
            ))}
          </div>
        )}
      </section>
    </div>
  );
};
