# 🚀 AI Safety Auditing System - 完整安裝與啟動指南

## 📋 系統需求

- **Node.js**: >= 18.0.0
- **Python**: >= 3.11
- **npm** 或 **yarn**

---

## 🎯 一、快速啟動（3 步驟）

### 1️⃣ 安裝前端依賴

```bash
cd frontend
npm install
```

### 2️⃣ 啟動後端 API（另開終端）

```bash
# 在專案根目錄
cd ai-safety-auditing
python backend/main.py
```

後端將運行在 `http://localhost:8000`

### 3️⃣ 啟動前端開發伺服器

```bash
# 在 frontend 目錄
npm run dev
```

前端將運行在 `http://localhost:3000`

✅ 打開瀏覽器訪問: **http://localhost:3000**

---

## 📁 二、專案架構總覽

```
ai-safety-auditing/
├── backend/                 # FastAPI 後端
│   ├── main.py             # API 入口
│   ├── api/                # API 路由
│   ├── services/           # 業務邏輯
│   └── models.py           # Pydantic Models
│
├── src/                    # Python 核心邏輯
│   ├── generator/          # 攻擊生成器
│   ├── target/             # 目標模型
│   ├── judge/              # 安全評審
│   └── evaluation/         # 指標計算
│
└── frontend/               # React 前端 ⭐ NEW
    ├── src/
    │   ├── api/            # API Service Layer
    │   ├── components/     # UI 組件
    │   ├── pages/          # 頁面
    │   ├── layouts/        # 佈局
    │   ├── styles/         # 全域樣式
    │   └── types/          # TypeScript 類型
    │
    ├── package.json
    ├── vite.config.ts
    └── tsconfig.json
```

---

## 🎨 三、前端設計特色

### 科技感視覺風格

✨ **Glassmorphism（玻璃擬態）**
- 半透明面板
- 背景模糊效果
- 細微邊框發光

🌈 **配色方案**
```css
主色：Indigo (#6366f1)     - 按鈕、重點
輔助色：Cyan (#06b6d4)     - 圖表、強調
危險色：Red (#ef4444)      - 警告、錯誤
成功色：Green (#10b981)    - 安全、成功
```

🎯 **UI 元件**
- 現代化按鈕（漸層、發光效果）
- 卡片式 Dashboard
- 狀態徽章（Pulse 動畫）
- 專業圖表（Recharts）

---

## 🔌 四、API 整合範例

### 完整的 TypeScript 類型支援

```typescript
// ✅ 類型安全的 API 呼叫
import { systemService } from '@/api';
import type { Metrics } from '@/types/api';

// 自動完成 + 類型檢查
const metrics: Metrics = await systemService.calculateMetrics();

console.log(metrics.asr);           // ✅ 正確
console.log(metrics.unknownField);  // ❌ TypeScript 錯誤
```

### 統一的錯誤處理

```typescript
try {
  const data = await systemService.getState();
  // 處理數據
} catch (error: any) {
  // 統一的錯誤格式
  console.error('API Error:', error.message);
  setError(error.message);
}
```

### 所有 API 服務

```typescript
import { 
  attackService,   // 攻擊生成
  modelService,    // 模型管理
  judgeService,    // 評審系統
  systemService    // 系統狀態
} from '@/api';

// 範例：生成攻擊
const result = await attackService.generateAttacks({
  num_attacks: 10,
  categories: ['jailbreak', 'prompt_injection'],
  use_llm: true,
});

// 範例：評估響應
const evaluation = await judgeService.evaluateSingle({
  attack_prompt: "...",
  model_response: "...",
});

// 範例：獲取指標
const metrics = await systemService.calculateMetrics();
```

---

## 🧩 五、UI 組件使用範例

### Button 組件

```tsx
import { Button } from '@/components';

// Primary 按鈕（漸層 + 發光）
<Button variant="primary" size="md" loading={isLoading}>
  Generate Attacks
</Button>

// Secondary 按鈕（Glassmorphism）
<Button variant="secondary" onClick={handleRefresh}>
  Refresh Data
</Button>

// Danger 按鈕（紅色 + 發光）
<Button variant="danger" onClick={handleReset}>
  Reset System
</Button>
```

### Card 組件

```tsx
import { Card, CardHeader, CardBody } from '@/components';

<Card hover glow>
  <CardHeader 
    title="Security Metrics" 
    subtitle="Real-time monitoring"
    action={<Button size="sm">Export</Button>}
  />
  <CardBody>
    <p>ASR: 25.5%</p>
    <p>Average Score: 4.2/5.0</p>
  </CardBody>
</Card>
```

### StatusBadge 組件

```tsx
import { StatusBadge, getScoreStatus, getScoreLabel } from '@/components';

// 自動根據分數設定顏色
<StatusBadge 
  status={getScoreStatus(score)}    // 'success' | 'warning' | 'danger'
  label={getScoreLabel(score)}      // 'SAFE' | 'UNSAFE' | 'CRITICAL'
  pulse                              // 脈動動畫
/>

// 手動設定
<StatusBadge status="success" label="ONLINE" pulse />
<StatusBadge status="danger" label="CRITICAL" />
```

---

