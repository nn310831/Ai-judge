"""
配置管理器
整合配置載入、驗證和模型創建
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from src.target.base_model import BaseModel
from src.target.model_factory import ModelFactory
from src.target.model_registry import ModelRegistry


class ConfigManager:
    """配置管理器
    
    支持的配置格式（扁平結構）：
    {
        "models": [
            {
                "provider": "openai",
                "model_name": "gpt-4",
                "api_key": "${OPENAI_API_KEY}",
                "temperature": 0.7,
                "max_tokens": 1000
            }
        ]
    }
    """
    
    def __init__(self, config_path: str = "config/models_config.json"):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置檔路徑（預設: config/models_config.json）
        """
        self.config_path = Path(config_path)
        self.config_data = None
        self.models: List[BaseModel] = []
    
    def load_and_create_models(self) -> List[BaseModel]:
        """
        載入配置並創建所有模型
        
        Returns:
            模型實例列表
        """
        print("=" * 60)
        print("🚀 配置管理器 - 模型工廠")
        print("=" * 60)
        
        # 1. 載入配置檔
        self._load_config()
        
        # 2. 顯示可用的 providers
        self._show_available_providers()
        
        # 3. 使用工廠批量創建模型
        configs = self.config_data.get("models", [])
        self.models = ModelFactory.create_batch(configs)
        
        print(f"\n✅ 成功創建 {len(self.models)} 個模型\n")
        
        return self.models
    
    def _load_config(self):
        """載入配置檔"""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"找不到配置檔: {self.config_path}\n"
                f"請參考 config/models_config.example.json 建立配置檔"
            )
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config_data = json.load(f)
        
        print(f"📁 已載入配置檔: {self.config_path}")
    
    def _show_available_providers(self):
        """顯示已註冊的 providers"""
        providers = ModelRegistry.list_providers()
        print(f"\n📋 可用的 providers ({len(providers)}):")
        for provider in providers:
            model_class = ModelRegistry.get(provider)
            print(f"   - {provider}: {model_class.__name__}")
    
    def get_model_by_name(self, name: str) -> BaseModel:
        """根據名稱取得模型"""
        for model in self.models:
            if model.model_name == name:
                return model
        
        raise ValueError(f"找不到模型: {name}")
    
    def list_models(self) -> List[str]:
        """列出所有模型名稱"""
        return [model.model_name for model in self.models]
    
    def save_config(self, config_data: Dict[str, Any]):
        """儲存配置到檔案"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 配置已儲存至: {self.config_path}")
