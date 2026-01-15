"""
簡單測試：快速驗證系統各模組是否正常運作
"""

import sys
from pathlib import Path


def test_imports():
    """測試模組導入"""
    print("\n📦 測試模組導入...")
    print("-" * 70)
    
    tests = [
        ("src.generator", "AttackGenerator"),
        ("src.target", "BaseModel", "ModelRegistry", "ModelFactory"),
        ("src.judge", "SafetyJudge"),
        ("src.evaluation.metrics", "MetricsCalculator"),
        ("src.evaluation.statistical_tests", "StatisticalTests"),
        ("src.utils", "setup_logger", "DataHandler"),
    ]
    
    failed = []
    
    for test in tests:
        module_name = test[0]
        imports = test[1:]
        
        try:
            module = __import__(module_name, fromlist=imports)
            for item in imports:
                if not hasattr(module, item):
                    print(f"❌ {module_name}.{item} - 不存在")
                    failed.append(f"{module_name}.{item}")
                else:
                    print(f"✅ {module_name}.{item}")
        except ImportError as e:
            print(f"❌ {module_name} - 導入失敗: {e}")
            failed.append(module_name)
    
    return len(failed) == 0, failed


def test_generator():
    """測試攻擊生成器"""
    print("\n🎯 測試攻擊生成器...")
    print("-" * 70)
    
    try:
        from src.generator import AttackGenerator
        import os
        
        # 檢查是否有 API key
        has_api_key = bool(os.getenv("OPENAI_API_KEY"))
        
        if has_api_key:
            print("✅ 檢測到 API key，將測試 LLM 模式")
            gen = AttackGenerator()
            attacks = gen.generate_attacks(
                category="prompt_injection",
                count=2,
                use_llm=True
            )
        else:
            print("ℹ️  未設定 API key，使用模板模式測試")
            # 使用模板模式測試（不需要 API）
            gen = AttackGenerator()
            attacks = gen.generate_attacks(
                category="prompt_injection",
                count=3,
                use_llm=False  # 使用模板
            )
        
        print(f"✅ 成功生成 {len(attacks)} 個攻擊")
        print(f"   範例: {attacks[0]['prompt'][:50]}...")
        
        return True, None
    
    except Exception as e:
        print(f"❌ 失敗: {e}")
        return False, str(e)


def test_model_registry():
    """測試模型註冊系統"""
    print("\n📋 測試模型註冊系統...")
    print("-" * 70)
    
    try:
        from src.target import ModelRegistry
        
        providers = ModelRegistry.list_providers()
        print(f"✅ 已註冊 {len(providers)} 個 provider:")
        for provider in providers:
            print(f"   - {provider}")
        
        return True, None
    
    except Exception as e:
        print(f"❌ 失敗: {e}")
        return False, str(e)


def test_judge():
    """測試 Judge 系統"""
    print("\n⚖️  測試 Judge 系統...")
    print("-" * 70)
    
    try:
        from src.judge import SafetyJudge
        import os
        
        # 檢查是否有 API key
        has_api_key = bool(os.getenv("ANTHROPIC_API_KEY"))
        
        if not has_api_key:
            print("ℹ️  未設定 ANTHROPIC_API_KEY，僅測試初始化")
        
        # 只測試初始化，不實際呼叫 API
        judge = SafetyJudge()
        print(f"✅ Judge 初始化成功")
        print(f"   模型: {judge.model}")
        print(f"   溫度: {judge.temperature}")
        
        if has_api_key:
            print(f"   ✅ API key 已設定，可進行實際評估")
        else:
            print(f"   ℹ️  若要測試實際評估，請設定 ANTHROPIC_API_KEY")
        
        return True, None
    
    except Exception as e:
        print(f"❌ 失敗: {e}")
        return False, str(e)


def test_metrics():
    """測試評估指標"""
    print("\n📊 測試評估指標...")
    print("-" * 70)
    
    try:
        from src.evaluation.metrics import MetricsCalculator
        
        # 測試資料
        test_evals = [
            {"score": 1, "is_safe": False, "refusal_detected": False},
            {"score": 2, "is_safe": False, "refusal_detected": False},
            {"score": 3, "is_safe": False, "refusal_detected": False},
            {"score": 4, "is_safe": True, "refusal_detected": True},
            {"score": 5, "is_safe": True, "refusal_detected": True},
        ]
        
        asr = MetricsCalculator.calculate_asr(test_evals)
        avg_score = MetricsCalculator.calculate_average_score(test_evals)
        refusal_rate = MetricsCalculator.calculate_refusal_rate(test_evals)
        
        print(f"✅ ASR: {asr:.2%}")
        print(f"✅ 平均分數: {avg_score:.2f}")
        print(f"✅ 拒絕率: {refusal_rate:.2%}")
        
        return True, None
    
    except Exception as e:
        print(f"❌ 失敗: {e}")
        return False, str(e)


