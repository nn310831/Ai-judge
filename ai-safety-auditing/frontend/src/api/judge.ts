/**
 * Judge Evaluation API Service
 */

import { api } from './client';
import type {
  JudgeEvaluationRequest,
  JudgeEvaluationResponse,
  BatchEvaluateRequest,
  BatchEvaluateResponse,
} from '@/types/api';

export const judgeService = {
  /**
   * Evaluate a single response
   */
  evaluateSingle: async (
    request: JudgeEvaluationRequest
  ): Promise<JudgeEvaluationResponse> => {
    return api.post<JudgeEvaluationResponse>('/judge/evaluate', request);
  },

  /**
   * Batch evaluate multiple responses
   */
  evaluateBatch: async (
    request: BatchEvaluateRequest
  ): Promise<BatchEvaluateResponse> => {
    return api.post<BatchEvaluateResponse>('/judge/evaluate-batch', request);
  },

  /**
   * Get evaluation rubric
   */
  getRubric: async (): Promise<{ rubric: string }> => {
    return api.get<{ rubric: string }>('/judge/rubric');
  },

  /**
   * Get all evaluations
   */
  getAllEvaluations: async (): Promise<JudgeEvaluationResponse[]> => {
    return api.get<JudgeEvaluationResponse[]>('/judge/evaluations');
  },

  /**
   * Clear all evaluations
   */
  clearEvaluations: async (): Promise<{ message: string }> => {
    return api.delete<{ message: string }>('/judge/evaluations');
  },
};
