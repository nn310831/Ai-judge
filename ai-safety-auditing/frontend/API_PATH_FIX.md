# API 路徑重複前綴修復說明

## 問題描述

後端日誌顯示出現了 `/api/api` 的重複路徑前綴，導致 404 錯誤：

```
404 /api/api/test/attacks
404 /api/api/models/loaded
404 /api/api/test/generate-attacks
```

## 根本原因

在 [frontend/src/api/client.ts](frontend/src/api/client.ts) 中，Axios 客戶端的 `baseURL` 被設置為 `/api`：

```typescript
const BASE_URL = '/api';

const apiClient: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  // ...
});
```

但在各個 API 服務文件中，API 調用又使用了完整路徑（包含 `/api` 前綴），例如：

```typescript
// ❌ 錯誤寫法
api.post('/api/test/generate-attacks', params);
api.get('/api/models/loaded');
```

這導致最終的請求路徑變成：`baseURL + path = /api + /api/test/... = /api/api/test/...`

## 解決方案

移除所有 API 服務文件中的 `/api` 前綴，只使用相對路徑：

```typescript
// ✅ 正確寫法
api.post('/test/generate-attacks', params);
api.get('/models/loaded');
```

因為 Axios 會自動將 `baseURL` 加到相對路徑前面，所以：
- `baseURL` = `/api`
- `path` = `/test/generate-attacks`
- 最終路徑 = `/api/test/generate-attacks` ✅

## 修改的文件

### API 服務層（移除 `/api` 前綴）

1. **frontend/src/api/attacks.ts**
   - `POST /test/generate-attacks` (原: `/api/test/generate-attacks`)
   - `GET /test/attacks` (原: `/api/test/attacks`)

2. **frontend/src/api/models.ts**
   - `GET /models/providers` (原: `/api/models/providers`)
   - `GET /models/loaded` (原: `/api/models/loaded`)
   - `GET /models/plugins` (原: `/api/models/plugins`)
   - `POST /models/plugins/load` (原: `/api/models/plugins/load`)
   - `POST /models/plugins/load-all` (原: `/api/models/plugins/load-all`)

3. **frontend/src/api/test.ts**
   - `POST /test/run` (原: `/api/test/run`)
   - `GET /test/status/:testId` (原: `/api/test/status/:testId`)
   - `GET /test/list` (原: `/api/test/list`)

4. **frontend/src/api/results.ts**
   - `GET /results/:testId` (原: `/api/results/:testId`)
   - `GET /results/:testId/metrics` (原: `/api/results/:testId/metrics`)
   - `GET /results/:testId/comparison` (原: `/api/results/:testId/comparison`)
   - `POST /results/:testId/statistical-test` (原: `/api/results/:testId/statistical-test`)
   - `GET /results/:testId/export` (原: `/api/results/:testId/export`)

5. **frontend/src/api/config.ts**
   - `GET /config/` (原: `/api/config/`)
   - `POST /config/` (原: `/api/config/`)
   - `GET /config/example` (原: `/api/config/example`)
   - `POST /config/load` (原: `/api/config/load`)

### 頁面組件（使用 API 服務而非直接 fetch）

6. **frontend/src/pages/Dashboard/Dashboard.tsx**
   - 替換 `fetch('/api/models/loaded')` 為 `modelService.getLoadedModels()`
   - 替換 `fetch('/api/test/list')` 為 `testService.listTests()`
   - 替換 `fetch('/api/results/${testId}/metrics')` 為 `resultsService.getTestMetrics(testId)`
   - 新增 import: `import { modelService, testService, resultsService } from '@/api';`

## 額外修復的 TypeScript 錯誤

在修復 API 路徑的同時，也解決了以下 TypeScript 錯誤：

### 1. StatusBadge 屬性錯誤
- ✅ 將所有 `text` prop 替換為 `label`
- ✅ 將所有 `status="error"` 替換為 `status="danger"`

### 2. Button 尺寸錯誤
- ✅ 將所有 `size="small"` 替換為 `size="sm"`

### 3. 其他修復
- ✅ Models.tsx: 修復 LoadedModel 類型不匹配
- ✅ Results.tsx: 移除未使用的 `useNavigate` import
- ✅ Results.tsx: 修復 getStatusColor 函數返回值
- ✅ Card.css: 移除空的 `.card-body` 規則

## 驗證

執行 `npm run dev` 後，所有 API 請求應該都會正確地發送到：
- `/api/models/*`
- `/api/test/*`
- `/api/results/*`
- `/api/config/*`

而不是錯誤的 `/api/api/*` 路徑。

## Vite 代理配置

Vite 開發服務器的代理配置保持不變（vite.config.ts）：

```typescript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
  },
}
```

這會將所有 `/api/*` 請求轉發到後端服務器 `http://localhost:8000/api/*`。

## 最終請求流程

1. 前端代碼: `api.get('/models/loaded')`
2. Axios 加上 baseURL: `/api/models/loaded`
3. Vite 代理轉發: `http://localhost:8000/api/models/loaded` ✅
4. 後端 FastAPI 路由: `@router.get("/api/models/loaded")` ✅

完美匹配！🎉
