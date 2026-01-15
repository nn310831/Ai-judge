"""
配置管理 API
"""

from fastapi import APIRouter, HTTPException, Request
from typing import List
import json
from pathlib import Path

from backend.models import (
    ConfigFileResponse,
    ModelsConfigRequest,
    ModelConfig
)

router = APIRouter()


@router.get("/", response_model=ConfigFileResponse)
async def get_config():
    """取得當前配置
    
    讀取 config/models_config.json 並返回內容
    返回扁平格式的模型配置列表
    """
    config_path = Path("config/models_config.json")
    
    if not config_path.exists():
        return ConfigFileResponse(
            exists=False,
            file_path=str(config_path),
            error="配置檔不存在"
        )
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        return ConfigFileResponse(
            exists=True,
            file_path=str(config_path),
            models=config.get("models", [])
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"讀取配置失敗: {str(e)}")


@router.post("/")
async def update_config(request: ModelsConfigRequest):
    """更新配置檔
    
    將前端提交的模型配置寫入 config/models_config.json
    配置採用扁平格式，每個模型包含 provider、model_name、api_key 等欄位
    """
    config_path = Path("config/models_config.json")
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        config_data = {
            "models": [model.dict() for model in request.models]
        }
        
        # 備份舊配置
        if config_path.exists():
            backup_path = config_path.with_suffix('.json.backup')
            import shutil
            shutil.copy(config_path, backup_path)
        
        # 寫入新配置
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "message": f"配置已更新，包含 {len(request.models)} 個模型"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新配置失敗: {str(e)}")


@router.get("/example")
async def get_example_config():
    """取得範例配置
    
    讀取 config/models_config.example.json
    返回扁平格式的模型配置範例
    """
    example_path = Path("config/models_config.example.json")
    
    if not example_path.exists():
        raise HTTPException(status_code=404, detail="範例配置檔不存在")
    
    try:
        with open(example_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        return config
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"讀取範例配置失敗: {str(e)}")


@router.post("/load")
async def load_config(request: Request):
    """載入配置並初始化模型
    
    從 config/models_config.json 讀取配置，使用 ModelFactory 創建模型實例
    支持扁平和嵌套兩種格式（建議使用扁平格式）
    """
    state_manager = request.app.state.state_manager
    
    try:
        models = state_manager.load_models_from_config()
        
        return {
            "success": True,
            "message": f"已載入 {len(models)} 個模型",
            "models": [
                {
                    "provider": m.provider if hasattr(m, 'provider') else "unknown",
                    "model_name": m.model_name
                }
                for m in models
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"載入配置失敗: {str(e)}")
