"""
外掛載入器：動態載入自訂模型適配器
"""

import importlib.util
import inspect
import sys
from pathlib import Path
from typing import Dict, List, Optional, Type, Any

from src.target.base_model import BaseModel
from src.target.model_registry import ModelRegistry
from src.utils.logger import setup_logger


logger = setup_logger("plugin_loader")


class PluginValidator:
    """外掛驗證器：檢查外掛是否符合規範"""
    
    @staticmethod
    def validate_model_class(cls: Type) -> tuple[bool, Optional[str]]:
        """
        驗證模型類別是否符合規範
        
        Args:
            cls: 要驗證的類別
        
        Returns:
            (是否有效, 錯誤訊息)
        """
        # 1. 必須繼承 BaseModel
        if not issubclass(cls, BaseModel):
            return False, f"{cls.__name__} 必須繼承 BaseModel"
        
        # 2. 不能是抽象類別
        if inspect.isabstract(cls):
            return False, f"{cls.__name__} 不能是抽象類別"
        
        # 3. 必須實作 _call_api 方法
        if not hasattr(cls, '_call_api') or cls._call_api is BaseModel._call_api:
            return False, f"{cls.__name__} 必須實作 _call_api 方法"
        
        # 4. 必須有 __init__ 方法且接受 api_key 參數
        init_signature = inspect.signature(cls.__init__)
        if 'api_key' not in init_signature.parameters:
            return False, f"{cls.__name__}.__init__ 必須包含 api_key 參數"
        
        return True, None
    
    @staticmethod
    def validate_plugin_file(file_path: Path) -> tuple[bool, Optional[str]]:
        """
        驗證外掛檔案
        
        Args:
            file_path: 外掛檔案路徑
        
        Returns:
            (是否有效, 錯誤訊息)
        """
        # 1. 檔案必須存在
        if not file_path.exists():
            return False, f"檔案不存在: {file_path}"
        
        # 2. 必須是 Python 檔案
        if file_path.suffix != '.py':
            return False, f"必須是 .py 檔案: {file_path}"
        
        # 3. 檢查檔案大小（防止過大）
        if file_path.stat().st_size > 1024 * 1024:  # 1MB
            return False, f"檔案過大（超過 1MB）: {file_path}"
        
        return True, None
    
    @staticmethod
    def check_dangerous_imports(code: str) -> tuple[bool, List[str]]:
        """
        檢查程式碼中是否有危險的 import
        
        Args:
            code: 程式碼內容
        
        Returns:
            (是否安全, 危險 import 列表)
        """
        dangerous_imports = []
        dangerous_modules = {
            'os.system', 'subprocess', 'eval', 'exec',
            '__import__', 'compile', 'open',
            'pickle', 'shelve', 'marshal'
        }
        
        lines = code.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                for dangerous in dangerous_modules:
                    if dangerous in line:
                        dangerous_imports.append(line)
        
        is_safe = len(dangerous_imports) == 0
        return is_safe, dangerous_imports


