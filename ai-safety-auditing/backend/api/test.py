"""
測試執行 API
"""

from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from typing import Optional
import asyncio

from backend.models import (
    GenerateAttacksRequest,
    GenerateAttacksResponse,
    RunTestRequest,
    TestProgress
)

router = APIRouter()


@router.post("/generate-attacks", response_model=GenerateAttacksResponse)
async def generate_attacks(request: Request, data: GenerateAttacksRequest):
    """生成攻擊提示詞"""
    state_manager = request.app.state.state_manager
    
    try:
        # 初始化 Generator（如果需要）
        state_manager.initialize_generator()
        
        # 生成攻擊
        attacks = state_manager.generator.generate_attacks(
            category=data.category.value,
            count=data.count,
            use_llm=data.use_llm
        )
        
        # 儲存到緩存
        state_manager.attacks_cache = attacks
        
        return GenerateAttacksResponse(
            success=True,
            attacks=attacks,
            total=len(attacks),
            message=f"成功生成 {len(attacks)} 個攻擊"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成攻擊失敗: {str(e)}")


@router.get("/attacks")
async def get_cached_attacks(request: Request):
    """取得緩存的攻擊"""
    state_manager = request.app.state.state_manager
    
    return {
        "attacks": state_manager.attacks_cache,
        "total": len(state_manager.attacks_cache)
    }


async def run_test_async(
    state_manager,
    test_id: str,
    attacks,
    models_to_test
):
    """背景執行測試"""
    try:
        state_manager.active_tests[test_id]["status"] = "running"
        
        # 初始化 Judge
        state_manager.initialize_judge()
        
        results = []
        
        for model in models_to_test:
            for attack in attacks:
                try:
                    # 呼叫模型
                    response = model.generate_with_retry(attack["prompt"])
                    
                    # Judge 評分
                    if response.get("success"):
                        evaluation = state_manager.judge.evaluate(
                            attack["prompt"],
                            response.get("response", "")
                        )
                    else:
                        evaluation = {
                            "score": None,
                            "is_safe": None,
                            "reasoning": f"模型呼叫失敗: {response.get('error')}",
                            "error": response.get("error")
                        }
                    
                    # 記錄結果
                    result = {
                        "model": model.model_name,
                        "attack_id": attack["id"],
                        "attack_category": attack["category"],
                        "attack_prompt": attack["prompt"],
                        "model_response": response.get("response"),
                        "evaluation": evaluation,
                        "success": response.get("success", False)
                    }
                    
                    results.append(result)
                    
                    # 更新進度
                    state_manager.update_test_progress(test_id)
                
                except Exception as e:
                    # 記錄錯誤但繼續
                    results.append({
                        "model": model.model_name,
                        "attack_id": attack["id"],
                        "error": str(e)
                    })
                    state_manager.update_test_progress(test_id)
        
        # 完成測試
        state_manager.complete_test(test_id, results)
    
    except Exception as e:
        state_manager.active_tests[test_id]["status"] = "failed"
        state_manager.active_tests[test_id]["error"] = str(e)


@router.post("/run")
async def run_test(
    request: Request,
    data: RunTestRequest,
    background_tasks: BackgroundTasks
):
    """執行測試"""
    state_manager = request.app.state.state_manager
    
    # 確認有模型可測試
    if not state_manager.target_models:
        raise HTTPException(status_code=400, detail="尚未載入任何模型")
    
    # 取得攻擊列表
    attacks = data.attacks if data.attacks else state_manager.attacks_cache
    
    if not attacks:
        raise HTTPException(status_code=400, detail="沒有可用的攻擊提示詞")
    
    # 選擇模型
    if data.model_names:
        models_to_test = [
            m for m in state_manager.target_models 
            if m.model_name in data.model_names
        ]
    else:
        models_to_test = state_manager.target_models
    
    if not models_to_test:
        raise HTTPException(status_code=400, detail="找不到指定的模型")
    
    # 創建測試
    test_id = state_manager.create_test(attacks, data.model_names)
    
    # 在背景執行測試
    background_tasks.add_task(
        run_test_async,
        state_manager,
        test_id,
        attacks,
        models_to_test
    )
    
    return {
        "test_id": test_id,
        "message": "測試已開始",
        "total_tests": len(attacks) * len(models_to_test)
    }


@router.get("/status/{test_id}", response_model=TestProgress)
async def get_test_status(request: Request, test_id: str):
    """取得測試狀態"""
    state_manager = request.app.state.state_manager
    
    status = state_manager.get_test_status(test_id)
    
    if not status:
        raise HTTPException(status_code=404, detail="測試不存在")
    
    return status


@router.get("/list")
async def list_tests(request: Request):
    """列出所有測試"""
    state_manager = request.app.state.state_manager
    
    tests = state_manager.list_all_tests()
    
    return {
        "tests": tests,
        "total": len(tests)
    }
