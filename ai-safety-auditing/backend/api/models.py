"""
模型管理 API
"""

from fastapi import APIRouter, HTTPException, Request
from typing import List

from backend.models import PluginInfo, LoadPluginRequest

router = APIRouter()


@router.get("/providers")
async def get_providers(request: Request):
    """取得所有可用的 provider"""
    state_manager = request.app.state.state_manager
    
    providers = state_manager.get_available_providers()
    
    return {
        "providers": providers,
        "total": len(providers)
    }


@router.get("/loaded")
async def get_loaded_models(request: Request):
    """取得已載入的模型"""
    state_manager = request.app.state.state_manager
    
    models = state_manager.target_models
    
    return {
        "models": [
            {
                "provider": getattr(m, 'provider', 'unknown'),
                "model_name": m.model_name,
                "temperature": m.temperature,
                "max_tokens": m.max_tokens
            }
            for m in models
        ],
        "total": len(models)
    }


@router.get("/plugins")
async def get_plugins(request: Request):
    """取得已載入的外掛"""
    state_manager = request.app.state.state_manager
    
    plugins = state_manager.get_loaded_plugins()
    
    return {
        "plugins": plugins,
        "total": len(plugins)
    }


@router.post("/plugins/load")
async def load_plugin(request: Request, data: LoadPluginRequest):
    """載入外掛"""
    state_manager = request.app.state.state_manager
    
    try:
        result = state_manager.plugin_loader.load_plugin(
            data.file_path,
            validate=data.should_validate
        )
        
        if result["success"]:
            return {
                "success": True,
                "message": f"外掛已載入",
                "plugin_info": result
            }
        else:
            raise HTTPException(status_code=400, detail=result.get("error", "載入失敗"))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"載入外掛失敗: {str(e)}")


@router.post("/plugins/load-all")
async def load_all_plugins(request: Request):
    """載入所有外掛"""
    state_manager = request.app.state.state_manager
    
    try:
        result = state_manager.load_plugins()
        
        return {
            "success": True,
            "total": result["total"],
            "loaded": result["loaded"],
            "failed": result["failed"],
            "plugins": result["plugins"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"載入外掛失敗: {str(e)}")
