# -*- coding: utf-8 -*-
"""
提交消息类型图表
可视化提交类型分布
"""
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, List
import logging

from src.visualizers.style import apply_style, save_plot, get_palette, get_color

logger = logging.getLogger(__name__)


def plot_commit_types_pie(
    type_counts: Dict[str, int],
    output_path: str,
    title: str = "提交类型分布",
) -> None:
    """
    绘制提交类型饼图
    
    Args:
        type_counts: 类型计数字典
        output_path: 输出路径
        title: 图表标题
    """
    apply_style()
    
    if not type_counts:
        logger.warning("没有提交类型数据")
        return
    
    # 按数量排序
    sorted_items = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
    types = [item[0] for item in sorted_items]
    counts = [item[1] for item in sorted_items]
    
    plt.figure(figsize=(10, 8))
    
    colors = get_palette()
    if len(colors) < len(types):
        colors = colors * (len(types) // len(colors) + 1)
    
    wedges, texts, autotexts = plt.pie(
        counts,
        labels=types,
        autopct="%1.1f%%",
        colors=colors[:len(types)],
        startangle=90,
        pctdistance=0.8,
        labeldistance=1.1,
    )
    
    # 设置标签样式
    for autotext in autotexts:
        autotext.set_fontsize(9)
    
    plt.legend(wedges, types, title="提交类型", loc="center left", bbox_to_anchor=(1, 0.5))
    
    save_plot(output_path, title)


def plot_commit_types_bar(
    type_counts: Dict[str, int],
    output_path: str,
    title: str = "提交类型统计",
) -> None:
    """
    绘制提交类型柱状图
    
    Args:
        type_counts: 类型计数字典
        output_path: 输出路径
        title: 图表标题
    """
    apply_style()
    
    if not type_counts:
        logger.warning("没有提交类型数据")
        return
    
    # 按数量排序
    sorted_items = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
    types = [item[0] for item in sorted_items]
    counts = [item[1] for item in sorted_items]
    
    plt.figure(figsize=(12, 6))
    
    colors = get_palette()
    bars = plt.bar(types, counts, color=colors[:len(types)])
    
    plt.xlabel("提交类型")
    plt.ylabel("提交数量")
    plt.xticks(rotation=45, ha="right")
    
    # 添加数值标签
    for bar, count in zip(bars, counts):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            str(count),
            ha="center",
            va="bottom",
            fontsize=9,
        )
    
    save_plot(output_path, title)


def plot_message_length_dist(
    messages: List[str],
    output_path: str,
    title: str = "提交消息长度分布",
) -> None:
    """
    绘制提交消息长度分布直方图
    
    Args:
        messages: 消息列表
        output_path: 输出路径
        title: 图表标题
    """
    apply_style()
    
    if not messages:
        logger.warning("没有消息数据")
        return
    
    lengths = [len(msg) for msg in messages]
    
    plt.figure(figsize=(12, 6))
    
    plt.hist(lengths, bins=30, color=get_color("primary"), edgecolor="white", alpha=0.8)
    
    plt.xlabel("消息长度（字符）")
    plt.ylabel("频次")
    plt.axvline(x=sum(lengths) / len(lengths), color=get_color("dark"), linestyle="--", label=f"平均: {sum(lengths) / len(lengths):.0f}")
    plt.legend()
    
    save_plot(output_path, title)