def test_statistical_tests():
    """測試統計檢定"""
    print("\n📈 測試統計檢定...")
    print("-" * 70)
    
    try:
        from src.evaluation.statistical_tests import StatisticalTests
        
        # 測試資料
        scores_a = [1.0, 2.0, 3.0, 4.0, 5.0]
        scores_b = [2.0, 3.0, 4.0, 5.0, 5.0]
        
        result = StatisticalTests.independent_t_test(scores_a, scores_b)
        
        print(f"✅ t 統計量: {result['t_statistic']:.4f}")
        print(f"✅ p 值: {result['p_value']:.4f}")
        print(f"✅ Cohen's d: {result['cohens_d']:.4f}")
        print(f"✅ 效果量: {result['interpretation']}")
        
        return True, None
    
    except Exception as e:
        print(f"❌ 失敗: {e}")
        return False, str(e)


def test_data_handler():
    """測試資料處理"""
    print("\n💾 測試資料處理...")
    print("-" * 70)
    
    try:
        from src.utils import DataHandler
        import tempfile
        import os
        
        # 建立臨時檔案測試
        test_data = {"test": "data", "number": 123}
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        
        try:
            # 測試儲存
            DataHandler.save_json(test_data, temp_path)
            print("✅ JSON 儲存成功")
            
            # 測試載入
            loaded_data = DataHandler.load_json(temp_path)
            assert loaded_data == test_data
            print("✅ JSON 載入成功")
            
            return True, None
        
        finally:
            # 清理
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    except Exception as e:
        print(f"❌ 失敗: {e}")
        return False, str(e)


def test_plugin_loader():
    """測試外掛載入器"""
    print("\n🔌 測試外掛載入器...")
    print("-" * 70)
    
    try:
        from src.target.plugin_loader import PluginLoader
        
        loader = PluginLoader()
        print(f"✅ PluginLoader 初始化成功")
        print(f"   外掛目錄: {loader.plugin_dir}")
        
        # 掃描外掛（可能沒有）
        result = loader.load_all_plugins()
        print(f"✅ 掃描完成: {result['loaded']} 個外掛已載入")
        
        return True, None
    
    except Exception as e:
        print(f"❌ 失敗: {e}")
        return False, str(e)


def test_config_file():
    """測試配置檔"""
    print("\n⚙️  測試配置檔...")
    print("-" * 70)
    
    try:
        config_file = Path("config/models_config.json")
        
        if not config_file.exists():
            print("⚠️  config/models_config.json 不存在")
            
            example_file = Path("config/models_config.example.json")
            if example_file.exists():
                print("✅ 找到範例配置檔")
                return True, "使用範例配置"
            else:
                return False, "配置檔和範例都不存在"
        
        else:
            print(f"✅ 配置檔存在: {config_file}")
            
            # 嘗試載入
            import json
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            print(f"✅ 配置有效，包含 {len(config.get('models', []))} 個模型")
            
            return True, None
    
    except Exception as e:
        print(f"❌ 失敗: {e}")
        return False, str(e)


def main():
    """執行所有測試"""
    print("\n" + "=" * 70)
    print("🧪 AI Safety Auditing System - 系統測試")
    print("=" * 70)
    
    tests = [
        ("模組導入", test_imports),
        ("攻擊生成器", test_generator),
        ("模型註冊", test_model_registry),
        ("Judge 系統", test_judge),
        ("評估指標", test_metrics),
        ("統計檢定", test_statistical_tests),
        ("資料處理", test_data_handler),
        ("外掛載入器", test_plugin_loader),
        ("配置檔", test_config_file),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            success, error = test_func()
            results.append((name, success, error))
        except Exception as e:
            results.append((name, False, str(e)))
    
    # 總結
    print("\n" + "=" * 70)
    print("📊 測試總結")
    print("=" * 70)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for name, success, error in results:
        status = "✅ 通過" if success else "❌ 失敗"
        print(f"{status} - {name}")
        if error and not success:
            print(f"       錯誤: {error}")
    
    print("\n" + "=" * 70)
    print(f"總計: {passed}/{total} 通過 ({passed/total*100:.1f}%)")
    print("=" * 70)
    
    if passed == total:
        print("\n🎉 所有測試通過！系統已準備就緒。")
        print("\n下一步:")
        print("  1. 設定 .env 檔案（API Keys）")
        print("  2. 檢查 config/models_config.json")
        print("  3. 執行: python main.py")
        return 0
    else:
        print(f"\n⚠️  {total - passed} 個測試失敗，請檢查錯誤訊息。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
