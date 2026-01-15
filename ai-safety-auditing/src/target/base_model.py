"""
BaseModel 抽象類別
所有模型的統一介面
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import time


class BaseModel(ABC):
    """所有模型的基礎類別"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
    
    @abstractmethod
    def _call_api(self, prompt: str) -> Dict[str, Any]:
        """
        子類必須實作的 API 呼叫方法
        
        Args:
            prompt: 輸入提示詞
        
        Returns:
            字典格式：
            {
                "response": str,  # 模型回應
                "model": str,     # 模型名稱
                "usage": {        # Token 使用量（可選）
                    "prompt_tokens": int,
                    "completion_tokens": int,
                    "total_tokens": int
                }
            }
        """
        pass
    
    def generate(self, prompt: str) -> Dict[str, Any]:
        """
        統一的生成介面（加入計時）
        
        Args:
            prompt: 輸入提示詞
        
        Returns:
            包含回應和元資料的字典
        """
        start_time = time.time()
        
        try:
            result = self._call_api(prompt)
            latency = (time.time() - start_time) * 1000  # 毫秒
            result["latency_ms"] = latency
            result["success"] = True
            return result
        
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            return {
                "response": None,
                "model": self.model_name,
                "error": str(e),
                "latency_ms": latency,
                "success": False
            }
    
    def generate_with_retry(
        self,
        prompt: str,
        max_retries: int = 3,
        backoff_factor: float = 2.0
    ) -> Dict[str, Any]:
        """
        帶重試機制的生成
        
        Args:
            prompt: 輸入提示詞
            max_retries: 最大重試次數
            backoff_factor: 退避因子（每次重試等待時間倍數）
        
        Returns:
            包含回應和元資料的字典
        """
        last_error = None
        
        for attempt in range(max_retries):
            try:
                result = self.generate(prompt)
                
                if result.get("success", False):
                    return result
                
                last_error = result.get("error", "Unknown error")
            
            except Exception as e:
                last_error = str(e)
            
            if attempt < max_retries - 1:
                wait_time = backoff_factor ** attempt
                time.sleep(wait_time)
        
        # 所有重試都失敗
        return {
            "response": None,
            "model": self.model_name,
            "error": f"所有重試失敗。最後錯誤: {last_error}",
            "latency_ms": 0,
            "success": False
        }
    
    def estimate_cost(
        self,
        num_requests: int,
        avg_tokens: int = 500
    ) -> Dict[str, Any]:
        """
        估算成本（子類可覆寫以提供準確估算）
        
        Args:
            num_requests: 請求次數
            avg_tokens: 平均 token 數
        
        Returns:
            成本估算資訊
        """
        return {
            "estimated_cost": "N/A",
            "num_requests": num_requests,
            "note": "此模型未提供成本估算"
        }
    
    def __repr__(self):
        return f"{self.__class__.__name__}(model_name='{self.model_name}')"
