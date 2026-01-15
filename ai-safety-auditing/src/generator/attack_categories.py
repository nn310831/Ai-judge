"""
攻擊類型分類定義
"""

from enum import Enum
from typing import Dict, List

class AttackCategory(Enum):
    """攻擊類型分類"""
    PROMPT_INJECTION = "prompt_injection"      # 提示詞注入
    JAILBREAK = "jailbreak"                    # 越獄
    ROLEPLAY = "roleplay"                      # 角色扮演
    SCENARIO = "scenario"                      # 情境模擬
    ENCODING = "encoding"                      # 編碼繞過
    MULTILINGUAL = "multilingual"              # 多語言攻擊
    
    @classmethod
    def get_description(cls, category) -> str:
        """取得類別描述"""
        descriptions = {
            cls.PROMPT_INJECTION: "嘗試注入惡意指令覆蓋系統提示",
            cls.JAILBREAK: "嘗試繞過模型的安全限制",
            cls.ROLEPLAY: "要求模型扮演不受限制的角色",
            cls.SCENARIO: "建構特定情境誘導危險回應",
            cls.ENCODING: "使用編碼或混淆繞過過濾",
            cls.MULTILINGUAL: "使用非英語語言繞過檢測"
        }
        return descriptions.get(category, "未知類別")
    
    @classmethod
    def list_all(cls) -> List[str]:
        """列出所有類別"""
        return [c.value for c in cls]
