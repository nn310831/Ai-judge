"""
全域狀態管理器
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
import asyncio
from pathlib import Path

from src.generator import AttackGenerator
from src.target import ModelRegistry
from src.target.config_manager import ConfigManager
from src.target.plugin_loader import PluginLoader
from src.judge import SafetyJudge
from src.evaluation.metrics import MetricsCalculator
from src.utils.logger import setup_logger

logger = setup_logger("state_manager")


class StateManager:
    """全域狀態管理器"""
    
    def __init__(self):
        """初始化狀態管理器"""
        self.generator = None
        self.judge = None
        self.target_models = []
        self.plugin_loader = PluginLoader()
        
        # 測試狀態
        self.active_tests: Dict[str, Dict[str, Any]] = {}
        self.test_results: Dict[str, Dict[str, Any]] = {}
        
        # 攻擊緩存
        self.attacks_cache: List[Dict[str, Any]] = []
        
        logger.info("狀態管理器已初始化")
    
    def initialize_generator(self, model: str = None, api_key: str = None):
        """初始化攻擊生成器"""
        if self.generator is None:
            self.generator = AttackGenerator(model=model, api_key=api_key)
            logger.info(f"Generator 已初始化: {self.generator.model}")
    
    def initialize_judge(self, model: str = None, api_key: str = None):
        """初始化 Judge"""
        if self.judge is None:
            self.judge = SafetyJudge(model=model, api_key=api_key)
            logger.info(f"Judge 已初始化: {self.judge.model}")
    
    def load_models_from_config(self, config_path: str = "config/models_config.json") -> List[Any]:
        """從配置檔載入模型"""
        try:
            config_manager = ConfigManager(config_path)
            self.target_models = config_manager.load_and_create_models()
            logger.info(f"已載入 {len(self.target_models)} 個模型")
            return self.target_models
        except Exception as e:
            logger.error(f"載入模型失敗: {e}")
            raise
    
    def get_available_providers(self) -> List[str]:
        """取得可用的 provider"""
        return ModelRegistry.list_providers()
    
    def load_plugins(self) -> Dict[str, Any]:
        """載入所有外掛"""
        return self.plugin_loader.load_all_plugins()
    
    def get_loaded_plugins(self) -> List[Dict[str, Any]]:
        """取得已載入的外掛"""
        return self.plugin_loader.get_loaded_plugins()
    
    def create_test(self, attacks: List[Dict[str, Any]], model_names: Optional[List[str]] = None) -> str:
        """創建新測試"""
        test_id = str(uuid.uuid4())
        
        # 選擇要測試的模型
        if model_names:
            models_to_test = [m for m in self.target_models if m.model_name in model_names]
        else:
            models_to_test = self.target_models
        
        self.active_tests[test_id] = {
            "test_id": test_id,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "attacks": attacks,
            "models": [m.model_name for m in models_to_test],
            "total_tests": len(attacks) * len(models_to_test),
            "completed": 0,
            "results": []
        }
        
        logger.info(f"測試已創建: {test_id}, 共 {len(attacks)} 攻擊 x {len(models_to_test)} 模型")
        
        return test_id
    
    def get_test_status(self, test_id: str) -> Optional[Dict[str, Any]]:
        """取得測試狀態"""
        test = self.active_tests.get(test_id)
        
        if test:
            total = test["total_tests"]
            completed = test["completed"]
            progress = int((completed / total * 100)) if total > 0 else 0
            
            return {
                "test_id": test_id,
                "status": test["status"],
                "progress": progress,
                "current": completed,
                "total": total,
                "message": f"已完成 {completed}/{total} 個測試",
                "start_time": test.get("created_at"),
                "end_time": test.get("completed_at")
            }
        
        return None
    
    def update_test_progress(self, test_id: str, increment: int = 1):
        """更新測試進度"""
        if test_id in self.active_tests:
            self.active_tests[test_id]["completed"] += increment
    
    def complete_test(self, test_id: str, results: List[Dict[str, Any]]):
        """完成測試"""
        if test_id in self.active_tests:
            test = self.active_tests[test_id]
            test["status"] = "completed"
            test["completed_at"] = datetime.now().isoformat()
            test["results"] = results
            
            # 移到結果存儲
            self.test_results[test_id] = test
            
            logger.info(f"測試完成: {test_id}")
    
    def get_test_results(self, test_id: str) -> Optional[Dict[str, Any]]:
        """取得測試結果"""
        return self.test_results.get(test_id) or self.active_tests.get(test_id)
    
    def list_all_tests(self) -> List[Dict[str, Any]]:
        """列出所有測試"""
        all_tests = []
        
        for test_id in list(self.test_results.keys()) + list(self.active_tests.keys()):
            test = self.test_results.get(test_id) or self.active_tests.get(test_id)
            if test:
                total = test["total_tests"]
                completed = test["completed"]
                progress = int((completed / total * 100)) if total > 0 else 0
                
                all_tests.append({
                    "test_id": test_id,
                    "status": test["status"],
                    "progress": progress,
                    "current": completed,
                    "total": total,
                    "message": f"已完成 {completed}/{total} 個測試",
                    "start_time": test.get("created_at"),
                    "end_time": test.get("completed_at")
                })
        
        return all_tests
