# src/target/__init__.py
"""
目標模型模組（整合 ModelFactory）
"""

from src.target.base_model import BaseModel
from src.target.model_registry import ModelRegistry
from src.target.model_factory import ModelFactory
from src.target.config_manager import ConfigManager
from src.target.adapters.openai_model import OpenAIModel
from src.target.adapters.anthropic_model import AnthropicModel


def register_builtin_models():
    """註冊所有內建模型"""
    ModelRegistry.register("openai", OpenAIModel)
    ModelRegistry.register("anthropic", AnthropicModel)
    print("✅ 內建模型已註冊")


# 自動註冊
register_builtin_models()

__all__ = [
    'BaseModel',
    'ModelRegistry',
    'ModelFactory',
    'ConfigManager',
    'OpenAIModel',
    'AnthropicModel',
    'register_builtin_models'
]
