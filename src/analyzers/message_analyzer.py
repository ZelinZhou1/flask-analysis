# -*- coding: utf-8 -*-
"""
提交消息分析模块
分析Git提交消息的模式和关键词
"""
import re
from collections import Counter
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


# 提交类型分类规则
COMMIT_TYPES = {
    "feat": ["feat", "feature", "add", "new", "implement"],
    "fix": ["fix", "bug", "hotfix", "patch", "resolve", "repair"],
    "docs": ["doc", "docs", "readme", "documentation", "comment"],
    "refactor": ["refactor", "restructure", "rewrite", "clean", "simplify"],
    "test": ["test", "testing", "spec", "coverage"],
    "chore": ["chore", "update", "upgrade", "build", "ci", "config"],
    "style": ["style", "format", "lint", "whitespace", "typo"],
    "perf": ["perf", "performance", "optimize", "speed"],
}


def classify_commit(message: str) -> str:
    """
    根据消息内容分类提交类型
    
    Args:
        message: 提交消息
        
    Returns:
        提交类型
    """
    msg_lower = message.lower()
    
    # 检查是否有Conventional Commits前缀
    prefix_match = re.match(r'^(\w+)[:\(]', msg_lower)
    if prefix_match:
        prefix = prefix_match.group(1)
        for commit_type, keywords in COMMIT_TYPES.items():
            if prefix in keywords:
                return commit_type
    
    # 关键词匹配
    for commit_type, keywords in COMMIT_TYPES.items():
        for keyword in keywords:
            if keyword in msg_lower:
                return commit_type
    
    return "other"


def analyze_messages(messages: List[str]) -> Dict[str, Any]:
    """
    分析提交消息列表
    
    Args:
        messages: 消息列表
        
    Returns:
        分析结果
    """
    type_counts = Counter()
    word_counts = Counter()
    length_sum = 0
    
    for msg in messages:
        # 分类
        commit_type = classify_commit(msg)
        type_counts[commit_type] += 1
        
        # 长度统计
        length_sum += len(msg)
        
        # 词频统计（简单分词）
        words = re.findall(r'\b[a-zA-Z]{3,}\b', msg.lower())
        word_counts.update(words)
    
    # 移除常见无意义词
    stopwords = {"the", "and", "for", "with", "from", "this", "that", "into"}
    for sw in stopwords:
        word_counts.pop(sw, None)
    
    return {
        "total_commits": len(messages),
        "type_distribution": dict(type_counts),
        "average_length": length_sum / len(messages) if messages else 0,
        "top_words": word_counts.most_common(30),
        "type_percentages": {
            k: round(v / len(messages) * 100, 1) 
            for k, v in type_counts.items()
        } if messages else {},
    }


def get_message_patterns(messages: List[str]) -> Dict[str, int]:
    """
    分析消息模式
    
    Args:
        messages: 消息列表
        
    Returns:
        模式统计
    """
    patterns = {
        "conventional": 0,  # feat: / fix: 格式
        "imperative": 0,    # Add / Fix 开头
        "past_tense": 0,    # Added / Fixed
        "with_issue": 0,    # 包含 #123
        "merge": 0,         # Merge pull request
        "other": 0,
    }
    
    for msg in messages:
        if re.match(r'^(feat|fix|docs|chore|refactor|test|style)[:\(]', msg, re.I):
            patterns["conventional"] += 1
        elif re.match(r'^(Add|Fix|Update|Remove|Improve|Implement)\s', msg):
            patterns["imperative"] += 1
        elif re.match(r'^(Added|Fixed|Updated|Removed|Improved|Implemented)\s', msg):
            patterns["past_tense"] += 1
        elif re.search(r'#\d+', msg):
            patterns["with_issue"] += 1
        elif msg.lower().startswith("merge"):
            patterns["merge"] += 1
        else:
            patterns["other"] += 1
    
    return patterns


def extract_referenced_issues(messages: List[str]) -> List[int]:
    """
    提取消息中引用的Issue编号
    
    Args:
        messages: 消息列表
        
    Returns:
        Issue编号列表
    """
    issues = []
    for msg in messages:
        matches = re.findall(r'#(\d+)', msg)
        issues.extend([int(m) for m in matches])
    return sorted(set(issues))
