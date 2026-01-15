# AI Safety Auditing System

基於 LLM-as-a-Judge 的自動化 AI 責任與安全審計系統

## 📋 專題資訊

**標題**: Automated AI Responsibility & Safety Auditing System based on LLM-as-a-Judge

**目標**: 建立一個自動化紅隊測試管線，評估 LLM 對倫理/安全標準的遵從性

**研究動機**: 
- Grok AI 爭議顯示廠商自律不足
- 需要第三方自動化審計工具
- 解決人工測試的覆蓋率、主觀性、工具缺失問題

## 🏗️ 系統架構

```
攻擊生成器 (Generator) → 目標 LLM (Target) → 評審系統 (Judge)
         ↓                      ↓                    ↓
   攻擊提示詞庫            模型回應記錄           安全評分
                                                     ↓
                                              統計分析 & 視覺化
```

## 🚀 快速開始

### 1. 環境設定

```bash
# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

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
```

### 3. 配置模型

```bash
# 複製並編輯模型配置檔案（扁平格式）
cp config/models_config.example.json config/models_config.json

# 編輯 config/models_config.json，配置你要測試的模型
# 格式：
# {
#   "models": [
#     {
#       "provider": "openai",
#       "model_name": "gpt-4",
#       "api_key": "${OPENAI_API_KEY}",
#       "temperature": 0.7,
#       "max_tokens": 1000
#     }
#   ]
# }
```

### 4. 執行測試

```bash
# 執行完整測試流程
python main.py

# 或啟動 Web 界面（前後端分離）
# 後端
python backend/main.py

# 前端（新終端）
cd frontend
npm install
npm run dev
```

## 📁 專案結構

```
ai-safety-auditing/
├── backend/             # FastAPI 後端
│   ├── api/            # API 路由
│   ├── services/       # 業務邏輯
│   └── models.py       # 數據模型（扁平格式配置）
├── frontend/           # React + TypeScript 前端
│   ├── src/
│   │   ├── api/        # API 客戶端
│   │   ├── components/ # React 組件
│   │   ├── pages/      # 頁面組件
│   │   └── types/      # TypeScript 類型
├── config/             # 配置檔案（扁平格式）
│   ├── models_config.json         # 模型配置
│   └── models_config.example.json # 配置範例
├── src/                # 核心程式碼
│   ├── generator/      # 攻擊生成模組
│   ├── target/         # 目標模型介面（支持扁平格式配置）
│   ├── judge/          # 評審系統
│   ├── evaluation/     # 評估指標
│   └── utils/          # 工具函式
├── data/               # 資料儲存
└── results/            # 輸出結果
```

## 🎯 核心指標

- **ASR (Attack Success Rate)**: 攻擊成功率
- **Refusal Rate**: 拒絕率
- **Safety Score**: 安全分數 (1-5)
- **Precision/Recall**: 評審準確度

## 📚 理論基礎

- *Judging LLM-as-a-Judge* (LMSYS)
- *Red Teaming Language Models with Language Models* (DeepMind)
- *Constitutional AI* (Anthropic)

## 📊 實驗階段

- [x] Phase 1: 環境建置
- [x] Phase 2: MVP 原型
- [ ] Phase 3: 核心功能開發
- [ ] Phase 4: 評估與實驗
- [ ] Phase 5: 論文撰寫

## 🔐 安全性提醒

- 請勿將 `.env` 檔案上傳到 Git
- API Keys 應妥善保管
- 測試資料可能包含敏感內容，請小心處理

## 📝 License

此專案為北科大專題研究，僅供學術用途。

## 👤 作者

- 學校：國立臺北科技大學
- 專題：Responsible AI Auditing
- 日期：2026年1月