class PluginLoader:
    """外掛載入器：載入並註冊自訂模型"""
    
    def __init__(self, plugin_dir: str = "plugins"):
        """
        初始化外掛載入器
        
        Args:
            plugin_dir: 外掛目錄路徑
        """
        self.plugin_dir = Path(plugin_dir)
        self.plugin_dir.mkdir(parents=True, exist_ok=True)
        
        self.loaded_plugins: Dict[str, Dict[str, Any]] = {}
        self.validator = PluginValidator()
        
        logger.info(f"外掛載入器已初始化，外掛目錄: {self.plugin_dir}")
    
    def load_plugin(
        self,
        file_path: str,
        validate: bool = True,
        auto_register: bool = True
    ) -> Dict[str, Any]:
        """
        載入單個外掛
        
        Args:
            file_path: 外掛檔案路徑
            validate: 是否驗證外掛
            auto_register: 是否自動註冊到 ModelRegistry
        
        Returns:
            載入結果字典
        """
        plugin_path = Path(file_path)
        
        logger.info(f"正在載入外掛: {plugin_path}")
        
        # 驗證檔案
        if validate:
            is_valid, error = self.validator.validate_plugin_file(plugin_path)
            if not is_valid:
                logger.error(f"外掛驗證失敗: {error}")
                return {"success": False, "error": error}
            
            # 檢查危險 import
            with open(plugin_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            is_safe, dangerous = self.validator.check_dangerous_imports(code)
            if not is_safe:
                error = f"偵測到危險的 import: {dangerous}"
                logger.error(f"安全檢查失敗: {error}")
                return {"success": False, "error": error}
        
        # 動態載入模組
        try:
            module_name = plugin_path.stem
            spec = importlib.util.spec_from_file_location(module_name, plugin_path)
            
            if spec is None or spec.loader is None:
                return {"success": False, "error": "無法載入模組規範"}
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            logger.info(f"模組已載入: {module_name}")
        
        except Exception as e:
            logger.error(f"載入模組失敗: {e}")
            return {"success": False, "error": str(e)}
        
        # 尋找 BaseModel 的子類別
        model_classes = []
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, BaseModel) and obj is not BaseModel:
                # 驗證模型類別
                if validate:
                    is_valid, error = self.validator.validate_model_class(obj)
                    if not is_valid:
                        logger.warning(f"模型類別 {name} 驗證失敗: {error}")
                        continue
                
                model_classes.append((name, obj))
                logger.info(f"發現模型類別: {name}")
        
        if not model_classes:
            return {"success": False, "error": "外掛中沒有找到有效的模型類別"}
        
        # 自動註冊
        registered = []
        if auto_register:
            for name, cls in model_classes:
                try:
                    provider_name = getattr(cls, 'provider', name.lower())
                    ModelRegistry.register(provider_name, cls)
                    registered.append(provider_name)
                    logger.info(f"已註冊模型: {provider_name}")
                except Exception as e:
                    logger.error(f"註冊模型 {name} 失敗: {e}")
        
        # 儲存外掛資訊
        plugin_info = {
            "file_path": str(plugin_path),
            "module_name": module_name,
            "model_classes": [name for name, _ in model_classes],
            "registered_providers": registered,
            "success": True
        }
        
        self.loaded_plugins[module_name] = plugin_info
        
        return plugin_info
    
    def load_all_plugins(
        self,
        validate: bool = True,
        auto_register: bool = True
    ) -> Dict[str, Any]:
        """
        載入目錄中的所有外掛
        
        Args:
            validate: 是否驗證外掛
            auto_register: 是否自動註冊
        
        Returns:
            載入結果摘要
        """
        logger.info(f"正在掃描外掛目錄: {self.plugin_dir}")
        
        plugin_files = list(self.plugin_dir.glob("*.py"))
        
        if not plugin_files:
            logger.warning(f"外掛目錄中沒有找到 .py 檔案")
            return {
                "success": True,
                "total": 0,
                "loaded": 0,
                "failed": 0,
                "plugins": []
            }
        
        results = {
            "success": True,
            "total": len(plugin_files),
            "loaded": 0,
            "failed": 0,
            "plugins": []
        }
        
        for plugin_file in plugin_files:
            result = self.load_plugin(
                str(plugin_file),
                validate=validate,
                auto_register=auto_register
            )
            
            if result["success"]:
                results["loaded"] += 1
            else:
                results["failed"] += 1
            
            results["plugins"].append({
                "file": plugin_file.name,
                "result": result
            })
        
        logger.info(
            f"外掛載入完成: 總共 {results['total']}, "
            f"成功 {results['loaded']}, 失敗 {results['failed']}"
        )
        
        return results
    
    def unload_plugin(self, module_name: str) -> bool:
        """
        卸載外掛
        
        Args:
            module_name: 模組名稱
        
        Returns:
            是否成功卸載
        """
        if module_name not in self.loaded_plugins:
            logger.warning(f"外掛不存在: {module_name}")
            return False
        
        plugin_info = self.loaded_plugins[module_name]
        
        # 取消註冊
        for provider in plugin_info.get("registered_providers", []):
            try:
                ModelRegistry.unregister(provider)
                logger.info(f"已取消註冊: {provider}")
            except Exception as e:
                logger.error(f"取消註冊失敗: {e}")
        
        # 從 sys.modules 移除
        if module_name in sys.modules:
            del sys.modules[module_name]
        
        # 從載入列表移除
        del self.loaded_plugins[module_name]
        
        logger.info(f"外掛已卸載: {module_name}")
        return True
    
    def get_loaded_plugins(self) -> List[Dict[str, Any]]:
        """
        取得所有已載入的外掛資訊
        
        Returns:
            外掛資訊列表
        """
        return list(self.loaded_plugins.values())
    
    def reload_plugin(
        self,
        module_name: str,
        validate: bool = True
    ) -> Dict[str, Any]:
        """
        重新載入外掛（用於開發時）
        
        Args:
            module_name: 模組名稱
            validate: 是否驗證
        
        Returns:
            重新載入結果
        """
        if module_name not in self.loaded_plugins:
            return {"success": False, "error": "外掛未載入"}
        
        file_path = self.loaded_plugins[module_name]["file_path"]
        
        # 卸載
        self.unload_plugin(module_name)
        
        # 重新載入
        return self.load_plugin(file_path, validate=validate)
