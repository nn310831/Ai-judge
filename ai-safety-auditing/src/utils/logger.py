"""
日誌系統：結構化日誌記錄
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


def setup_logger(
    name: str,
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_dir: str = "logs"
) -> logging.Logger:
    """
    設定日誌系統
    
    Args:
        name: Logger 名稱
        log_level: 日誌等級 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: 日誌檔案名稱（None 則不寫入檔案）
        log_dir: 日誌目錄
    
    Returns:
        配置好的 Logger
    """
    
    # 創建 logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # 避免重複添加 handler
    if logger.handlers:
        return logger
    
    # 創建格式化器
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File Handler（可選）
    if log_file:
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        
        # 添加時間戳記到檔案名
        timestamp = datetime.now().strftime("%Y%m%d")
        file_name = f"{timestamp}_{log_file}"
        file_path = log_path / file_name
        
        file_handler = logging.FileHandler(file_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # 檔案記錄所有級別
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# 預設 logger
default_logger = setup_logger("ai_safety_auditing")
