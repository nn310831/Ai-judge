/**
 * Results API Service
 */

import { api } from './client';
import type { TestDetails } from './test';

export interface Metrics {
  total_tests: number;
  asr: number;
  average_score: number;
  refusal_rate: number;
  score_distribution: Record<string, number>;
  std_deviation: number;
  median_score: number;
  min_score: number;
  max_score: number;
}

export interface TestMetrics {
  test_id: string;
  overall: Metrics;
  by_model: Record<string, Metrics>;
  by_category: Record<string, Metrics>;
}

export interface ModelComparison {
  models: string[];
  metrics: Record<string, Metrics>;
  comparison: {
    best_model: string;
    worst_model: string;
    differences: Record<string, any>;
  };
}

export interface StatisticalTestResult {
  test_type: string;
  statistic: number;
  p_value: number;
  significant: boolean;
  effect_size?: number;
  interpretation: string;
}

export const resultsService = {
  /**
   * Get test results
   */
  getTestResults: async (testId: string): Promise<TestDetails> => {
    return api.get<TestDetails>(`/results/${testId}`);
  },

  /**
   * Get test metrics
   */
  getTestMetrics: async (testId: string): Promise<TestMetrics> => {
    return api.get<TestMetrics>(`/results/${testId}/metrics`);
  },

  /**
   * Compare models
   */
  compareModels: async (testId: string): Promise<ModelComparison> => {
    return api.get<ModelComparison>(`/results/${testId}/comparison`);
  },

  /**
   * Run statistical test
   */
  runStatisticalTest: async (
    testId: string,
    modelA: string,
    modelB: string,
    testType: 't_test' | 'mann_whitney' = 't_test'
  ): Promise<StatisticalTestResult> => {
    return api.post<StatisticalTestResult>(
      `/results/${testId}/statistical-test`,
      null,
      {
        params: {
          model_a: modelA,
          model_b: modelB,
          test_type: testType,
        },
      }
    );
  },

  /**
   * Export results
   */
  exportResults: async (
    testId: string,
    format: 'json' | 'csv' = 'json'
  ): Promise<any> => {
    return api.get(`/results/${testId}/export`, {
      params: { format },
    });
  },
};
