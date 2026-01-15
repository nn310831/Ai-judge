"""
Pydantic 資料模型
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum


class AttackCategory(str, Enum):
    """攻擊類別"""
    prompt_injection = "prompt_injection"
    jailbreak = "jailbreak"
    roleplay = "roleplay"
    scenario = "scenario"
    encoding = "encoding"
    multilingual = "multilingual"
    all = "all"


class GenerateAttacksRequest(BaseModel):
    """生成攻擊請求"""
    category: AttackCategory = Field(default=AttackCategory.all, description="攻擊類別")
    count: int = Field(default=10, ge=1, le=100, description="生成數量")
    use_llm: bool = Field(default=False, description="是否使用 LLM 生成")


class GenerateAttacksResponse(BaseModel):
    """生成攻擊回應"""
    success: bool
    attacks: List[Dict[str, Any]]
    total: int
    message: Optional[str] = None


class ModelConfig(BaseModel):
    """模型配置（扁平格式）
    
    配置結構：
    {
        "provider": "openai",
        "model_name": "gpt-4",
        "api_key": "sk-...",
        "temperature": 0.7,
        "max_tokens": 1000
    }
    """
    provider: str = Field(..., description="Provider 名稱")
    model_name: str = Field(..., description="模型名稱")
    api_key: Optional[str] = Field(None, description="API Key（可選）")
    temperature: float = Field(default=0.7, ge=0, le=2, description="溫度參數")
    max_tokens: int = Field(default=1000, ge=1, le=4000, description="最大 token 數")


class ModelsConfigRequest(BaseModel):
    """模型配置請求"""
    models: List[ModelConfig]


class RunTestRequest(BaseModel):
    """執行測試請求"""
    attacks: Optional[List[Dict[str, Any]]] = Field(None, description="攻擊列表（可選，使用已生成的）")
    model_names: Optional[List[str]] = Field(None, description="要測試的模型名稱列表（None = 全部）")


class TestProgress(BaseModel):
    """測試進度"""
    test_id: str
    status: str  # "pending", "running", "completed", "failed"
    progress: int  # 0-100
    current: int
    total: int
    message: Optional[str] = None
    start_time: Optional[str] = None  # 開始時間
    end_time: Optional[str] = None    # 結束時間


class TestResultSummary(BaseModel):
    """測試結果摘要"""
    test_id: str
    timestamp: str
    total_tests: int
    completed: int
    overall_asr: float
    overall_avg_score: float
    overall_refusal_rate: float
    models_tested: List[str]


class EvaluationMetrics(BaseModel):
    """評估指標"""
    asr: float
    average_score: float
    refusal_rate: float
    score_distribution: Dict[str, float]
    total_samples: int


class ModelComparisonResponse(BaseModel):
    """模型比較回應"""
    models: Dict[str, EvaluationMetrics]
    ranking_by_asr: List[tuple]
    ranking_by_avg_score: List[tuple]


class PluginInfo(BaseModel):
    """外掛資訊"""
    name: str
    file_path: str
    model_classes: List[str]
    registered_providers: List[str]
    is_loaded: bool


class LoadPluginRequest(BaseModel):
    """載入外掛請求"""
    file_path: str
    should_validate: bool = Field(default=True, description="是否驗證外掛")


class ConfigFileResponse(BaseModel):
    """配置檔回應"""
    exists: bool
    file_path: str
    models: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
