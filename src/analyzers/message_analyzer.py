import re
import logging
from typing import Dict, Any, List
from collections import Counter

# 配置日志记录器
logger = logging.getLogger(__name__)


class MessageAnalyzer:
    """
    提交消息分析器。
    用于分析 Git 提交消息的格式、类型和内容特征。
    """

    # 常规提交类型模式 (Angular convention)
    TYPE_PATTERN = re.compile(
        r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .+",
        re.IGNORECASE,
    )

    def __init__(self):
        """初始化消息分析器"""
        pass

    def classify_message(self, message: str) -> str:
        """
        分类提交消息类型。

        Args:
            message: 提交消息内容

        Returns:
            str: 提交类型 (如 feat, fix) 或 'other'
        """
        match = self.TYPE_PATTERN.match(message)
        if match:
            return match.group(1).lower()

        # 简单的关键词回退机制
        lower_msg = message.lower()
        if "merge" in lower_msg:
            return "merge"
        if "fix" in lower_msg or "bug" in lower_msg:
            return "fix"
        if "add" in lower_msg or "feat" in lower_msg or "new" in lower_msg:
            return "feat"
        if "doc" in lower_msg:
            return "docs"

        return "other"

    def analyze_structure(self, message: str) -> Dict[str, Any]:
        """
        分析消息的结构特征。

        Args:
            message: 提交消息内容

        Returns:
            Dict: 结构特征字典
        """
        lines = message.strip().splitlines()
        if not lines:
            return {"length": 0, "lines": 0, "has_body": False}

        subject = lines[0]
        body_lines = [l for l in lines[1:] if l.strip()]

        return {
            "length": len(message),
            "subject_length": len(subject),
            "line_count": len(lines),
            "has_body": len(body_lines) > 0,
            "type": self.classify_message(message),
        }

    def generate_word_cloud_data(self, messages: List[str]) -> Dict[str, int]:
        """
        生成词云数据（词频统计）。

        Args:
            messages: 提交消息列表

        Returns:
            Dict: 词频字典
        """
        words = []
        for msg in messages:
            # 简单的分词，过滤掉非字母字符
            # 实际项目中可能需要更复杂的 NLP 处理
            clean_msg = re.sub(r"[^a-zA-Z\s]", "", msg.lower())
            words.extend(clean_msg.split())

        # 过滤常用停用词（简单列表）
        stopwords = {
            "the",
            "a",
            "an",
            "to",
            "in",
            "on",
            "at",
            "for",
            "of",
            "and",
            "with",
            "is",
            "it",
            "this",
            "that",
        }
        filtered_words = [w for w in words if w not in stopwords and len(w) > 2]

        return dict(Counter(filtered_words))
