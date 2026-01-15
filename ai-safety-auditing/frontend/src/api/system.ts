/**
 * System State API Service
 * 注意：這些是假設的 API endpoints，實際後端路由為：
 * - /api/config
 * - /api/models
 * - /api/test
 * - /api/results
 */

import { api } from './client';
import type { SystemState, Metrics, StatisticsResponse } from '@/types/api';

export const systemService = {
  /**
   * Get system state (假設 endpoint，需要後端實作)
   */
  getState: async (): Promise<SystemState> => {
    // TODO: 實際後端路由需要實作此 endpoint
    return api.get<SystemState>('/config/state');
  },

  /**
   * Calculate metrics (假設 endpoint)
   * 使用測試結果來計算指標
   */
  calculateMetrics: async (testId?: string): Promise<Metrics> => {
    // 如果有 testId，使用實際的後端路由
    if (testId) {
      return api.get<Metrics>(`/results/${testId}/metrics`);
    }
    
    // 否則返回模擬數據
    return {
      total_tests: 0,
      asr: 0,
      average_score: 0,
      refusal_rate: 0,
      score_distribution: {},
      std_deviation: 0,
      median_score: 0,
      min_score: 0,
      max_score: 0,
    };
  },

  /**
   * Get full statistics (假設 endpoint)
   */
  getStatistics: async (): Promise<StatisticsResponse> => {
    // TODO: 需要後端實作
    throw new Error('此 API 尚未實作');
  },

  /**
   * Export data (假設 endpoint)
   */
  exportData: async (_format: 'json' | 'csv' = 'json'): Promise<Blob> => {
    // TODO: 需要後端實作
    throw new Error('此 API 尚未實作');
  },

  /**
   * Reset system (假設 endpoint)
   */
  reset: async (): Promise<{ message: string }> => {
    // TODO: 需要後端實作
    throw new Error('此 API 尚未實作');
  },

  /**
   * Health check
   */
  healthCheck: async (): Promise<{
    status: string;
    service?: string;
  }> => {
    return api.get('/health');
  },
};
