"""
FastAPI 主應用程式
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import sys
from pathlib import Path
from dotenv import load_dotenv

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 載入環境變數
load_dotenv(project_root / ".env")

from backend.api import config, test, models, results
from backend.services.state_manager import StateManager
from src.utils.logger import setup_logger

logger = setup_logger("api", log_level="INFO", log_file="api.log")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """應用程式生命週期管理"""
    logger.info("🚀 API 伺服器啟動中...")
    
    # 初始化全域狀態管理器
    app.state.state_manager = StateManager()
    
    logger.info("✅ API 伺服器已就緒")
    yield
    
    logger.info("🛑 API 伺服器關閉中...")


# 創建 FastAPI 應用
app = FastAPI(
    title="AI Safety Auditing API",
    description="用於評估大型語言模型安全性的 Red Team 測試 API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 設定（允許前端跨域請求）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生產環境應改為特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 註冊路由
app.include_router(config.router, prefix="/api/config", tags=["配置管理"])
app.include_router(models.router, prefix="/api/models", tags=["模型管理"])
app.include_router(test.router, prefix="/api/test", tags=["測試執行"])
app.include_router(results.router, prefix="/api/results", tags=["結果查詢"])


@app.get("/")
async def root():
    """根路徑"""
    return {
        "message": "AI Safety Auditing API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """健康檢查"""
    return {
        "status": "healthy",
        "service": "ai-safety-auditing-api"
    }


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 開發模式自動重載
        log_level="info"
    )
