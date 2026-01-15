# -*- coding: utf-8 -*-
"""
词云生成模块
从提交消息生成词云图
"""

import matplotlib.pyplot as plt
from collections import Counter
from typing import List, Dict
import re
import logging

try:
    from wordcloud import WordCloud
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False

from src.visualizers.style import apply_style, save_plot, get_color

logger = logging.getLogger(__name__)

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "been",
    "be", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "must", "shall", "can", "this",
    "that", "these", "those", "it", "its", "i", "we", "you", "he", "she",
    "they", "them", "fix", "add", "update", "merge", "pull", "request",
    "branch", "commit", "into", "not", "use", "using", "also", "when",
    "more", "some", "all", "new", "see", "now", "only", "just", "make",
}


def clean_text(text: str) -> str:
    """清理文本"""
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_keywords(messages: List[str], min_length: int = 3) -> Dict[str, int]:
    """从消息列表提取关键词"""
    word_counts = Counter()
    
    for msg in messages:
        cleaned = clean_text(msg)
        words = cleaned.split()
        
        for word in words:
            if len(word) >= min_length and word not in STOPWORDS:
                word_counts[word] += 1
    
    return dict(word_counts)


def generate_wordcloud(
    messages: List[str],
    output_path: str,
    title: str = "提交消息词云",
    width: int = 1600,
    height: int = 800,
) -> None:
    """
    生成词云图
    """
    apply_style()
    
    if not WORDCLOUD_AVAILABLE:
        logger.warning("wordcloud库未安装，跳过词云生成")
        return
    
    if not messages:
        logger.warning("没有消息数据")
        return
    
    all_text = " ".join([clean_text(msg) for msg in messages])
    
    words = all_text.split()
    filtered_words = [w for w in words if w not in STOPWORDS and len(w) >= 3]
    final_text = " ".join(filtered_words)
    
    if not final_text.strip():
        logger.warning("没有足够的词生成词云")
        return
    
    wordcloud = WordCloud(
        width=width,
        height=height,
        max_words=300,
        background_color="white",
        colormap="YlOrRd",
        contour_width=0,
        prefer_horizontal=0.7,
        min_font_size=8,
        max_font_size=150,
    ).generate(final_text)
    
    plt.figure(figsize=(16, 8))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    
    save_plot(output_path, title)


def generate_wordcloud_from_freq(
    word_freq: Dict[str, int],
    output_path: str,
    title: str = "关键词词云",
) -> None:
    """从词频字典生成词云"""
    apply_style()
    
    if not WORDCLOUD_AVAILABLE:
        logger.warning("wordcloud库未安装")
        return
    
    if not word_freq:
        logger.warning("词频字典为空")
        return
    
    wordcloud = WordCloud(
        width=1600,
        height=800,
        max_words=300,
        background_color="white",
        colormap="YlOrRd",
    ).generate_from_frequencies(word_freq)
    
    plt.figure(figsize=(16, 8))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    
    save_plot(output_path, title)
