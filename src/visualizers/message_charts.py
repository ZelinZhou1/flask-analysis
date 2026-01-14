# -*- coding: utf-8 -*-
"""
提交消息可视化模块
生成提交消息词云等图表
"""

import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from pathlib import Path
from typing import List
import numpy as np
from PIL import Image

from src.config import OUTPUT_DIR, WARM_COLORS, WARM_PALETTE, FIGURE_DPI
from src.visualizers.style import apply_style, save_plot


def plot_commit_message_wordcloud(messages: List[str]) -> None:
    """
    生成提交消息词云

    Args:
        messages: 提交消息列表
    """
    apply_style()

    if not messages:
        print("没有提交消息，跳过词云绘制。")
        return

    # 组合所有文本
    text = " ".join(messages)

    # 简单清洗：去除常见Git前缀
    text = (
        text.replace("feat:", "")
        .replace("fix:", "")
        .replace("docs:", "")
        .replace("chore:", "")
        .replace("refactor:", "")
        .replace("style:", "")
        .replace("test:", "")
        .replace("merge", "")
        .replace("branch", "")
    )

    # 自定义颜色函数，从暖色调色板中随机选取
    def warm_color_func(
        word, font_size, position, orientation, random_state=None, **kwargs
    ):
        import random

        return random.choice(WARM_PALETTE)

    # 配置词云
    wc = WordCloud(
        width=1600,
        height=900,
        background_color=WARM_COLORS["background"],
        font_path="msyh.ttc",  # 尝试使用微软雅黑，如果系统没有可能回退
        max_words=200,
        color_func=warm_color_func,
        stopwords=STOPWORDS,
    )

    # 生成词云
    wc.generate(text)

    plt.figure(figsize=(16, 9))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")

    output_path = OUTPUT_DIR / "commit_wordcloud.png"

    # 手动保存，因为 save_plot 会带有一些坐标轴设置，词云不需要
    import os

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.title(
        "提交消息词云",
        pad=20,
        fontsize=20,
        fontweight="bold",
        color=WARM_COLORS["dark"],
    )
    plt.tight_layout()
    plt.savefig(
        output_path,
        dpi=FIGURE_DPI,
        bbox_inches="tight",
        facecolor=WARM_COLORS["background"],
    )
    plt.close()


def plot_message_type_distribution(types: List[str]) -> None:
    """
    绘制提交类型分布 (feat, fix, etc.)

    Args:
        types: 提交类型列表
    """
    apply_style()

    if not types:
        return

    from collections import Counter

    counts = Counter(types)

    labels = list(counts.keys())
    sizes = list(counts.values())

    # 排序以美化饼图
    sorted_pairs = sorted(zip(sizes, labels), reverse=True)
    sizes = [s for s, l in sorted_pairs]
    labels = [l for s, l in sorted_pairs]

    plt.figure(figsize=(10, 10))

    patches, texts, autotexts = plt.pie(
        sizes,
        labels=labels,
        colors=WARM_PALETTE[: len(labels)],
        autopct="%1.1f%%",
        startangle=140,
        pctdistance=0.85,
        explode=[0.05] * len(labels),  # 轻微炸开所有切片
    )

    # 调整字体颜色
    for text in texts:
        text.set_color(WARM_COLORS["dark"])
        text.set_fontsize(12)
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_weight("bold")

    # 添加中心圆，做成环形图
    centre_circle = plt.Circle((0, 0), 0.70, fc=WARM_COLORS["background"])
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    output_path = OUTPUT_DIR / "commit_types_pie.png"
    save_plot(str(output_path), "提交类型分布")
