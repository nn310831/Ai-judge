# AI Safety Auditing 前端 - 快速開始指南

## 🚀 快速啟動

### 1. 安裝依賴
```bash
cd frontend
npm install
```

### 2. 啟動後端 API
在另一個終端啟動後端服務：
```bash
cd ..
python backend/main.py
```

後端會運行在 `http://localhost:8000`

### 3. 啟動前端
```bash
npm run dev
```

前端會運行在 `http://localhost:5173`

## 📋 使用流程

### 第一步：配置模型

1. 打開瀏覽器訪問 `http://localhost:5173`
2. 點擊側邊欄的 **Settings**
3. 新增模型配置：
   - 名稱：`my-gpt4`
   - Provider：`openai`
   - Model Name：`gpt-4`
   - API Key：您的 OpenAI API key
   - Temperature：`0.7`
   - Max Tokens：`2048`
4. 點擊「儲存配置」
5. 點擊「載入並初始化模型」

### 第二步：生成攻擊

1. 點擊側邊欄的 **Testing**
2. 在攻擊生成器區域：
   - 選擇類別（例如：`harmful_content`）
   - 設定數量（例如：`10`）
   - 可選：勾選「使用 LLM 生成」
3. 點擊「生成攻擊」
4. 等待攻擊生成完成

### 第三步：執行測試

1. 在 Testing 頁面，攻擊列表會顯示剛生成的攻擊
2. 可以：
   - 點擊單個攻擊選擇
   - 點擊「全選」選擇所有
   - 使用篩選器按類別篩選
3. 確認系統狀態顯示已載入模型
4. 點擊「執行測試」
5. 測試開始執行，會在「執行中的測試」區域顯示進度

### 第四步：查看結果

1. 點擊側邊欄的 **Results**
2. 從左側測試歷史中選擇一個已完成的測試
3. 查看：
   - 測試摘要（狀態、總數、時間）
   - 整體指標（ASR、平均分數、拒絕率等）
   - 分數分布圖
   - 模型比較（如果測試了多個模型）
   - 詳細結果表格
4. 可以匯出結果：
   - 點擊「JSON」匯出 JSON 格式
   - 點擊「CSV」匯出 CSV 格式

### 第五步：查看總覽

1. 點擊側邊欄的 **Dashboard**
2. 查看系統總覽：
   - 關鍵安全指標（ASR、平均分數、拒絕率、總測試數）
   - 分數分布圖表
   - 系統狀態（Generator、Judge、Target Models）

## 🎨 頁面功能說明

### Dashboard (首頁)
- **功能**：系統總覽和監控
- **顯示**：最新測試的關鍵指標和系統狀態
- **用途**：快速了解系統安全性狀況

### Models (模型管理)
- **功能**：管理目標模型和外掛
- **顯示**：
  - 已載入的模型列表
  - 可用的 Providers
  - 已載入的外掛
  - 配置檔預覽
- **用途**：查看和管理測試目標

### Testing (測試執行)
- **功能**：生成攻擊和執行測試
- **顯示**：
  - 攻擊生成器
  - 攻擊列表和選擇
  - 執行中的測試進度
  - 系統狀態
- **用途**：創建和執行安全性測試

### Results (結果分析)
- **功能**：查看和分析測試結果
- **顯示**：
  - 測試歷史列表
  - 詳細測試結果
  - 統計指標
  - 模型對比
- **用途**：深入分析測試結果

### Settings (系統設定)
- **功能**：配置模型和系統參數
- **顯示**：
  - 配置檔資訊
  - 模型配置表單
  - JSON 預覽
- **用途**：設定測試環境

## 🔍 故障排除

### 後端連接失敗
**問題**：前端顯示「尚無測試數據」或載入失敗

**解決方案**：
1. 確認後端正在運行：`http://localhost:8000`
2. 在瀏覽器訪問：`http://localhost:8000/docs`
3. 檢查瀏覽器控制台錯誤訊息

### 模型載入失敗
**問題**：Settings 頁面儲存配置後載入失敗

**解決方案**：
1. 確認 API Key 正確
2. 確認網路連接正常
3. 檢查 Provider 和 Model Name 拼寫
4. 查看後端終端的錯誤日誌

### 測試無法執行
**問題**：點擊「執行測試」沒有反應

**解決方案**：
1. 確認已載入至少一個模型
2. 確認已生成或選擇攻擊
3. 檢查瀏覽器控制台錯誤
4. 刷新頁面重試

## 📚 API 端點對照

### 前端調用 → 後端路由

| 前端服務 | API 路徑 | 後端路由 | 說明 |
|---------|---------|---------|------|
| `configService.getConfig()` | `GET /api/config/` | `config.router` | 獲取配置 |
| `modelService.getLoadedModels()` | `GET /api/models/loaded` | `models.router` | 獲取已載入模型 |
| `attackService.generateAttacks()` | `POST /api/test/generate-attacks` | `test.router` | 生成攻擊 |
| `testService.runTest()` | `POST /api/test/run` | `test.router` | 執行測試 |
| `resultsService.getTestResults()` | `GET /api/results/{test_id}` | `results.router` | 獲取結果 |

## 💡 進階提示

### 批量測試
1. 生成多個類別的攻擊
2. 使用「全選」選擇所有攻擊
3. 確保載入多個模型以進行對比
4. 執行測試後在 Results 頁面對比模型表現

### 自定義攻擊
1. 使用「使用 LLM 生成」選項獲得更多樣化的攻擊
2. 嘗試不同的類別組合
3. 調整生成數量找到最佳測試規模

### 結果分析
1. 注意 ASR (Attack Success Rate) - 越低越好
2. 查看分數分布了解模型行為模式
3. 使用模型比較功能找出最安全的模型
4. 匯出 CSV 在 Excel 中進行進階分析

## 🛠 開發者資訊

### 技術棧
- React 18 + TypeScript
- Vite 5
- React Router 6
- Recharts (圖表)
- Lucide React (圖標)

### 項目結構
```
frontend/src/
├── api/          # API 服務層
├── components/   # UI 組件
├── pages/        # 頁面組件
├── layouts/      # 布局組件
├── styles/       # 全局樣式
└── types/        # TypeScript 類型
```

### 修改建議
- 修改主題：編輯 `src/styles/theme.css`
- 添加新頁面：在 `src/pages/` 創建，更新 `App.tsx` 路由
- 修改 API：編輯 `src/api/` 對應的服務文件
- 調整布局：編輯 `src/layouts/MainLayout.tsx`

## 📞 需要幫助？

查看詳細文檔：
- [README.md](./README.md) - 項目概述
- [INSTALLATION_GUIDE.md](./INSTALLATION_GUIDE.md) - 安裝指南
- [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md) - 功能總結

後端文檔：
- API 文檔：`http://localhost:8000/docs`

## ⚡ 快速命令參考

```bash
# 安裝
npm install

# 開發
npm run dev

# 構建
npm run build

# 預覽構建
npm run preview

# 類型檢查
npm run type-check

# Lint
npm run lint
```

祝測試順利！🎉
