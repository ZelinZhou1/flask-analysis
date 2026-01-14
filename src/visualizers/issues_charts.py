# -*- coding: utf-8 -*-
"""
Issue和PR可视化模块
生成Issue状态分布、标签分布等图表
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List, Dict, Any

from src.config import OUTPUT_DIR, WARM_COLORS, WARM_PALETTE
from src.visualizers.style import apply_style, save_plot


def plot_issue_status_distribution(issues_data: List[Dict[str, Any]]) -> None:
    """
    绘制Issue状态分布 (Open vs Closed)

    Args:
        issues_data: Issue数据列表
    """
    apply_style()

    if not issues_data:
        print("没有Issue数据，跳过绘制。")
        return

    df = pd.DataFrame(issues_data)
    if "state" not in df.columns:
        return

    status_counts = df["state"].value_counts()

    plt.figure(figsize=(8, 8))

    # 饼图颜色
    colors = [WARM_COLORS["primary"], WARM_COLORS["tertiary"]]

    plt.pie(
        status_counts,
        labels=status_counts.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        textprops={"color": WARM_COLORS["dark"], "fontsize": 12, "weight": "bold"},
        wedgeprops={"edgecolor": WARM_COLORS["background"], "linewidth": 2},
    )

    output_path = OUTPUT_DIR / "issue_status_dist.png"
    save_plot(str(output_path), "Issue 状态分布")


def plot_issue_labels(issues_data: List[Dict[str, Any]], top_n: int = 10) -> None:
    """
    绘制热门Issue标签排行

    Args:
        issues_data: Issue数据列表
    """
    apply_style()

    if not issues_data:
        return

    # 提取所有标签
    all_labels = []
    for issue in issues_data:
        labels = issue.get("labels", [])
        # 处理labels可能是字符串列表或对象列表的情况
        if labels and isinstance(labels[0], dict):
            all_labels.extend([l.get("name") for l in labels])
        else:
            all_labels.extend(labels)

    if not all_labels:
        return

    from collections import Counter

    label_counts = Counter(all_labels).most_common(top_n)

    labels, counts = zip(*label_counts)

    plt.figure(figsize=(12, 6))

    sns.barplot(
        x=list(counts), y=list(labels), palette=WARM_PALETTE[: len(labels)], orient="h"
    )

    plt.xlabel("数量", fontsize=12)
    plt.ylabel("标签", fontsize=12)

    output_path = OUTPUT_DIR / "issue_labels.png"
    save_plot(str(output_path), f"热门 Issue 标签 Top {top_n}")


def plot_issue_creation_history(issues_data: List[Dict[str, Any]]) -> None:
    """
    绘制Issue创建时间线

    Args:
        issues_data: Issue数据列表
    """
    apply_style()

    if not issues_data:
        return

    df = pd.DataFrame(issues_data)
    if "created_at" not in df.columns:
        return

    # 转换日期并按月聚合
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["month_year"] = df["created_at"].dt.to_period("M")

    counts = df.groupby("month_year").size()
    # 转换索引为字符串以便绘图
    counts.index = counts.index.astype(str)

    plt.figure(figsize=(14, 6))

    sns.lineplot(
        x=counts.index,
        y=counts.values,
        marker="o",
        color=WARM_COLORS["secondary"],
        linewidth=2,
    )

    # 减少X轴标签密度
    plt.xticks(rotation=45, ha="right")
    ax = plt.gca()
    # 简单的稀疏化逻辑：每隔n个显示一个
    n = max(len(counts) // 20, 1)
    for index, label in enumerate(ax.xaxis.get_ticklabels()):
        if index % n != 0:
            label.set_visible(False)

    plt.ylabel("新 Issue 数量", fontsize=12)
    plt.xlabel("时间", fontsize=12)

    output_path = OUTPUT_DIR / "issue_history.png"
    save_plot(str(output_path), "Issue 创建趋势")
