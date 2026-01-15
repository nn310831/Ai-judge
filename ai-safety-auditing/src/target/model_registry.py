"""
模型註冊器
管理所有可用的模型類別
"""

from typing import Dict, Type, List
from src.target.base_model import BaseModel


class ModelRegistry:
    """模型註冊器"""
    
    _registry: Dict[str, Type[BaseModel]] = {}
    
    @classmethod
    def register(cls, provider: str, model_class: Type[BaseModel]):
        """
        註冊模型類別
        
        Args:
            provider: Provider 名稱（如 "openai", "anthropic"）
            model_class: 模型類別（必須繼承 BaseModel）
        
        Raises:
            TypeError: 如果 model_class 不是 BaseModel 的子類
        """
        if not issubclass(model_class, BaseModel):
            raise TypeError(f"{model_class.__name__} 必須繼承 BaseModel")
        
        cls._registry[provider] = model_class
        print(f"✅ 已註冊 provider: {provider} -> {model_class.__name__}")
    
    @classmethod
    def get(cls, provider: str) -> Type[BaseModel]:
        """
        取得模型類別
        
        Args:
            provider: Provider 名稱
        
        Returns:
            模型類別
        
        Raises:
            ValueError: 如果 provider 未註冊
        """
        if provider not in cls._registry:
            available = ', '.join(cls._registry.keys())
            raise ValueError(
                f"未註冊的 provider: {provider}\n"
                f"可用的 providers: {available}"
            )
        
        return cls._registry[provider]
    
    @classmethod
    def list_providers(cls) -> List[str]:
        """
        列出所有已註冊的 providers
        
        Returns:
            Provider 名稱列表
        """
        return list(cls._registry.keys())
    
    @classmethod
    def is_registered(cls, provider: str) -> bool:
        """
        檢查 provider 是否已註冊
        
        Args:
            provider: Provider 名稱
        
        Returns:
            是否已註冊
        """
        return provider in cls._registry
    
    @classmethod
    def unregister(cls, provider: str):
        """
        移除 provider 註冊
        
        Args:
            provider: Provider 名稱
        """
        if provider in cls._registry:
            del cls._registry[provider]
            print(f"✅ 已移除 provider: {provider}")
        else:
            print(f"⚠️  Provider 不存在: {provider}")
    
    @classmethod
    def get_info(cls, provider: str) -> Dict[str, str]:
        """
        取得 provider 資訊
        
        Args:
            provider: Provider 名稱
        
        Returns:
            Provider 資訊字典
        """
        if provider not in cls._registry:
            return {"error": f"Provider '{provider}' 不存在"}
        
        model_class = cls._registry[provider]
        return {
            "provider": provider,
            "class_name": model_class.__name__,
            "module": model_class.__module__,
            "doc": model_class.__doc__ or "無文檔"
        }
