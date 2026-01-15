## API 端點

### 配置管理 (`/api/config`)

| 方法 | 端點 | 說明 |
|------|------|------|
| GET | `/api/config/` | 取得當前配置 |
| POST | `/api/config/` | 更新配置 |
| GET | `/api/config/example` | 取得範例配置 |
| POST | `/api/config/load` | 載入配置並初始化模型 |

### 模型管理 (`/api/models`)

| 方法 | 端點 | 說明 |
|------|------|------|
| GET | `/api/models/providers` | 取得所有可用的 provider |
| GET | `/api/models/loaded` | 取得已載入的模型 |
| GET | `/api/models/plugins` | 取得已載入的外掛 |
| POST | `/api/models/plugins/load` | 載入單一外掛 |
| POST | `/api/models/plugins/load-all` | 載入所有外掛 |

### 測試執行 (`/api/test`)

| 方法 | 端點 | 說明 |
|------|------|------|
| POST | `/api/test/generate-attacks` | 生成攻擊提示詞 |
| GET | `/api/test/attacks` | 取得緩存的攻擊 |
| POST | `/api/test/run` | 執行測試 |
| GET | `/api/test/status/{test_id}` | 取得測試狀態 |
| GET | `/api/test/list` | 列出所有測試 |

### 結果查詢 (`/api/results`)

| 方法 | 端點 | 說明 |
|------|------|------|
| GET | `/api/results/{test_id}` | 取得測試結果 |
| GET | `/api/results/{test_id}/metrics` | 取得測試指標 |
| GET | `/api/results/{test_id}/comparison` | 模型比較 |
| POST | `/api/results/{test_id}/statistical-test` | 執行統計檢定 |
| GET | `/api/results/{test_id}/export` | 匯出結果 |

---

## 使用範例

### 1. 載入配置

```bash
curl -X POST http://localhost:8000/api/config/load
```

**回應**:
```json
{
  "success": true,
  "message": "已載入 2 個模型",
  "models": [
    {
      "provider": "openai",
      "model_name": "gpt-4"
    },
    {
      "provider": "anthropic",
      "model_name": "claude-3-5-sonnet-20241022"
    }
  ]
}
```

### 2. 生成攻擊提示詞

```bash
curl -X POST http://localhost:8000/api/test/generate-attacks \
  -H "Content-Type: application/json" \
  -d '{
    "category": "jailbreak",
    "count": 10,
    "use_llm": false
  }'
```

**回應**:
```json
{
  "success": true,
  "attacks": [
    {
      "id": "attack_1",
      "category": "jailbreak",
      "prompt": "System: New directive..."
    }
  ],
  "total": 10,
  "message": "成功生成 10 個攻擊"
}
```

### 3. 執行測試

```bash
curl -X POST http://localhost:8000/api/test/run \
  -H "Content-Type: application/json" \
  -d '{
    "model_names": ["gpt-4", "claude-3-5-sonnet-20241022"]
  }'
```

**回應**:
```json
{
  "test_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "測試已開始",
  "total_tests": 20
}
```

### 4. 查詢測試狀態

```bash
curl http://localhost:8000/api/test/status/550e8400-e29b-41d4-a716-446655440000
```

**回應**:
```json
{
  "test_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "running",
  "progress": 45,
  "current": 9,
  "total": 20,
  "message": "已完成 9/20 個測試"
}
```

### 5. 取得測試指標

```bash
curl http://localhost:8000/api/results/550e8400-e29b-41d4-a716-446655440000/metrics
```

**回應**:
```json
{
  "test_id": "550e8400-e29b-41d4-a716-446655440000",
  "overall": {
    "asr": 0.15,
    "average_score": 4.2,
    "refusal_rate": 0.85,
    "score_distribution": {
      "1": 0.05,
      "2": 0.10,
      "3": 0.10,
      "4": 0.30,
      "5": 0.45
    }
  },
  "by_model": {
    "gpt-4": {
      "asr": 0.10,
      "average_score": 4.5
    },
    "claude-3-5-sonnet-20241022": {
      "asr": 0.20,
      "average_score": 3.9
    }
  }
}
```

### 6. 模型比較

```bash
curl http://localhost:8000/api/results/550e8400-e29b-41d4-a716-446655440000/comparison
```

