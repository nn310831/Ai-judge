"""
資料處理：JSON 儲存/載入、CSV 匯出等
"""

import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


class DataHandler:
    """資料處理工具類"""
    
    @staticmethod
    def save_json(
        data: Any,
        file_path: str,
        indent: int = 2,
        ensure_ascii: bool = False
    ) -> None:
        """
        儲存資料為 JSON 格式
        
        Args:
            data: 要儲存的資料
            file_path: 檔案路徑
            indent: 縮排空格數
            ensure_ascii: 是否強制 ASCII 編碼
        """
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)
    
    @staticmethod
    def load_json(file_path: str) -> Any:
        """
        從 JSON 檔案載入資料
        
        Args:
            file_path: 檔案路徑
        
        Returns:
            載入的資料
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def export_to_csv(
        data: List[Dict[str, Any]],
        file_path: str,
        fieldnames: Optional[List[str]] = None
    ) -> None:
        """
        匯出資料為 CSV 格式
        
        Args:
            data: 資料列表（每個元素是字典）
            file_path: CSV 檔案路徑
            fieldnames: 欄位名稱（None 則自動從第一筆資料取得）
        """
        if not data:
            raise ValueError("資料不能為空")
        
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # 自動取得欄位名稱
        if fieldnames is None:
            fieldnames = list(data[0].keys())
        
        with open(path, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    
    @staticmethod
    def flatten_results_for_csv(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        將嵌套的測試結果扁平化以便匯出 CSV
        
        Args:
            results: 測試結果列表
        
        Returns:
            扁平化的資料列表
        """
        flat_results = []
        
        for result in results:
            flat_row = {
                "timestamp": result.get("timestamp"),
                "model": result.get("model"),
                "attack_id": result.get("attack_id"),
                "attack_category": result.get("attack_category"),
                "attack_prompt": result.get("attack_prompt", "")[:100],  # 截斷
                "model_response": result.get("model_response", "")[:200],  # 截斷
                "latency_ms": result.get("latency_ms"),
                "success": result.get("success"),
            }
            
            # 展開 evaluation 欄位
            evaluation = result.get("evaluation", {})
            flat_row.update({
                "eval_score": evaluation.get("score"),
                "eval_is_safe": evaluation.get("is_safe"),
                "eval_reasoning": evaluation.get("reasoning", "")[:200],
                "eval_refusal_detected": evaluation.get("refusal_detected"),
            })
            
            flat_results.append(flat_row)
        
        return flat_results
    
    @staticmethod
    def create_backup(file_path: str) -> str:
        """
        為檔案創建備份（加上時間戳記）
        
        Args:
            file_path: 要備份的檔案路徑
        
        Returns:
            備份檔案路徑
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"檔案不存在: {file_path}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.parent / f"{path.stem}_backup_{timestamp}{path.suffix}"
        
        import shutil
        shutil.copy2(path, backup_path)
        
        return str(backup_path)
    
    @staticmethod
    def merge_json_files(
        file_paths: List[str],
        output_path: str
    ) -> None:
        """
        合併多個 JSON 檔案（假設是列表）
        
        Args:
            file_paths: 要合併的 JSON 檔案路徑列表
            output_path: 輸出檔案路徑
        """
        merged_data = []
        
        for file_path in file_paths:
            data = DataHandler.load_json(file_path)
            if isinstance(data, list):
                merged_data.extend(data)
            else:
                merged_data.append(data)
        
        DataHandler.save_json(merged_data, output_path)
