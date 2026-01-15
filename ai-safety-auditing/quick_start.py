"""
快速開始腳本：幫助新使用者快速設定專案
"""

import os
import shutil
from pathlib import Path


def print_header(text: str):
    """印出標題"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_step(step: int, text: str):
    """印出步驟"""
    print(f"\n📌 步驟 {step}: {text}")
    print("-" * 70)


def quick_start():
    """快速開始設定流程"""
    
    print_header("🚀 AI Safety Auditing System - 快速開始")
    
    print("""
這個腳本將幫助你：
  1. 設定環境變數
  2. 創建配置檔
  3. 準備資料目錄
  4. 檢查相依套件
  5. 執行測試運行
    """)
    
    # ==================== 步驟 1：檢查環境變數 ====================
    print_step(1, "檢查環境變數")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        print("❌ .env 檔案不存在")
        
        if env_example.exists():
            print("✅ 找到 .env.example，正在複製...")
            shutil.copy(env_example, env_file)
            print(f"✅ 已創建 .env 檔案")
        else:
            print("⚠️  .env.example 也不存在，創建空白 .env")
            with open(env_file, 'w') as f:
                f.write("# API Keys\n")
                f.write("OPENAI_API_KEY=your_openai_key_here\n")
                f.write("ANTHROPIC_API_KEY=your_anthropic_key_here\n")
        
        print("\n⚠️  請編輯 .env 檔案並填入你的 API Keys:")
        print(f"   nano {env_file}  或  code {env_file}")
        
        response = input("\n已設定好 API Keys 了嗎? (y/n): ")
        if response.lower() != 'y':
            print("請設定好 API Keys 後再執行此腳本")
            return
    else:
        print("✅ .env 檔案已存在")
    
    # ==================== 步驟 2：檢查配置檔 ====================
    print_step(2, "檢查模型配置檔")
    
    config_file = Path("config/models_config.json")
    config_example = Path("config/models_config.example.json")
    
    if not config_file.exists():
        print("❌ models_config.json 不存在")
        
        if config_example.exists():
            print("✅ 找到範例配置，正在複製...")
            shutil.copy(config_example, config_file)
            print(f"✅ 已創建 {config_file}")
        else:
            print("❌ 範例配置也不存在！")
            return
    else:
        print(f"✅ {config_file} 已存在")
    
    # ==================== 步驟 3：建立目錄結構 ====================
    print_step(3, "建立資料目錄")
    
    directories = [
        "data/attacks",
        "data/results",
        "data/exports",
        "logs",
        "plugins"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ {dir_path}/")
    
    # ==================== 步驟 4：檢查相依套件 ====================
    print_step(4, "檢查 Python 套件")
    
    required_packages = {
        "openai": "OpenAI API",
        "anthropic": "Anthropic API",
        "python-dotenv": "環境變數管理",
        "tqdm": "進度條顯示",
        "numpy": "數值計算",
        "scipy": "統計分析"
    }
    
    missing_packages = []
    
    for package, description in required_packages.items():
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} ({description})")
        except ImportError:
            print(f"❌ {package} ({description}) - 未安裝")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  缺少 {len(missing_packages)} 個套件")
        print(f"執行以下命令安裝:")
        print(f"pip install {' '.join(missing_packages)}")
        
        response = input("\n現在安裝嗎? (y/n): ")
        if response.lower() == 'y':
            import subprocess
            subprocess.run(["pip", "install"] + missing_packages)
    else:
        print("\n✅ 所有必要套件都已安裝！")
    
    # ==================== 步驟 5：測試 API Keys ====================
    print_step(5, "測試 API 連接")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    # 測試 OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and openai_key != "your_openai_key_here":
        try:
            import openai
            client = openai.OpenAI(api_key=openai_key)
            # 簡單測試
            response = client.models.list()
            print("✅ OpenAI API 連接成功")
        except Exception as e:
            print(f"❌ OpenAI API 測試失敗: {e}")
    else:
        print("⚠️  OpenAI API Key 未設定")
    
    # 測試 Anthropic
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key and anthropic_key != "your_anthropic_key_here":
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=anthropic_key)
            # 簡單測試（不實際呼叫 API）
            print("✅ Anthropic API Key 已設定")
        except Exception as e:
            print(f"❌ Anthropic API 測試失敗: {e}")
    else:
        print("⚠️  Anthropic API Key 未設定")
    
    # ==================== 步驟 6：執行選項 ====================
    print_step(6, "下一步")
    
    print("""
設定完成！你可以：

  1. 執行完整測試:
     python main.py

  2. 生成攻擊提示詞:
     python -c "from src.generator import AttackGenerator; \
     gen = AttackGenerator(); \
     attacks = gen.generate_attacks('all', 5); \
     print(f'已生成 {len(attacks)} 個攻擊')"

  3. 測試單一模型:
     python -c "from src.target.config_manager import ConfigManager; \
     cm = ConfigManager('config/models_config.json'); \
     models = cm.load_and_create_models(); \
     print(models[0].generate('Hello!'))"

  4. 載入自訂外掛:
     python -c "from src.target.plugin_loader import PluginLoader; \
     loader = PluginLoader(); \
     loader.load_all_plugins()"

  5. 查看專案文件:
     cat README.md
    """)
    
    response = input("\n現在執行完整測試嗎? (y/n): ")
    if response.lower() == 'y':
        print("\n正在啟動 main.py...")
        import subprocess
        subprocess.run(["python", "main.py"])


if __name__ == "__main__":
    try:
        quick_start()
    except KeyboardInterrupt:
        print("\n\n⚠️  設定被中斷")
    except Exception as e:
        print(f"\n\n❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()