## 📊 六、數據視覺化

### 分數分布圖表

```tsx
import { ScoreDistributionChart } from './components/ScoreDistributionChart';

<ScoreDistributionChart 
  data={{
    1: 10,   // 10 次得 1 分
    2: 15,   // 15 次得 2 分
    3: 10,
    4: 30,
    5: 35
  }}
  total={100}
/>
```

**特色**：
- 自動配色（1分紅色 → 5分綠色）
- 懸停顯示詳細資訊
- 響應式設計

---

## 🎯 七、為什麼這樣設計？

### 1. Vite 而非 Create React App

| 優勢 | 說明 |
|------|------|
| ⚡ 極速啟動 | 秒級冷啟動 |
| 🔥 熱更新快 | 實時反映變更 |
| 📦 優化構建 | Rollup 生產構建 |
| 🎯 現代化 | 原生 ESM 支援 |

### 2. TypeScript 嚴格模式

**好處**：
```typescript
// ❌ 編譯時就發現錯誤
const score: number = "5";  // Type Error!

// ✅ IDE 自動完成
systemService.  // ← 自動顯示所有方法
```

### 3. Service Layer 架構

**為什麼不直接在組件中呼叫 API？**

```typescript
// ❌ 不好的做法
function Component() {
  const data = await axios.get('/api/metrics');
}

// ✅ 好的做法
function Component() {
  const data = await systemService.calculateMetrics();
}
```

**優勢**：
- 統一的錯誤處理
- 可重用的 API 邏輯
- 易於測試
- 類型安全

### 4. CSS Variables 主題系統

**為什麼不用 Tailwind？**

對於**系統級工具**：
- ✅ CSS Variables 更適合 Dark Mode
- ✅ 全域主題一致性
- ✅ 更精確的顏色控制
- ✅ 更好的 Glassmorphism 效果

```css
/* 一次修改，全局生效 */
:root {
  --accent-primary: #6366f1;
}

.button-primary {
  background: var(--accent-primary);
}
```

---

## 🚀 八、開發流程

### 添加新頁面

1. **創建頁面組件**
```tsx
// src/pages/Attacks/Attacks.tsx
export function Attacks() {
  return <div>Attack Generator Page</div>;
}
```

2. **添加路由**
```tsx
// App.tsx
import { Attacks } from './pages/Attacks/Attacks';

<Route path="/attacks" element={<Attacks />} />
```

3. **更新 Sidebar**
```tsx
// components/Sidebar/Sidebar.tsx
const navigation = [
  // ...
  { name: 'Attacks', path: '/attacks', icon: Target },
];
```

### 添加新 API 服務

1. **定義類型**
```typescript
// types/api.ts
export interface NewFeature {
  id: string;
  name: string;
}
```

2. **創建服務**
```typescript
// api/feature.ts
export const featureService = {
  getAll: async (): Promise<NewFeature[]> => {
    return api.get<NewFeature[]>('/features');
  },
};
```

3. **使用服務**
```tsx
import { featureService } from '@/api';

const features = await featureService.getAll();
```

---

## 🔧 九、常見問題

### Q: API 請求失敗怎麼辦？

確保後端正在運行：
```bash
cd ai-safety-auditing
python backend/main.py
```

檢查 Vite proxy 配置 (`vite.config.ts`)：
```typescript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
  },
}
```

### Q: 如何修改主題顏色？

編輯 `src/styles/theme.css`：
```css
:root {
  --accent-primary: #your-color;
}
```

### Q: 如何添加新圖表？

1. 安裝 Recharts（已安裝）
2. 創建新圖表組件
3. 使用相同的配色方案

---

## 📱 十、響應式設計

所有組件都支援響應式：

```css
/* Desktop */
@media (min-width: 1024px) {
  .grid-4 { grid-template-columns: repeat(4, 1fr); }
}

/* Tablet */
@media (max-width: 1024px) {
  .grid-4 { grid-template-columns: repeat(2, 1fr); }
}

/* Mobile */
@media (max-width: 640px) {
  .grid-4 { grid-template-columns: 1fr; }
}
```

---

## 🎓 十一、學習資源

- [React 官方文檔](https://react.dev/)
- [Vite 文檔](https://vitejs.dev/)
- [TypeScript 手冊](https://www.typescriptlang.org/docs/)
- [Recharts 範例](https://recharts.org/en-US/examples)

---

## ✅ 十二、檢查清單

確保一切正常：

- [ ] Node.js >= 18 已安裝
- [ ] Python >= 3.11 已安裝
- [ ] `npm install` 成功
- [ ] 後端 API 運行中（http://localhost:8000）
- [ ] 前端運行中（http://localhost:3000）
- [ ] 瀏覽器打開無錯誤
- [ ] Dashboard 正常顯示

---

## 🎯 完成！

你現在擁有一個完整的、專業級的 AI Safety Auditing System 前端系統：

✅ 現代化技術棧  
✅ 科技感 UI 設計  
✅ 完整的 TypeScript 類型支援  
✅ 統一的 API Service Layer  
✅ 可擴展的組件系統  
✅ 響應式設計  
✅ 生產就緒  

立即開始使用：`npm run dev` 🚀
