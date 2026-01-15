"""
模型工廠
根據配置創建模型實例
"""

from typing import Dict, Any, List
import os
import re
from src.target.base_model import BaseModel
from src.target.model_registry import ModelRegistry


class ModelFactory:
    """模型工廠"""
    
    @staticmethod
    def create(config: Dict[str, Any]) -> BaseModel:
        """
        根據配置創建模型實例
        
        支持兩種格式：
        1. 扁平格式（推薦）:
            {
                "provider": "openai",
                "model_name": "gpt-4",
                "api_key": "${OPENAI_API_KEY}",
                "temperature": 0.7,
                "max_tokens": 1000
            }
        
        2. 嵌套格式（向後兼容）:
            {
                "provider": "openai",
                "config": {
                    "model_name": "gpt-4",
                    "api_key": "${OPENAI_API_KEY}",
                    ...
                }
            }
        
        Returns:
            模型實例
        
        Raises:
            ValueError: 如果配置格式錯誤或 provider 未註冊
        """
        # 驗證配置格式
        if "provider" not in config:
            raise ValueError("配置缺少 'provider' 欄位")
        
        provider = config["provider"]
        
        # 判斷是扁平格式還是嵌套格式
        if "config" in config:
            # 嵌套格式：使用 config 內的配置
            model_config = config["config"]
        else:
            # 扁平格式：直接使用除了 provider 之外的所有欄位
            model_config = {k: v for k, v in config.items() if k != "provider"}
        
        # 解析環境變數
        resolved_config = ModelFactory._resolve_env_vars(model_config)
        
        # 從註冊器取得類別
        model_class = ModelRegistry.get(provider)
        
        # 創建實例
        try:
            model = model_class(**resolved_config)
            print(f"✅ 已創建模型: {provider} -> {model.model_name}")
            return model
        except Exception as e:
            raise ValueError(
                f"創建模型失敗: {provider}\n"
                f"錯誤: {e}"
            )
    
    @staticmethod
    def create_batch(configs: List[Dict[str, Any]]) -> List[BaseModel]:
        """
        批量創建模型
        
        Args:
            configs: 配置列表
        
        Returns:
            模型實例列表
        """
        models = []
        errors = []
        
        for i, config in enumerate(configs):
            try:
                model = ModelFactory.create(config)
                models.append(model)
            except Exception as e:
                error_msg = f"配置 {i+1} 失敗: {e}"
                errors.append(error_msg)
                print(f"❌ {error_msg}")
        
        if errors:
            print(f"\n⚠️  {len(errors)} 個模型創建失敗")
        
        return models
    
    @staticmethod
    def _resolve_env_vars(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析配置中的環境變數
        
        支援格式：
        - ${VAR_NAME}：從環境變數讀取
        - $VAR_NAME：從環境變數讀取
        
        Args:
            config: 原始配置
        
        Returns:
            解析後的配置
        """
        resolved = {}
        
        for key, value in config.items():
            if isinstance(value, str):
                # 解析 ${VAR_NAME} 格式
                resolved[key] = ModelFactory._substitute_env_var(value)
            elif isinstance(value, dict):
                # 遞迴解析嵌套字典
                resolved[key] = ModelFactory._resolve_env_vars(value)
            else:
                resolved[key] = value
        
        return resolved
    
    @staticmethod
    def _substitute_env_var(value: str) -> str:
        """
        替換字串中的環境變數
        
        Args:
            value: 可能包含環境變數的字串
        
        Returns:
            替換後的字串
        """
        # 匹配 ${VAR_NAME} 或 $VAR_NAME
        pattern = r'\$\{([A-Z_][A-Z0-9_]*)\}|\$([A-Z_][A-Z0-9_]*)'
        
        def replacer(match):
            var_name = match.group(1) or match.group(2)
            env_value = os.getenv(var_name)
            
            if env_value is None:
                print(f"⚠️  環境變數未設定: {var_name}")
                return match.group(0)  # 保留原始字串
            
            return env_value
        
        return re.sub(pattern, replacer, value)
    
    @staticmethod
    def validate_config(config: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        驗證配置格式（支持扁平和嵌套格式）
        
        Args:
            config: 配置字典
        
        Returns:
            (是否有效, 錯誤訊息列表)
        """
        errors = []
        
        # 檢查必要欄位
        if "provider" not in config:
            errors.append("缺少 'provider' 欄位")
        elif not ModelRegistry.is_registered(config["provider"]):
            errors.append(f"未註冊的 provider: {config['provider']}")
        
        # 判斷格式並檢查 model_name
        if "config" in config:
            # 嵌套格式
            if not isinstance(config["config"], dict):
                errors.append("'config' 必須是字典")
            elif "model_name" not in config["config"]:
                errors.append("config 中缺少 'model_name' 欄位")
        else:
            # 扁平格式
            if "model_name" not in config:
                errors.append("缺少 'model_name' 欄位")
        
        return (len(errors) == 0, errors)
