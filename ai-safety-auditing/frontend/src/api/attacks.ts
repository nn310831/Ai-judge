/**
 * Attack Generator API Service
 */

import { api } from './client';
import type {
  AttackPrompt,
  GenerateAttacksRequest,
  GenerateAttacksResponse,
  AttackCategory,
} from '@/types/api';

export const attackService = {
  /**
   * Generate new attack prompts
   */
  generateAttacks: async (
    params: GenerateAttacksRequest
  ): Promise<GenerateAttacksResponse> => {
    return api.post<GenerateAttacksResponse>('/test/generate-attacks', params);
  },

  /**
   * Get all generated attacks (from cache)
   */
  getAllAttacks: async (): Promise<AttackPrompt[]> => {
    const response = await api.get<{ attacks: AttackPrompt[]; total: number }>('/test/attacks');
    return response.attacks;
  },

  /**
   * Get attacks by category
   */
  getAttacksByCategory: async (category: AttackCategory): Promise<AttackPrompt[]> => {
    const allAttacks = await attackService.getAllAttacks();
    return allAttacks.filter(attack => attack.category === category);
  },

  /**
   * Get attack statistics
   */
  getStatistics: async () => {
    const attacks = await attackService.getAllAttacks();
    const byCategory: Record<string, number> = {};
    attacks.forEach(attack => {
      byCategory[attack.category] = (byCategory[attack.category] || 0) + 1;
    });
    return {
      total: attacks.length,
      by_category: byCategory,
    };
  },
};
