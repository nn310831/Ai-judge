"""
Anthropic Claude 模型適配器
"""

from anthropic import Anthropic
from typing import Dict, Any
import os
from src.target.base_model import BaseModel


class AnthropicModel(BaseModel):
    """Anthropic Claude 模型適配器"""
    
    def __init__(
        self,
        model_name: str,
        api_key: str = None,
        temperature: float = 0.0,
        max_tokens: int = 1000,
        **kwargs
    ):
        """
        初始化 Anthropic 模型
        
        Args:
            model_name: 模型名稱（如 "claude-3-5-sonnet-20241022"）
            api_key: Anthropic API Key
            temperature: 溫度參數（0.0-1.0）
            max_tokens: 最大 token 數
            **kwargs: 其他參數
        """
        super().__init__(model_name=model_name, provider='anthropic')
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=self.api_key)
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.extra_params = kwargs
    
    def _call_api(self, prompt: str) -> Dict[str, Any]:
        """實作 Anthropic API 呼叫"""
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}],
            **self.extra_params
        )
        
        return {
            "response": response.content[0].text,
            "model": self.model_name,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            },
            "stop_reason": response.stop_reason
        }
    
    def estimate_cost(self, num_requests: int, avg_tokens: int = 500) -> Dict[str, Any]:
        """估算成本（基於 Anthropic 定價）"""
        # 簡化的成本估算
        pricing = {
            "claude-3-5-sonnet-20241022": {"input": 0.003, "output": 0.015},
            "claude-3-opus": {"input": 0.015, "output": 0.075},
            "claude-3-sonnet": {"input": 0.003, "output": 0.015}
        }
        
        model_pricing = pricing.get(self.model_name, {"input": 0.003, "output": 0.015})
        
        estimated_input_tokens = avg_tokens * 0.7
        estimated_output_tokens = avg_tokens * 0.3
        
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
