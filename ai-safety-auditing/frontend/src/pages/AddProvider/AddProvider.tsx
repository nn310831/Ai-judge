/**
 * Add Provider Page
 * 
 * 上傳自定義 Model Provider 的頁面
 */

import React, { useState } from 'react';
import { Upload, Code, CheckCircle, XCircle, Loader, AlertCircle, FileCode } from 'lucide-react';
import Editor from '@monaco-editor/react';
import { Card } from '@/components/Card/Card';
import { Button } from '@/components/Button/Button';
import './AddProvider.css';

export const AddProvider: React.FC = () => {
  const [code, setCode] = useState('');
  const [fileName, setFileName] = useState('');
  const [dependencies, setDependencies] = useState('');
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<{ success: boolean; message: string } | null>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.name.endsWith('.py')) {
      setFileName(file.name);
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target?.result as string;
        setCode(content);
      };
      reader.readAsText(file);
    } else {
      alert('請選擇 .py 檔案');
    }
  };

  const handleUpload = async () => {
    if (!code.trim()) {
      alert('請輸入或上傳 Python 程式碼');
      return;
    }

    if (!fileName) {
      alert('請提供檔案名稱');
      return;
    }

    setUploading(true);
    setUploadResult(null);

    try {
      const response = await fetch('http://localhost:8000/api/models/upload-provider', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          file_name: fileName,
          code: code,
          dependencies: dependencies.split(',').map(d => d.trim()).filter(d => d),
        }),
      });

      const result = await response.json();

      if (response.ok && result.success) {
        setUploadResult({ success: true, message: result.message || '上傳成功！請前往 Models 頁面查看新的 Provider' });
        // 清空表單
        setTimeout(() => {
          setCode('');
          setFileName('');
          setDependencies('');
          setUploadResult(null);
        }, 5000);
      } else {
        setUploadResult({ 
          success: false, 
          message: result.error || result.detail || '上傳失敗' 
        });
      }
    } catch (error: any) {
      setUploadResult({ 
        success: false, 
        message: error.message || '網路錯誤，請檢查後端是否運行' 
      });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="add-provider-page">
      <header className="page-header">
        <div>
          <h1>Provider 管理</h1>
          <p className="page-subtitle">上傳自定義 Model Provider</p>
        </div>
      </header>

      {/* Upload Result Banner */}
      {uploadResult && (
        <div className={`result-banner ${uploadResult.success ? 'result-success' : 'result-error'}`}>
          {uploadResult.success ? <CheckCircle size={20} /> : <XCircle size={20} />}
          {uploadResult.message}
        </div>
      )}

      {/* Code Editor Section */}
      <section className="upload-section">
        <Card className="upload-card">
          <div className="upload-header">
            <div className="upload-title">
              <Code size={24} />
              <h2>Python 程式碼</h2>
            </div>
            <div className="upload-actions">
              <label className="file-upload-btn">
                <FileCode size={18} />
                選擇檔案
                <input
                  type="file"
                  accept=".py"
                  onChange={handleFileSelect}
                  style={{ display: 'none' }}
                />
              </label>
            </div>
          </div>

          <div className="file-name-input">
            <label htmlFor="fileName">檔案名稱:</label>
            <input
              id="fileName"
              type="text"
              value={fileName}
              onChange={(e) => setFileName(e.target.value)}
              placeholder="my_custom_model.py"
              className="file-name-field"
            />
          </div>

          <div className="file-name-input">
            <label htmlFor="dependencies">依賴套件:</label>
            <input
              id="dependencies"
              type="text"
              value={dependencies}
              onChange={(e) => setDependencies(e.target.value)}
              placeholder="google-generativeai, httpx, requests"
              className="file-name-field"
            />
            <span className="input-hint">多個套件用逗號分隔</span>
            <div className="security-notice">
              <AlertCircle size={14} />
              <span>出於安全考量，僅允許安裝白名單內的套件：google-generativeai, anthropic, openai, httpx, requests, aiohttp, pydantic, typing-extensions, python-dotenv</span>
            </div>
          </div>

          <Editor
            height="500px"
            defaultLanguage="python"
            theme="vs-dark"
            value={code}
            onChange={(value) => setCode(value || '')}
            options={{
              minimap: { enabled: false },
              fontSize: 14,
              lineNumbers: 'on',
              scrollBeyondLastLine: false,
              automaticLayout: true,
              tabSize: 4,
              wordWrap: 'on',
            }}
          />

          <div className="upload-footer">
            <Button
              onClick={handleUpload}
              disabled={uploading || !code.trim() || !fileName}
              size="lg"
            >
              {uploading ? (
                <>
                  <Loader className="spinner" size={18} />
                  上傳中...
                </>
              ) : (
                <>
                  <Upload size={18} />
                  上傳 Provider
                </>
              )}
            </Button>
          </div>
        </Card>
      </section>

      {/* Instructions */}
      <section className="instructions-section">
        <Card className="instructions-card">
          <div className="instructions-header">
            <AlertCircle size={24} />
            <h3>使用說明</h3>
          </div>
          <div className="instructions-content">
            <h4>如何創建自定義 Provider</h4>
            <ol className="instructions-list">
              <li>繼承 <code>BaseModel</code> 類別</li>
              <li>實作 <code>__init__</code> 方法並設定 provider 名稱</li>
              <li>實作 <code>{'async generate(prompt: str) -> str'}</code> 方法</li>
              <li>可選：實作 <code>generate_with_retry</code> 方法來處理重試邏輯</li>
              <li>上傳後，系統會自動儲存到 <code>plugins/</code> 目錄並載入</li>
            </ol>

            <h4>範例代碼</h4>
            <pre className="example-code">{`from src.target.base_model import BaseModel
import httpx

class MyCustomModel(BaseModel):
    def __init__(self, model_name: str, api_key: str = None, **kwargs):
        super().__init__(model_name, provider='my_custom')
        self.api_key = api_key
        self.endpoint = "https://api.example.com/generate"
        
    async def generate(self, prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.endpoint,
                json={"prompt": prompt, "model": self.model_name},
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return response.json()["text"]`}</pre>
          </div>
        </Card>
      </section>
    </div>
  );
};
