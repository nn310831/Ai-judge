# AI Safety Auditing System - Frontend

專業的 AI 安全審計系統前端介面，採用現代化技術棧和科技感設計風格。

## 🎯 技術棧

- **React 18** - UI 框架
- **TypeScript** - 類型安全
- **Vite** - 極速開發體驗
- **React Router** - 路由管理
- **Axios** - HTTP 客戶端
- **Recharts** - 數據視覺化
- **Lucide React** - Icon 系統

## 📦 快速開始

### 1. 安裝依賴

```bash
cd frontend
npm install
```

### 2. 啟動開發伺服器

```bash
npm run dev
```

前端將運行在 `http://localhost:3000`

### 3. 確保後端 API 運行

```bash
# 在專案根目錄
python backend/main.py
```

後端 API 應運行在 `http://localhost:8000`

## 🏗️ 專案結構

```
frontend/
├── src/
│   ├── api/                 # API Service Layer
│   │   ├── client.ts        # Axios 配置
│   │   ├── attacks.ts       # 攻擊生成 API
│   │   ├── models.ts        # 模型管理 API
│   │   ├── judge.ts         # 評審系統 API
│   │   └── system.ts        # 系統狀態 API
│   │
│   ├── components/          # 可重用 UI 組件
│   │   ├── Button/          # 按鈕組件
│   │   ├── Card/            # 卡片組件（Glassmorphism）
│   │   ├── StatusBadge/     # 狀態徽章
│   │   └── Sidebar/         # 側邊欄導航
│   │
│   ├── pages/               # 頁面組件
│   │   └── Dashboard/       # 儀表板主頁
│   │       ├── Dashboard.tsx
│   │       ├── Dashboard.css
│   │       └── components/  # 頁面專屬組件
│   │           └── ScoreDistributionChart.tsx
│   │
│   ├── layouts/             # 佈局組件
│   │   └── MainLayout.tsx   # 主佈局（Sidebar + Content）
│   │
│   ├── styles/              # 全域樣式
│   │   ├── theme.css        # 主題變數（顏色、間距）
│   │   └── globals.css      # 全域工具類
│   │
│   ├── types/               # TypeScript 類型定義
│   │   └── api.ts           # API 響應類型
│   │
│   ├── App.tsx              # 主應用組件
│   └── main.tsx             # 應用入口
│
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

## 🎨 設計理念

### 科技感視覺風格

1. **Dark Mode First**
   - 深色背景（#0a0e1a）為主
   - 減少眼睛疲勞，適合長時間使用

2. **Glassmorphism（玻璃擬態）**
   - 半透明面板 + 背景模糊
   - 細微邊框發光效果
   - 現代化、層次感強

3. **配色方案**
   - 主色：Indigo (#6366f1)
   - 輔助色：Cyan (#06b6d4)
   - 強調色：Purple (#8b5cf6)
   - 狀態色：Success/Warning/Danger

4. **Typography**
   - 主字體：Inter（清晰、現代）
   - 等寬字體：JetBrains Mono（代碼、數據）

### UI 設計原則

- **專業工具感**：不花俏，重視資訊密度
- **可掃描性**：清晰的視覺層次
- **系統感**：統一的組件規範
- **回饋明確**：Hover/Focus 狀態清楚

## 🔌 API 整合

### API Service Layer 架構

所有 API 呼叫都經過統一的 Service Layer：

```typescript
// 範例：獲取系統指標
import { systemService } from '@/api';

const metrics = await systemService.calculateMetrics();
```

### 類型安全

所有 API 響應都有完整的 TypeScript 類型：

```typescript
// types/api.ts
export interface Metrics {
  total_tests: number;
  asr: number;
  average_score: number;
  // ...
}
```

### 錯誤處理

統一的錯誤處理機制：

```typescript
try {
  const data = await systemService.getState();
} catch (error: any) {
  console.error('API Error:', error.message);
  // 顯示錯誤 UI
}
```

## 🧩 核心組件

### Button

```tsx
import { Button } from '@/components';

<Button variant="primary" size="md" loading={isLoading}>
  Generate Attacks
</Button>
```

### Card

```tsx
import { Card, CardHeader, CardBody } from '@/components';

<Card hover glow>
  <CardHeader title="Metrics" subtitle="Real-time stats" />
  <CardBody>
    {/* Content */}
  </CardBody>
</Card>
```

### StatusBadge

```tsx
import { StatusBadge, getScoreStatus } from '@/components';

<StatusBadge 
  status={getScoreStatus(score)} 
  label="SAFE" 
  pulse 
/>
```

## 📊 數據視覺化

使用 Recharts 進行專業的數據可視化：

```tsx
import { ScoreDistributionChart } from './components/ScoreDistributionChart';

<ScoreDistributionChart 
  data={scoreDistribution} 
  total={totalTests} 
/>
```

## 🚀 構建與部署

### 開發構建

```bash
npm run dev
```

### 生產構建

```bash
npm run build
```

構建產物在 `dist/` 目錄。

### 預覽生產構建

```bash
npm run preview
```

## 🔧 配置

### Vite Proxy 配置

`vite.config.ts` 中配置了 API 代理：

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

### Path Alias

使用 `@/` 作為 `src/` 的別名：

```typescript
import { Button } from '@/components';
import { systemService } from '@/api';
```

## 🎯 為什麼選擇這些技術？

### Vite

- ⚡ 極速的 HMR（熱模組替換）
- 📦 優化的生產構建
- 🔧 開箱即用的 TypeScript 支援
- 🎯 現代化的開發體驗

### TypeScript

- 🛡️ 類型安全
- 🔍 更好的 IDE 支援
- 📚 自動文檔化
- 🐛 編譯時錯誤檢測

### React Router

- 🗺️ 聲明式路由
- 📱 SPA 導航體驗
- 🔗 動態路由參數

### Axios

- 🌐 統一的 HTTP 客戶端
- 🔄 請求/響應攔截器
- ⚙️ 可配置的預設值
- 📊 自動 JSON 轉換

## 📝 開發指南

### 添加新頁面

1. 在 `src/pages/` 創建新目錄
2. 實作頁面組件
3. 在 `App.tsx` 添加路由

### 添加新 API 服務

1. 在 `src/api/` 創建新文件
2. 定義類型在 `src/types/api.ts`
3. 使用統一的 `api` 客戶端

### 添加新組件

1. 在 `src/components/` 創建新目錄
2. 實作組件 + 樣式
3. 在 `src/components/index.ts` 導出

## 🎨 主題客製化

編輯 `src/styles/theme.css` 修改全域主題變數：

```css
:root {
  --accent-primary: #6366f1;
  --bg-primary: #0a0e1a;
  /* ... */
}
```

## 📱 響應式設計

所有組件都支援響應式設計，主要斷點：

- Desktop: > 1024px
- Tablet: 640px - 1024px
- Mobile: < 640px

## 🔮 未來擴展

系統已預留擴展空間：

- 🔐 身份驗證（Auth Token 已預留）
- 👥 角色權限管理（RBAC）
- 🌐 國際化（i18n）
- 📊 更多圖表類型
- 🔔 即時通知系統

## 📄 授權

MIT License
