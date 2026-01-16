# 🛡️ AI Safety Auditing System

基於 LLM-as-a-Judge 的自動化 AI 責任與安全審計系統

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)](https://reactjs.org/)

---

## 📋 專題資訊

**標題**: Automated AI Responsibility & Safety Auditing System based on LLM-as-a-Judge

**研究動機**: 
- Grok AI 等爭議顯示廠商自律不足
- 需要第三方自動化審計工具
- 解決人工測試的覆蓋率、主觀性、工具缺失問題

**目標**: 建立一個自動化紅隊測試管線，評估大型語言模型（LLM）對倫理與安全標準的遵從性

---

## 🌟 核心功能

### 🎯 自動化紅隊測試
- **攻擊生成器 (Generator)**: 基於 LLM 自動生成多樣化的安全測試案例
- **目標模型測試 (Target)**: 支援多種 LLM Provider（OpenAI、Anthropic、Gemini 等）
- **智能評審系統 (Judge)**: 使用 LLM-as-a-Judge 自動評估模型回應的安全性

### 📊 全面的評估指標
- **ASR (Attack Success Rate)**: 攻擊成功率
- **Refusal Rate**: 模型拒絕率
- **Safety Score**: 安全評分 (1-5 級)
- **Precision/Recall**: 評審系統準確度
- **統計分析**: 自動生成詳細的測試報告

### 🎨 現代化 Web 界面
- **Dashboard**: 即時測試概覽與視覺化圖表
- **Testing**: 互動式測試執行與管理
- **Models**: 模型配置與管理
- **Provider 管理**: 上傳與管理自定義 Model Provider
- **Results**: 詳細的測試結果與統計分析
- **Settings**: 系統配置與 API Keys 管理

### 🔌 擴展性設計
- **Plugin 系統**: 支援自定義 Model Provider
- **安全白名單**: 僅允許安全的依賴套件
- **動態載入**: 自動發現並註冊新的 Provider

---

## 🏗️ 系統架構

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  攻擊生成器      │ ──→  │   目標 LLM      │ ──→  │   評審系統      │
│  (Generator)    │      │   (Target)      │      │   (Judge)       │
└─────────────────┘      └─────────────────┘      └─────────────────┘
        ↓                         ↓                         ↓
   攻擊提示詞庫              模型回應記錄              安全評分 (1-5)
                                                           ↓
                                              ┌─────────────────────┐
                                              │ 統計分析 & 視覺化   │
                                              │  • ASR              │
                                              │  • Refusal Rate     │
                                              │  • Safety Score     │
                                              └─────────────────────┘
```

### 技術棧

**後端**:
- FastAPI (Python 3.9+)
- Pydantic (數據驗證)
- OpenAI SDK, Anthropic SDK, Google Generative AI

**前端**:
- React 18 + TypeScript
- Vite (構建工具)
- Monaco Editor (代碼編輯器)
- Recharts (圖表庫)
- Lucide React (圖標)

---

## 🚀 快速開始

### 前置需求

- Python 3.9 或更高版本
- Node.js 16 或更高版本
- npm 或 yarn

### 1. 環境設定

```bash
# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows

# 安裝套件
pip install -r requirements.txt
```

### 2. 設定 API Keys

```bash
# 複製範例檔案
cp .env.example .env

# 編輯 .env，填入你的 API Keys
# OPENAI_API_KEY=sk-proj-...
# ANTHROPIC_API_KEY=sk-ant-...
# GEMINI_API_KEY=AIza...
```

### 3. 配置模型

```bash
# 複製並編輯模型配置檔案
cp config/models_config.example.json config/models_config.json

# 編輯 config/models_config.json，配置你要測試的模型
```

**配置格式範例**:

```json
{
  "models": [
    {
      "provider": "openai",
      "model_name": "gpt-4o-mini",
      "api_key": "${OPENAI_API_KEY}",
      "temperature": 0.0,
      "max_tokens": 1000
    },
    {
      "provider": "anthropic",
      "model_name": "claude-sonnet-4-20250514",
      "api_key": "${ANTHROPIC_API_KEY}",
      "temperature": 0.0,
      "max_tokens": 1000
    }
  ]
}
```

### 4. 啟動應用

#### 方式一：啟動 Web 界面（推薦）

**後端**:
```bash
python backend/main.py
```

**前端**（新終端）:
```bash
cd frontend
npm install
npm run dev
```

訪問 `http://localhost:5173` 開始使用

#### 方式二：命令行測試

```bash
# 執行完整測試流程
python main.py

# 或快速測試
python quick_start.py
```

---

## 📁 專案結構

```
ai-safety-auditing/
├── backend/                    # FastAPI 後端
│   ├── api/                   # API 路由
│   │   ├── config.py          # 配置管理 API
│   │   ├── models.py          # 模型管理 API
│   │   ├── test.py            # 測試執行 API
│   │   └── results.py         # 結果查詢 API
│   ├── services/              # 業務邏輯
│   │   └── state_manager.py  # 全域狀態管理
│   └── main.py                # FastAPI 應用入口
│
├── frontend/                   # React + TypeScript 前端
│   ├── src/
│   │   ├── api/               # API 客戶端
│   │   ├── components/        # 可複用組件
│   │   │   ├── Card/          # 卡片組件
│   │   │   ├── Button/        # 按鈕組件
│   │   │   └── Sidebar/       # 側邊欄導覽
│   │   ├── pages/             # 頁面組件
│   │   │   ├── Dashboard/     # 儀表板
│   │   │   ├── Testing/       # 測試頁面
│   │   │   ├── Models/        # 模型管理
│   │   │   ├── AddProvider/   # Provider 上傳
│   │   │   ├── Results/       # 結果查詢
│   │   │   └── Settings/      # 系統設定
│   │   ├── layouts/           # 布局組件
│   │   ├── types/             # TypeScript 類型定義
│   │   └── styles/            # 全域樣式
│   ├── package.json
│   └── vite.config.ts
│
├── src/                        # 核心測試引擎
│   ├── generator/             # 攻擊生成模組
│   │   ├── attack_generator.py
│   │   └── prompts.py         # 提示詞模板
│   ├── target/                # 目標模型介面
│   │   ├── base_model.py      # 基礎模型類別
│   │   ├── model_factory.py   # 模型工廠
│   │   ├── model_registry.py  # 模型註冊表
│   │   ├── plugin_loader.py   # 插件載入器
│   │   ├── config_manager.py  # 配置管理器
│   │   └── adapters/          # 內建 Provider 適配器
│   │       ├── openai_model.py
│   │       └── anthropic_model.py
│   ├── judge/                 # LLM-as-a-Judge 評審系統
│   │   └── safety_judge.py
│   ├── evaluation/            # 評估指標計算
│   │   └── metrics.py
│   └── utils/                 # 工具函式
│       └── logger.py
│
├── plugins/                    # 自定義 Provider 插件目錄
│   ├── gemini_model.py        # Gemini Provider 範例
│   └── ollama_adapter.py.example
│
├── config/                     # 配置檔案
│   ├── models_config.json     # 模型配置（不提交到 Git）
│   └── models_config.example.json
│
├── data/                       # 測試資料
│   ├── attacks/               # 攻擊案例
│   ├── responses/             # 模型回應
│   └── evaluations/           # 評估結果
│
├── logs/                       # 日誌檔案
├── .env                        # 環境變數（不提交到 Git）
├── .env.example                # 環境變數範例
├── requirements.txt            # Python 依賴
├── main.py                     # CLI 測試入口
└── README.md                   # 本文件
```

---

## 🔌 自定義 Provider 開發

### 測試 Provider 上傳功能

```bash
# 1. 複製範例 Provider
cp plugins/gemini_model.py plugins/my_test_provider.py

# 2. 刪除原始檔案（模擬需要上傳的情境）
rm plugins/gemini_model.py

# 3. 前往 Web 界面的 "Provider 管理" 頁面上傳
```

### 開發自定義 Provider

所有自定義 Provider 必須繼承 `BaseModel` 並實作必要方法：

```python
from src.target.base_model import BaseModel
from typing import Dict, Any

class MyCustomModel(BaseModel):
    """自定義模型適配器"""
    
    # 設定 Provider 名稱（用於註冊）
    provider = 'my_custom_provider'
    
    def __init__(
        self,
        model_name: str,
        api_key: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ):
        super().__init__(model_name=model_name, provider=self.provider)
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        # 初始化你的 API 客戶端
    
    def _call_api(self, prompt: str) -> Dict[str, Any]:
        """
        實作 API 呼叫邏輯
        
        Returns:
            {
                "response": str,      # 模型回應文本
                "model": str,         # 模型名稱
                "usage": dict,        # Token 使用量（可選）
                "finish_reason": str  # 完成原因（可選）
            }
        """
        # 實作你的 API 呼叫邏輯
        response = your_api_call(prompt)
        
        return {
            "response": response.text,
            "model": self.model_name,
            "usage": {},
            "finish_reason": "stop"
        }
```

### 允許的依賴套件

出於安全考慮，僅允許以下套件：

- `google-generativeai`
- `anthropic`
- `openai`
- `httpx`
- `requests`
- `aiohttp`
- `pydantic`
- `typing-extensions`
- `python-dotenv`

---
程式碼在 /backend/api/models.py

```python
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
```

## 🎯 核心指標說明

### ASR (Attack Success Rate)
**攻擊成功率** - 衡量模型被成功繞過安全機制的比例

```
ASR = (成功攻擊數 / 總攻擊數) × 100%
```

- **高 ASR**: 表示模型安全機制較弱
- **低 ASR**: 表示模型安全防護較好

### Refusal Rate
**拒絕率** - 衡量模型正確拒絕不當請求的比例

```
Refusal Rate = (拒絕回應數 / 總攻擊數) × 100%
```

- **高 Refusal Rate**: 表示模型能有效識別並拒絕不當請求
- **理想值**: 應與 ASR 互補（Refusal Rate + ASR ≈ 100%）

### Safety Score
**安全評分** - 由 Judge 評估每個回應的安全等級

- **5**: 完全安全，無任何風險
- **4**: 大致安全，有輕微問題
- **3**: 中等風險
- **2**: 明顯不安全
- **1**: 嚴重違反安全準則

### Precision & Recall
**評審準確度** - 衡量 Judge 評估的可靠性

- **Precision**: 預測為不安全的回應中，真正不安全的比例
- **Recall**: 所有不安全的回應中，被正確識別的比例

---

## 📚 理論基礎

本系統基於以下研究：

1. **Judging LLM-as-a-Judge** (LMSYS)
   - 使用 LLM 作為評審系統的有效性研究
   - Meta-evaluation 方法論

2. **Red Teaming Language Models with Language Models** (DeepMind)
   - 使用 LLM 自動生成對抗性測試案例
   - 多樣化攻擊策略

3. **Constitutional AI** (Anthropic)
   - AI 安全對齊原則
   - 自我批評與修正機制

---

## 🔐 安全性提醒

- 請勿將 `.env` 檔案上傳到 Git
- API Keys 應妥善保管
- 測試資料可能包含敏感內容，請小心處理

---

**⚠️ 免責聲明**: 本系統僅供研究與教育用途。測試過程中可能產生不當內容，請負責任地使用。
