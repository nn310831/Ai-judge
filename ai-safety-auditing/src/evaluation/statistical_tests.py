"""
統計檢定：比較不同模型的安全性表現
"""

from typing import Dict, List, Any, Tuple
import numpy as np
from scipy import stats


class StatisticalTests:
    """統計檢定工具類"""
    
    @staticmethod
    def independent_t_test(
        scores_a: List[float],
        scores_b: List[float],
        alpha: float = 0.05
    ) -> Dict[str, Any]:
        """
        獨立樣本 t 檢定：比較兩組分數是否有顯著差異
        
        Args:
            scores_a: 第一組分數
            scores_b: 第二組分數
            alpha: 顯著水準（預設 0.05）
        
        Returns:
            檢定結果字典
        """
        # 移除 None 值
        scores_a = [s for s in scores_a if s is not None]
        scores_b = [s for s in scores_b if s is not None]
        
        if len(scores_a) < 2 or len(scores_b) < 2:
            return {
                "test": "independent_t_test",
                "error": "樣本數不足（需要至少 2 個）"
            }
        
        # 執行 t 檢定
        t_statistic, p_value = stats.ttest_ind(scores_a, scores_b)
        
        # 計算效果量（Cohen's d）
        cohens_d = StatisticalTests.cohens_d(scores_a, scores_b)
        
        return {
            "test": "independent_t_test",
            "t_statistic": float(t_statistic),
            "p_value": float(p_value),
            "alpha": alpha,
            "is_significant": p_value < alpha,
            "cohens_d": cohens_d,
            "interpretation": StatisticalTests._interpret_cohens_d(cohens_d),
            "sample_sizes": {
                "group_a": len(scores_a),
                "group_b": len(scores_b)
            },
            "means": {
                "group_a": float(np.mean(scores_a)),
                "group_b": float(np.mean(scores_b))
            }
        }
    
    @staticmethod
    def paired_t_test(
        scores_a: List[float],
        scores_b: List[float],
        alpha: float = 0.05
    ) -> Dict[str, Any]:
        """
        配對樣本 t 檢定：比較同一組樣本在兩種條件下的分數
        
        Args:
            scores_a: 第一組分數
            scores_b: 第二組分數（需與 scores_a 配對）
            alpha: 顯著水準
        
        Returns:
            檢定結果字典
        """
        # 移除配對中任一為 None 的資料
        paired_data = [(a, b) for a, b in zip(scores_a, scores_b) if a is not None and b is not None]
        
        if len(paired_data) < 2:
            return {
                "test": "paired_t_test",
                "error": "配對樣本數不足"
            }
        
        scores_a, scores_b = zip(*paired_data)
        
        # 執行配對 t 檢定
        t_statistic, p_value = stats.ttest_rel(scores_a, scores_b)
        
        return {
            "test": "paired_t_test",
            "t_statistic": float(t_statistic),
            "p_value": float(p_value),
            "alpha": alpha,
            "is_significant": p_value < alpha,
            "sample_size": len(paired_data),
            "mean_difference": float(np.mean(np.array(scores_a) - np.array(scores_b)))
        }
    
    @staticmethod
    def anova_test(
        scores_dict: Dict[str, List[float]],
        alpha: float = 0.05
    ) -> Dict[str, Any]:
        """
        單因子變異數分析（ANOVA）：比較多組分數
        
        Args:
            scores_dict: 分數字典，key 為組別名稱，value 為分數列表
            alpha: 顯著水準
        
        Returns:
            ANOVA 結果字典
        """
        # 準備資料
        groups = []
        group_names = []
        
        for name, scores in scores_dict.items():
            clean_scores = [s for s in scores if s is not None]
            if len(clean_scores) >= 2:
                groups.append(clean_scores)
                group_names.append(name)
        
        if len(groups) < 2:
            return {
                "test": "anova",
                "error": "至少需要 2 組資料"
            }
        
        # 執行 ANOVA
        f_statistic, p_value = stats.f_oneway(*groups)
        
        # 計算組間平均數
        group_means = {name: float(np.mean(scores)) for name, scores in zip(group_names, groups)}
        
        result = {
            "test": "anova",
            "f_statistic": float(f_statistic),
            "p_value": float(p_value),
            "alpha": alpha,
            "is_significant": p_value < alpha,
            "group_means": group_means,
            "group_sizes": {name: len(scores) for name, scores in zip(group_names, groups)}
        }
        
        # 如果顯著，進行事後檢定（Tukey HSD）
        if p_value < alpha and len(groups) > 2:
            result["post_hoc"] = StatisticalTests._tukey_hsd(groups, group_names)
        
        return result
    
    @staticmethod
    def cohens_d(scores_a: List[float], scores_b: List[float]) -> float:
        """
        計算 Cohen's d 效果量
        
        Args:
            scores_a: 第一組分數
            scores_b: 第二組分數
        
        Returns:
            Cohen's d 值
        """
        mean_a = np.mean(scores_a)
        mean_b = np.mean(scores_b)
        
        std_a = np.std(scores_a, ddof=1)
        std_b = np.std(scores_b, ddof=1)
        
        n_a = len(scores_a)
        n_b = len(scores_b)
        
        # 合併標準差
        pooled_std = np.sqrt(((n_a - 1) * std_a**2 + (n_b - 1) * std_b**2) / (n_a + n_b - 2))
        
        # Cohen's d
        d = (mean_a - mean_b) / pooled_std
        
        return float(d)
    
    @staticmethod
    def _interpret_cohens_d(d: float) -> str:
        """解釋 Cohen's d 效果量"""
        abs_d = abs(d)
        
        if abs_d < 0.2:
            return "negligible (可忽略)"
        elif abs_d < 0.5:
            return "small (小)"
        elif abs_d < 0.8:
            return "medium (中)"
        else:
            return "large (大)"
    
    @staticmethod
    def _tukey_hsd(groups: List[List[float]], group_names: List[str]) -> List[Dict[str, Any]]:
        """
        Tukey HSD 事後檢定
        
        Args:
            groups: 分數組列表
            group_names: 組名列表
        
        Returns:
            配對比較結果列表
        """
        from itertools import combinations
        
        results = []
        
        for (name_a, scores_a), (name_b, scores_b) in combinations(zip(group_names, groups), 2):
            # 使用 scipy.stats.tukey_hsd 或簡化版本
            mean_diff = abs(np.mean(scores_a) - np.mean(scores_b))
            
            # 簡化的 Tukey HSD（實務上應使用完整公式）
            t_result = stats.ttest_ind(scores_a, scores_b)
            
            results.append({
                "comparison": f"{name_a} vs {name_b}",
                "mean_difference": float(mean_diff),
                "p_value": float(t_result.pvalue),
                "is_significant": t_result.pvalue < 0.05
            })
        
        return results
    
    @staticmethod
    def mann_whitney_u_test(
        scores_a: List[float],
        scores_b: List[float],
        alpha: float = 0.05
    ) -> Dict[str, Any]:
        """
        Mann-Whitney U 檢定（非參數檢定）
        適用於非常態分佈的資料
        
        Args:
            scores_a: 第一組分數
            scores_b: 第二組分數
            alpha: 顯著水準
        
        Returns:
            檢定結果字典
        """
        scores_a = [s for s in scores_a if s is not None]
        scores_b = [s for s in scores_b if s is not None]
        
        if len(scores_a) < 2 or len(scores_b) < 2:
            return {
                "test": "mann_whitney_u",
                "error": "樣本數不足"
            }
        
        u_statistic, p_value = stats.mannwhitneyu(scores_a, scores_b, alternative='two-sided')
        
        return {
            "test": "mann_whitney_u",
            "u_statistic": float(u_statistic),
            "p_value": float(p_value),
            "alpha": alpha,
            "is_significant": p_value < alpha,
            "sample_sizes": {
                "group_a": len(scores_a),
                "group_b": len(scores_b)
            },
            "medians": {
                "group_a": float(np.median(scores_a)),
                "group_b": float(np.median(scores_b))
            }
        }
    
    @staticmethod
    def chi_square_test(
        observed_a: List[int],
        observed_b: List[int],
        alpha: float = 0.05
    ) -> Dict[str, Any]:
        """
        卡方檢定：比較兩組類別資料的分佈
        例如：比較兩個模型的安全/不安全分佈
        
        Args:
            observed_a: 第一組觀察頻率（例如 [安全數, 不安全數]）
            observed_b: 第二組觀察頻率
            alpha: 顯著水準
        
        Returns:
            卡方檢定結果
        """
        # 構建列聯表
        contingency_table = np.array([observed_a, observed_b])
        
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        
        return {
            "test": "chi_square",
            "chi2_statistic": float(chi2),
            "p_value": float(p_value),
            "degrees_of_freedom": int(dof),
            "alpha": alpha,
            "is_significant": p_value < alpha,
            "observed": {
                "group_a": observed_a,
                "group_b": observed_b
            },
            "expected": expected.tolist()
        }
