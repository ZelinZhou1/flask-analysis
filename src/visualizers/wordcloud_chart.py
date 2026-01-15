# -*- coding: utf-8 -*-
"""
词云图生成模块
用于从提交消息生成词云可视化
"""
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from typing import List, Dict, Optional
import re
from pathlib import Path

from src.visualizers.style import apply_style, save_plot, get_color


# 停用词列表（常见的无意义词）
STOPWORDS_EN = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "been",
    "be", "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "shall", "can", "this", "that", "these",
    "those", "it", "its", "i", "we", "you", "he", "she", "they", "them",
    "fix", "add", "update", "merge", "pull", "request", "branch", "commit",
}


def clean_text(text: str) -> str:
    """
    清理文本，移除特殊字符
    
    Args:
        text: 原始文本
        
    Returns:
        清理后的文本
    """
    # 移除非字母数字字符（保留空格）
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    # 移除多余空格
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_keywords(messages: List[str], min_length: int = 3) -> Dict[str, int]:
    """
    从消息列表中提取关键词
    
    Args:
        messages: 提交消息列表
        min_length: 最小词长度
        
    Returns:
        词频字典
    """
    word_counts = Counter()
    
    for msg in messages:
        cleaned = clean_text(msg)
        words = cleaned.split()
        
        for word in words:
            if len(word) >= min_length and word not in STOPWORDS_EN:
                word_counts[word] += 1
    
    return dict(word_counts)


def generate_wordcloud(
    messages: List[str],
    output_path: str,
    title: str = "提交消息词云",
    width: int = 1200,
    height: int = 600,
    max_words: int = 200,
    background_color: str = "white",
) -> None:
    """
    生成词云图
    
    Args:
        messages: 提交消息列表
        output_path: 输出路径
        title: 图表标题
        width: 图片宽度
        height: 图片高度
        max_words: 最大词数
        background_color: 背景颜色
    """
    apply_style()
    
    # 合并所有消息
    all_text = " ".join([clean_text(msg) for msg in messages])
    
    # 移除停用词
    words = all_text.split()
    filtered_words = [w for w in words if w not in STOPWORDS_EN and len(w) >= 3]
    final_text = " ".join(filtered_words)
    
    if not final_text.strip():
        print("警告: 没有足够的词生成词云")
        return
    
    # 暖色系配色
    warm_colormap = "YlOrRd"  # 黄-橙-红渐变
    
    # 生成词云
    wordcloud = WordCloud(
        width=width,
        height=height,
        max_words=max_words,
        background_color=background_color,
        colormap=warm_colormap,
        contour_width=0,
        prefer_horizontal=0.7,
    ).generate(final_text)
    
    # 绘制
    plt.figure(figsize=(width / 100, height / 100))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    
    save_plot(output_path, title)


def generate_wordcloud_from_frequencies(
    word_freq: Dict[str, int],
    output_path: str,
    title: str = "关键词词云",
) -> None:
    """
    从词频字典生成词云
    
    Args:
        word_freq: 词频字典
        output_path: 输出路径
        title: 图表标题
    """
    apply_style()
    
    if not word_freq:
        print("警告: 词频字典为空")
        return
    
    wordcloud = WordCloud(
        width=1200,
        height=600,
        max_words=200,
        background_color="white",
        colormap="YlOrRd",
    ).generate_from_frequencies(word_freq)
    
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    
    save_plot(output_path, title)
