"""
OpenAI 模型適配器
"""

from openai import OpenAI
from typing import Dict, Any
import os
from src.target.base_model import BaseModel


class OpenAIModel(BaseModel):
    """OpenAI GPT 模型適配器"""
    
    def __init__(
        self,
        model_name: str,
        api_key: str = None,
        temperature: float = 0.0,
        max_tokens: int = 1000,
        **kwargs
    ):
        """
        初始化 OpenAI 模型
        
        Args:
            model_name: 模型名稱（如 "gpt-4", "gpt-3.5-turbo"）
            api_key: OpenAI API Key
            temperature: 溫度參數（0.0-2.0）
            max_tokens: 最大 token 數
            **kwargs: 其他參數
        """
        super().__init__(model_name=model_name, provider='openai')
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.extra_params = kwargs
    
    def _call_api(self, prompt: str) -> Dict[str, Any]:
        """實作 OpenAI API 呼叫"""
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **self.extra_params
        )
        
        return {
            "response": response.choices[0].message.content,
            "model": self.model_name,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            },
            "finish_reason": response.choices[0].finish_reason
        }
    
    def estimate_cost(self, num_requests: int, avg_tokens: int = 500) -> Dict[str, Any]:
        """估算成本（基於 OpenAI 定價）"""
        # 簡化的成本估算（實際價格請參考官方）
        pricing = {
            "gpt-4": {"input": 0.03, "output": 0.06},  # per 1K tokens
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015}
        }
        
        model_pricing = pricing.get(self.model_name, {"input": 0.01, "output": 0.03})
        
        estimated_input_tokens = avg_tokens * 0.7  # 假設 70% 是輸入
        estimated_output_tokens = avg_tokens * 0.3  # 30% 是輸出
        
        cost_per_request = (
            (estimated_input_tokens / 1000) * model_pricing["input"] +
            (estimated_output_tokens / 1000) * model_pricing["output"]
        )
        
        total_cost = cost_per_request * num_requests
        
        return {
            "estimated_cost": f"${total_cost:.4f}",
            "num_requests": num_requests,
            "cost_per_request": f"${cost_per_request:.6f}",
            "model": self.model_name
        }
