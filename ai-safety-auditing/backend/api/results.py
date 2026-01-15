"""
結果查詢 API
"""

from fastapi import APIRouter, HTTPException, Request
from typing import Optional

from src.evaluation.metrics import MetricsCalculator
from src.evaluation.statistical_tests import StatisticalTests

router = APIRouter()


@router.get("/{test_id}")
async def get_test_results(request: Request, test_id: str):
    """取得測試結果"""
    state_manager = request.app.state.state_manager
    
    test = state_manager.get_test_results(test_id)
    
    if not test:
        raise HTTPException(status_code=404, detail="測試不存在")
    
    return test


@router.get("/{test_id}/metrics")
async def get_test_metrics(request: Request, test_id: str):
    """取得測試指標"""
    state_manager = request.app.state.state_manager
    
    test = state_manager.get_test_results(test_id)
    
    if not test:
        raise HTTPException(status_code=404, detail="測試不存在")
    
    if test["status"] != "completed":
        raise HTTPException(status_code=400, detail="測試尚未完成")
    
    results = test["results"]
    
    # 整體指標
    evaluations = [r["evaluation"] for r in results if "evaluation" in r]
    overall_metrics = MetricsCalculator.calculate_all_metrics(evaluations)
    
    # 按模型分組
    results_by_model = {}
    for result in results:
        model_name = result["model"]
        if model_name not in results_by_model:
            results_by_model[model_name] = []
        if "evaluation" in result:
            results_by_model[model_name].append(result["evaluation"])
    
    model_metrics = {
        model: MetricsCalculator.calculate_all_metrics(evals)
        for model, evals in results_by_model.items()
    }
    
    # 按類別分組
    results_by_category = {}
    for result in results:
        if "attack_category" in result:
            category = result["attack_category"]
            if category not in results_by_category:
                results_by_category[category] = []
            if "evaluation" in result:
                results_by_category[category].append(result["evaluation"])
    
    category_metrics = {
        category: MetricsCalculator.calculate_all_metrics(evals)
        for category, evals in results_by_category.items()
    }
    
    return {
        "test_id": test_id,
        "overall": overall_metrics,
        "by_model": model_metrics,
        "by_category": category_metrics
    }


@router.get("/{test_id}/comparison")
async def compare_models(request: Request, test_id: str):
    """模型比較"""
    state_manager = request.app.state.state_manager
    
    test = state_manager.get_test_results(test_id)
    
    if not test:
        raise HTTPException(status_code=404, detail="測試不存在")
    
    if test["status"] != "completed":
        raise HTTPException(status_code=400, detail="測試尚未完成")
    
    results = test["results"]
    
    # 按模型分組
    results_by_model = {}
    for result in results:
        model_name = result["model"]
        if model_name not in results_by_model:
            results_by_model[model_name] = []
        if "evaluation" in result:
            results_by_model[model_name].append(result["evaluation"])
    
    # 使用 MetricsCalculator 比較
    comparison = MetricsCalculator.compare_models(results_by_model)
    
    return comparison


@router.post("/{test_id}/statistical-test")
async def run_statistical_test(
    request: Request,
    test_id: str,
    model_a: str,
    model_b: str,
    test_type: str = "t_test"
):
    """執行統計檢定"""
    state_manager = request.app.state.state_manager
    
    test = state_manager.get_test_results(test_id)
    
    if not test:
        raise HTTPException(status_code=404, detail="測試不存在")
    
    if test["status"] != "completed":
        raise HTTPException(status_code=400, detail="測試尚未完成")
    
    results = test["results"]
    
    # 提取分數
    scores_a = [
        r["evaluation"]["score"]
        for r in results
        if r["model"] == model_a and "evaluation" in r and r["evaluation"].get("score") is not None
    ]
    
    scores_b = [
        r["evaluation"]["score"]
        for r in results
        if r["model"] == model_b and "evaluation" in r and r["evaluation"].get("score") is not None
    ]
    
    if not scores_a or not scores_b:
        raise HTTPException(status_code=400, detail="找不到足夠的分數資料")
    
    # 執行統計檢定
    if test_type == "t_test":
        result = StatisticalTests.independent_t_test(scores_a, scores_b)
    elif test_type == "mann_whitney":
        result = StatisticalTests.mann_whitney_u_test(scores_a, scores_b)
    else:
        raise HTTPException(status_code=400, detail="不支援的檢定類型")
    
    return result


@router.get("/{test_id}/export")
async def export_results(
    request: Request,
    test_id: str,
    format: str = "json"
):
    """匯出結果"""
    state_manager = request.app.state.state_manager
    
    test = state_manager.get_test_results(test_id)
    
    if not test:
        raise HTTPException(status_code=404, detail="測試不存在")
    
    if format == "json":
        return test
    
    elif format == "csv":
        from src.utils import DataHandler
        from pathlib import Path
        import tempfile
        from fastapi.responses import FileResponse
        
        # 扁平化資料
        flat_results = DataHandler.flatten_results_for_csv(test["results"])
        
        # 儲存到臨時檔案
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        DataHandler.export_to_csv(flat_results, temp_file.name)
        
        return FileResponse(
            temp_file.name,
            media_type="text/csv",
            filename=f"test_results_{test_id}.csv"
        )
    
    else:
        raise HTTPException(status_code=400, detail="不支援的匯出格式")
