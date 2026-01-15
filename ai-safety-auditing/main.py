"""
主程式：不使用API,完整的 AI 安全審計流程
"""

import json
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

from src.generator.attack_generator import AttackGenerator
from src.target.config_manager import ConfigManager
from src.judge.safety_judge import SafetyJudge
from src.evaluation.metrics import MetricsCalculator

# 檢查是否有 tqdm
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    print("⚠️  未安裝 tqdm，進度條將不顯示")
    print("   執行：pip install tqdm")


def main():
    """主程式：完整的 Red Team 測試流程"""
    
    print("\n" + "=" * 70)
    print("🚀 AI Safety Auditing System")
    print("   Responsible AI Red Team Testing")
    print("=" * 70 + "\n")
    
    # ==================== 第 1 步：生成攻擊提示詞 ====================
    print("📝 步驟 1/5: 生成攻擊提示詞")
    print("-" * 70)
    
    generator = AttackGenerator()
    
    # 生成攻擊（可調整參數）
    attacks = generator.generate_attacks(
        category="all",      # "all" 或指定類別
        count=20,            # 每個類別的數量
        use_llm=True         # 使用 LLM 生成（False 則用模板）
    )
    
    print(f"✅ 已生成 {len(attacks)} 個攻擊提示詞")
    print(f"   類別分布:")
    
    # 顯示類別分布
    from collections import Counter
    categories = Counter([a['category'] for a in attacks])
    for cat, count in categories.items():
        print(f"     - {cat}: {count}")
    
    # 儲存攻擊
    attacks_file = Path("data/attacks/generated_attacks.json")
    attacks_file.parent.mkdir(parents=True, exist_ok=True)
    generator.save_attacks(attacks, str(attacks_file))
    
    # ==================== 第 2 步：載入目標模型 ====================
    print(f"\n🎯 步驟 2/5: 載入目標模型")
    print("-" * 70)
    
    # 檢查配置檔是否存在
    config_file = Path("config/models_config.json")
    if not config_file.exists():
        print("⚠️  配置檔不存在，使用範例配置...")
        example_file = Path("config/models_config.example.json")
        if example_file.exists():
            import shutil
            shutil.copy(example_file, config_file)
            print(f"✅ 已複製範例配置至 {config_file}")
            print(f"⚠️  請編輯配置檔並設定 API Keys")
        else:
            print("❌ 找不到範例配置檔")
            return
    
    config_manager = ConfigManager(str(config_file))
    target_models = config_manager.load_and_create_models()
    
    if not target_models:
        print("❌ 沒有可用的模型，請檢查配置檔")
        return
    
    print(f"✅ 已載入 {len(target_models)} 個目標模型:")
    for model in target_models:
        print(f"   - {model.model_name}")
    
    # ==================== 第 3 步：初始化 Judge ====================
    print(f"\n⚖️  步驟 3/5: 初始化 Judge 系統")
    print("-" * 70)
    
    judge = SafetyJudge()
    print(f"✅ Judge 已就緒")
    print(f"   模型: {judge.model}")
    print(f"   溫度: {judge.temperature}")
    
    # ==================== 第 4 步：執行批量測試 ====================
    print(f"\n🧪 步驟 4/5: 執行批量測試")
    print("-" * 70)
    
    total_tests = len(attacks) * len(target_models)
    print(f"總測試數: {total_tests}")
    print(f"預估時間: {total_tests * 3 / 60:.1f} 分鐘（約每個測試 3 秒）\n")
    
    all_results = []
    
    # 創建進度條
    if HAS_TQDM:
        pbar = tqdm(total=total_tests, desc="測試進度")
    
    for model_idx, model in enumerate(target_models):
        print(f"\n測試模型 {model_idx+1}/{len(target_models)}: {model.model_name}")
        model_results = []
        
        for attack_idx, attack in enumerate(attacks):
            # 呼叫目標模型
            response = model.generate_with_retry(attack["prompt"])
            
            # Judge 評分
            if response.get("success"):
                evaluation = judge.evaluate(
                    attack["prompt"],
                    response.get("response", "")
                )
            else:
                # 如果模型呼叫失敗，記錄錯誤
                evaluation = {
                    "score": None,
                    "is_safe": None,
                    "reasoning": f"模型呼叫失敗: {response.get('error')}",
                    "error": response.get("error")
                }
            
            # 記錄結果
            result = {
                "timestamp": datetime.now().isoformat(),
                "model": model.model_name,
                "attack_id": attack["id"],
                "attack_category": attack["category"],
                "attack_prompt": attack["prompt"],
                "model_response": response.get("response"),
                "evaluation": evaluation,
                "latency_ms": response.get("latency_ms", 0),
                "success": response.get("success", False)
            }
            
            model_results.append(result)
            all_results.append(result)
            
            # 更新進度條
            if HAS_TQDM:
                pbar.set_postfix({
                    "模型": model.model_name[:20],
                    "分數": evaluation.get("score", "N/A")
                })
                pbar.update(1)
            else:
                # 簡單的進度顯示
                if (attack_idx + 1) % 5 == 0:
                    print(f"  進度: {attack_idx+1}/{len(attacks)}")
    
    if HAS_TQDM:
        pbar.close()
    
    print(f"\n✅ 測試完成！共 {len(all_results)} 個測試")
    
    # ==================== 第 5 步：計算指標與儲存 ====================
    print(f"\n📊 步驟 5/5: 計算評估指標")
    print("-" * 70)
    
    # 整體指標
    overall_evals = [r["evaluation"] for r in all_results]
    overall_metrics = MetricsCalculator.calculate_all_metrics(overall_evals)
    
    # 按模型分組計算
    results_by_model = {}
    for model in target_models:
        model_results = [
            r for r in all_results 
            if r["model"] == model.model_name
        ]
        results_by_model[model.model_name] = [r["evaluation"] for r in model_results]
    
    model_comparison = MetricsCalculator.compare_models(results_by_model)
    
    # 按攻擊類別計算
    category_metrics = MetricsCalculator.calculate_category_metrics(
        [r["evaluation"] for r in all_results if "attack_category" in r]
    )
    
    # ==================== 儲存結果 ====================
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path("data/results")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. 儲存詳細結果
    detailed_file = results_dir / f"detailed_results_{timestamp}.json"
    with open(detailed_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    # 2. 儲存指標摘要
    # 儲存測試配置和整體指標
    metrics_summary = {
        "timestamp": timestamp,
        "config": {
            "total_attacks": len(attacks),
            "total_models": len(target_models),
            "total_tests": total_tests,
            "generator_model": generator.model,
            "judge_model": judge.model
        },
        "overall_metrics": overall_metrics,
        "model_comparison": model_comparison,
        "category_metrics": category_metrics
    }
    
    summary_file = results_dir / f"metrics_summary_{timestamp}.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(metrics_summary, f, indent=2, ensure_ascii=False)
    
    # ==================== 顯示結果摘要 ====================
    print("\n" + "=" * 70)
    print("📊 測試結果摘要")
    print("=" * 70)
    
    print(f"\n整體表現：")
    print(f"  攻擊成功率 (ASR): {overall_metrics['asr']:.2%}")
    print(f"  平均安全分數: {overall_metrics['average_score']:.2f}/5.0")
    print(f"  拒絕率: {overall_metrics['refusal_rate']:.2%}")
    
    print(f"\n各模型表現：")
    for model_name, metrics in model_comparison["by_model"].items():
        print(f"\n  {model_name}:")
        print(f"    ASR: {metrics['asr']:.2%}")
        print(f"    平均分數: {metrics['average_score']:.2f}/5.0")
        print(f"    拒絕率: {metrics['refusal_rate']:.2%}")
    
    print(f"\n模型排名（依 ASR，越低越好）：")
    for i, (model, asr) in enumerate(model_comparison["ranking"]["by_asr"], 1):
        print(f"  {i}. {model}: {asr}")
    
    print(f"\n各攻擊類別表現：")
    for category, metrics in category_metrics.items():
        print(f"  {category}: ASR={metrics['asr']:.2%}, 平均分數={metrics['avg_score']:.2f}")
    
    print("\n" + "=" * 70)
    print("💾 結果已儲存:")
    print(f"   詳細結果: {detailed_file}")
    print(f"   指標摘要: {summary_file}")
    print("=" * 70)
    
    print("\n✨ 測試完成！")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  測試被使用者中斷")
    except Exception as e:
        print(f"\n\n❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
