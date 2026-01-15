/**
 * Configuration API Service
 * 
 * 管理模型配置的 API 服務
 * 配置格式採用扁平結構，與後端 Pydantic 模型一致
 */

import { api } from './client';

export interface ModelConfig {
  provider: string;
  model_name: string;
  api_key?: string;
  temperature?: number;
  max_tokens?: number;
}

export interface ConfigFileResponse {
  exists: boolean;
  file_path: string;
  models?: ModelConfig[];
  error?: string;
}

export const configService = {
  /**
   * Get current configuration
   */
  getConfig: async (): Promise<ConfigFileResponse> => {
    return api.get<ConfigFileResponse>('/config/');
  },

  /**
   * Update configuration
   */
  updateConfig: async (models: ModelConfig[]): Promise<{
    success: boolean;
    message: string;
  }> => {
    return api.post('/config/', { models });
  },

  /**
   * Get example configuration
   */
  getExampleConfig: async (): Promise<{ models: ModelConfig[] }> => {
    return api.get('/config/example');
  },

  /**
   * Load configuration and initialize models
   */
  loadConfig: async (): Promise<{
    success: boolean;
    message: string;
    total_models?: number;
    loaded?: number;
  }> => {
    return api.post('/config/load');
  },
};
