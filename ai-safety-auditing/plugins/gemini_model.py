"""
Google Gemini 模型適配器
"""

import google.generativeai as genai
from typing import Dict, Any
import os
from src.target.base_model import BaseModel


class GeminiModel(BaseModel):
    """Google Gemini 模型適配器"""
    
    def __init__(
        self,
        model_name: str = "gemini-pro",
        api_key: str = None,
        temperature: float = 0.0,
        max_tokens: int = 1000,
        **kwargs
    ):
        """
        初始化 Gemini 模型
        
        Args:
            model_name: 模型名稱（如 "gemini-pro", "gemini-pro-vision"）
            api_key: Google API Key
            temperature: 溫度參數（0.0-1.0）
            max_tokens: 最大 token 數
            **kwargs: 其他參數
        """
        super().__init__(model_name=model_name, provider='gemini')
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        # 配置 API Key
        genai.configure(api_key=self.api_key)
        
        # 創建模型實例
        self.model = genai.GenerativeModel(model_name)
        
        # 生成配置
        self.generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
            **kwargs
        )
    
    def _call_api(self, prompt: str) -> Dict[str, Any]:
        """實作 Gemini API 呼叫"""
        response = self.model.generate_content(
            prompt,
            generation_config=self.generation_config
        )
        
        # 提取回應文本
        response_text = response.text if hasattr(response, 'text') else ""
        
        # 提取 token 使用量（如果可用）
        usage = {}
        if hasattr(response, 'usage_metadata'):
            usage = {
                "prompt_tokens": response.usage_metadata.prompt_token_count,
                "completion_tokens": response.usage_metadata.candidates_token_count,
                "total_tokens": response.usage_metadata.total_token_count
            }
        
        return {
            "response": response_text,
            "model": self.model_name,
            "usage": usage,
            "finish_reason": response.candidates[0].finish_reason.name if response.candidates else "UNKNOWN"
        }
    
    def estimate_cost(self, num_requests: int, avg_tokens: int = 500) -> Dict[str, Any]:
        """估算成本（基於 Gemini 定價）"""
        # Gemini 定價（截至 2024 年的參考價格）
        pricing = {
            "gemini-pro": {"input": 0.00025, "output": 0.0005},  # per 1K tokens
            "gemini-pro-vision": {"input": 0.00025, "output": 0.0005},
            "gemini-1.5-pro": {"input": 0.0035, "output": 0.0105},
            "gemini-1.5-flash": {"input": 0.00035, "output": 0.00105}
        }
        
        model_pricing = pricing.get(self.model_name, {"input": 0.00025, "output": 0.0005})
        
        estimated_input_tokens = avg_tokens * 0.7  # 假設 70% 是輸入
        estimated_output_tokens = avg_tokens * 0.3  # 30% 是輸出
        
        cost_per_request = (
            (estimated_input_tokens / 1000) * model_pricing["input"] +
            (estimated_output_tokens / 1000) * model_pricing["output"]
        )
        
        total_cost = cost_per_request * num_requests
        
        return {
            "model": self.model_name,
            "num_requests": num_requests,
            "avg_tokens_per_request": avg_tokens,
            "cost_per_request": round(cost_per_request, 6),
            "total_cost": round(total_cost, 4),
            "currency": "USD"
        }