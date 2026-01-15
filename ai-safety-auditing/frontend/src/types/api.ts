/**
 * API Type Definitions
 * AI Safety Auditing System
 */

// ===== Attack Generator =====
export interface AttackPrompt {
  id: string;
  prompt: string;
  category: AttackCategory;
  created_at?: string;
  malicious_task?: string;
}

export type AttackCategory =
  | 'prompt_injection'
  | 'jailbreak'
  | 'roleplay'
  | 'scenario'
  | 'encoding'
  | 'multilingual'
  | 'all';

export interface GenerateAttacksRequest {
  category: AttackCategory;
  count: number;
  use_llm?: boolean;
}

export interface GenerateAttacksResponse {
  success: boolean;
  attacks: AttackPrompt[];
  total: number;
  message?: string;
}

// ===== Target Model =====
export interface TargetModel {
  model_name: string;
  model_type: string;
  description?: string;
  is_loaded: boolean;
}

export interface ModelTestRequest {
  model_name: string;
  attack_prompts: string[];
}

export interface ModelTestResponse {
  model_name: string;
  responses: ModelResponse[];
  total_tests: number;
}

export interface ModelResponse {
  attack_prompt: string;
  response: string;
  latency_ms: number;
  success: boolean;
  error?: string;
}

// ===== Judge Evaluation =====
export interface JudgeEvaluationRequest {
  attack_prompt: string;
  model_response: string;
}

export interface JudgeEvaluationResponse {
  score: number; // 1-5
  is_safe: boolean;
  reasoning: string;
  violated_policies: string[];
  refusal_detected: boolean;
  judge_model: string;
  attack_prompt: string;
  model_response: string;
}

export interface BatchEvaluateRequest {
  test_cases: Array<{
    attack_prompt: string;
    model_response: string;
  }>;
}

export interface BatchEvaluateResponse {
  evaluations: JudgeEvaluationResponse[];
  total_evaluated: number;
}

// ===== Metrics & Statistics =====
export interface Metrics {
  total_tests: number;
  asr: number; // Attack Success Rate
  average_score: number;
  refusal_rate: number;
  score_distribution: Record<number, number>; // {1: 10, 2: 15, ...}
  std_deviation: number;
  median_score: number;
  min_score: number;
  max_score: number;
}

export interface CategoryMetrics {
  [category: string]: {
    asr: number;
    avg_score: number;
    refusal_rate: number;
    count: number;
  };
}

export interface StatisticsResponse {
  metrics: Metrics;
  category_metrics: CategoryMetrics;
  timestamp: string;
}

// ===== System State =====
export interface SystemState {
  generator: {
    loaded: boolean;
    model: string | null;
    use_llm: boolean;
  };
  target_models: TargetModel[];
  judge: {
    loaded: boolean;
    model: string;
  };
}

// ===== API Response Wrapper =====
export interface ApiResponse<T> {
  data: T;
  message?: string;
  timestamp: string;
}

export interface ApiError {
  error: string;
  detail?: string;
  status_code: number;
}

// ===== Common Types =====
export interface PaginationParams {
  page?: number;
  page_size?: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// ===== Full Audit Report =====
export interface AuditReport {
  id: string;
  model_name: string;
  attacks: AttackPrompt[];
  responses: ModelResponse[];
  evaluations: JudgeEvaluationResponse[];
  metrics: Metrics;
  category_metrics: CategoryMetrics;
  created_at: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
}
