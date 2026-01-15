/**
 * Test Execution API Service
 */

import { api } from './client';
import type { AttackPrompt } from '@/types/api';

export interface RunTestRequest {
  attacks?: AttackPrompt[];
  model_names?: string[];
}

export interface TestProgress {
  test_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;  // 0-100
  current: number;   // 已完成數量
  total: number;     // 總數量
  message?: string;  // 狀態訊息
  start_time?: string;  // 開始時間
  end_time?: string;    // 結束時間
}

export interface TestResult {
  model: string;
  attack_id: string;
  attack_category: string;
  attack_prompt: string;
  model_response?: string;
  evaluation?: {
    score: number;
    is_safe: boolean;
    reasoning: string;
  };
  success: boolean;
  error?: string;
}

export interface TestDetails {
  test_id: string;
  status: string;
  results: TestResult[];
  total: number;
  current: number;  // 使用 current 與後端一致
  start_time: string;
  end_time?: string;
}

export const testService = {
  /**
   * Run a test with attacks
   */
  runTest: async (request: RunTestRequest): Promise<{
    test_id: string;
    message: string;
    total_tests: number;
  }> => {
    // 增加超時時間到 5 分鐘，因為測試執行需要較長時間
    return api.post('/test/run', request);
  },

  /**
   * Get test status
   */
  getTestStatus: async (testId: string): Promise<TestProgress> => {
    return api.get<TestProgress>(`/test/status/${testId}`);
  },

  /**
   * List all tests
   */
  listTests: async (): Promise<{
    tests: TestProgress[];
    total: number;
  }> => {
    return api.get('/test/list');
  },
};