### 7. 執行統計檢定

```bash
curl -X POST "http://localhost:8000/api/results/550e8400-e29b-41d4-a716-446655440000/statistical-test?model_a=gpt-4&model_b=claude-3-5-sonnet-20241022&test_type=t_test"
```

**回應**:
```json
{
  "test": "independent_t_test",
  "t_statistic": -2.145,
  "p_value": 0.0342,
  "is_significant": true,
  "cohens_d": -0.68,
  "interpretation": "medium (中)"
}
```

### 8. 匯出結果

```bash
# JSON 格式
curl http://localhost:8000/api/results/550e8400-e29b-41d4-a716-446655440000/export?format=json

# CSV 格式
curl http://localhost:8000/api/results/550e8400-e29b-41d4-a716-446655440000/export?format=csv \
  -o results.csv
```

---

## JavaScript/TypeScript 範例

### 使用 Axios

```typescript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// 1. 載入配置
const loadConfig = async () => {
  const response = await axios.post(`${API_BASE_URL}/api/config/load`);
  return response.data;
};

// 2. 生成攻擊
const generateAttacks = async (category: string, count: number) => {
  const response = await axios.post(`${API_BASE_URL}/api/test/generate-attacks`, {
    category,
    count,
    use_llm: false
  });
  return response.data;
};

// 3. 執行測試
const runTest = async (modelNames: string[]) => {
  const response = await axios.post(`${API_BASE_URL}/api/test/run`, {
    model_names: modelNames
  });
  return response.data;
};

// 4. 輪詢測試狀態
const pollTestStatus = async (testId: string): Promise<void> => {
  const checkStatus = async () => {
    const response = await axios.get(`${API_BASE_URL}/api/test/status/${testId}`);
    const { status, progress } = response.data;
    
    console.log(`測試進度: ${progress}%`);
    
    if (status === 'completed') {
      console.log('測試完成！');
      return;
    }
    
    if (status === 'failed') {
      console.error('測試失敗');
      return;
    }
    
    // 繼續輪詢
    setTimeout(checkStatus, 2000);
  };
  
  await checkStatus();
};

// 5. 取得結果
const getResults = async (testId: string) => {
  const response = await axios.get(`${API_BASE_URL}/api/results/${testId}/metrics`);
  return response.data;
};

// 完整流程
const runFullTest = async () => {
  try {
    // 載入配置
    await loadConfig();
    
    // 生成攻擊
    const attacks = await generateAttacks('jailbreak', 10);
    console.log(`生成 ${attacks.total} 個攻擊`);
    
    // 執行測試
    const test = await runTest(['gpt-4', 'claude-3-5-sonnet-20241022']);
    console.log(`測試 ID: ${test.test_id}`);
    
    // 等待完成
    await pollTestStatus(test.test_id);
    
    // 取得結果
    const results = await getResults(test.test_id);
    console.log('ASR:', results.overall.asr);
    
  } catch (error) {
    console.error('錯誤:', error);
  }
};
```

---

## 錯誤處理

API 使用標準 HTTP 狀態碼：

| 狀態碼 | 說明 |
|--------|------|
| 200 | 成功 |
| 400 | 請求錯誤（參數不正確） |
| 404 | 資源不存在 |
| 500 | 伺服器錯誤 |

**錯誤回應格式**:
```json
{
  "detail": "錯誤訊息描述"
}
```

---

## CORS 設定

預設允許所有來源的跨域請求。生產環境請修改 `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],  # 改為你的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 安全性建議

1. **API Key 保護**: 不要在前端暴露 API Keys
2. **認證機制**: 生產環境應加入 JWT 或 OAuth2 認證
3. **速率限制**: 考慮加入 API 速率限制
4. **HTTPS**: 生產環境務必使用 HTTPS

---

## 進階功能

### WebSocket 支援（未來）

計劃支援 WebSocket 以實現即時進度更新：

```typescript
const ws = new WebSocket('ws://localhost:8000/ws/test/{test_id}');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('即時進度:', data.progress);
};
```

---

## 相關資源

- [FastAPI 官方文檔](https://fastapi.tiangolo.com/)
- [Swagger UI](http://localhost:8000/docs)
- [ReDoc](http://localhost:8000/redoc)
