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
                "model_name": getattr(m, 'model_name', 'unknown'),
                "temperature": getattr(m, 'temperature', 0.7),
                "max_tokens": getattr(m, 'max_tokens', 1000)
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


@router.post("/upload-provider")
async def upload_provider(request: Request):
    """接收並儲存自定義 Provider 程式碼"""
    import os
    import subprocess
    import sys
    from pathlib import Path
    
    # 套件白名單（只允許這些套件）
    ALLOWED_PACKAGES = {
        "google-generativeai",
        "anthropic",
        "openai",
        "httpx",
        "requests",
        "aiohttp",
        "pydantic",
        "typing-extensions",
        "python-dotenv"
    }
    
    try:
        data = await request.json()
        file_name = data.get("file_name", "")
        code = data.get("code", "")
        dependencies = data.get("dependencies", [])
        
        if not file_name or not code:
            raise HTTPException(status_code=400, detail="檔案名稱和程式碼不能為空")
        
        if not file_name.endswith(".py"):
            file_name += ".py"
        
        # 檢查依賴是否在白名單中
        install_messages = []
        if dependencies:
            for dep in dependencies:
                dep_name = dep.strip()
                if dep_name:
                    if dep_name not in ALLOWED_PACKAGES:
                        raise HTTPException(
                            status_code=403, 
                            detail=f"套件 '{dep_name}' 不在允許清單中。允許的套件：{', '.join(sorted(ALLOWED_PACKAGES))}"
                        )
                    try:
                        subprocess.check_call(
                            [sys.executable, "-m", "pip", "install", dep_name],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        install_messages.append(f"✓ 已安裝 {dep_name}")
                    except subprocess.CalledProcessError:
                        install_messages.append(f"✗ 安裝 {dep_name} 失敗")
        
        # 儲存到 plugins/ 目錄
        plugins_dir = Path("plugins")
        plugins_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = plugins_dir / file_name
        
        # 檢查檔案是否已存在
        if file_path.exists():
            raise HTTPException(status_code=400, detail=f"檔案 {file_name} 已存在")
        
        # 寫入檔案
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        
        # 嘗試重新載入外掛
        state_manager = request.app.state.state_manager
        try:
            # 強制重新掃描 plugins 目錄
            import importlib
            
            # 清除已載入的模組快取（清除 plugins 和 adapters 相關）
            modules_to_clear = [
                key for key in sys.modules.keys() 
                if 'plugins.' in key or 'src.target.adapters' in key
            ]
            for module_name in modules_to_clear:
                del sys.modules[module_name]
            
            # 重新載入外掛
            state_manager.load_plugins()
        except Exception as load_error:
            # 如果載入失敗，保留檔案但提示警告
            return {
                "success": True,
                "message": f"檔案已儲存至 {file_path}，但載入時出現警告: {str(load_error)}",
                "file_path": str(file_path),
                "warning": str(load_error)
            }
        
        message = f"Provider 已成功上傳並儲存至 plugins/{file_name}"
        if install_messages:
            message += "\n\n依賴安裝結果：\n" + "\n".join(install_messages)
        
        return {
            "success": True,
            "message": message,
            "file_path": str(file_path),
            "dependencies_installed": install_messages
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上傳失敗: {str(e)}")
