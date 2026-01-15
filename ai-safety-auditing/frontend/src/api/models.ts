/**
 * Target Model API Service
 */

import { api } from './client';
import type {
  TargetModel,
} from '@/types/api';

export const modelService = {
  /**
   * Get all available providers
   */
  getProviders: async (): Promise<{ providers: string[]; total: number }> => {
    return api.get('/models/providers');
  },

  /**
   * Get loaded models
   */
  getLoadedModels: async (): Promise<{ models: TargetModel[]; total: number }> => {
    return api.get('/models/loaded');
  },

  /**
   * Get loaded plugins
   */
  getPlugins: async (): Promise<{ plugins: any[]; total: number }> => {
    return api.get('/models/plugins');
  },

  /**
   * Load a plugin
   */
  loadPlugin: async (filePath: string, shouldValidate: boolean = true): Promise<any> => {
    return api.post('/models/plugins/load', {
      file_path: filePath,
      should_validate: shouldValidate,
    });
  },

  /**
   * Load all plugins
   */
  loadAllPlugins: async (): Promise<{
    success: boolean;
    total: number;
    loaded: number;
    failed: number;
    plugins: any[];
  }> => {
    return api.post('/models/plugins/load-all');
  },
};
