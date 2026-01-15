# -*- coding: utf-8 -*-
"""
Issues可视化模块
生成Issues相关的图表
"""

import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict
from collections import Counter
import logging

from src.visualizers.style import apply_style, save_plot, get_palette, get_color

logger = logging.getLogger(__name__)


def plot_issues_state(issues: List[Dict], output_path: str, title: str = "Issues状态分布") -> None:
    """
    绘制Issues状态分布饼图
    """
    apply_style()
    
    if not issues:
        logger.warning("没有Issues数据")
        return
    
    states = Counter(i.get("state", "unknown") for i in issues)
    
    labels_map = {"open": "开放", "closed": "已关闭", "unknown": "未知"}
    labels = [labels_map.get(s, s) for s in states.keys()]
    values = list(states.values())
    
    plt.figure(figsize=(10, 8))
    
    colors = [get_color("primary"), get_color("secondary")]
    plt.pie(values, labels=labels, autopct="%1.1f%%", colors=colors[:len(values)], startangle=90)
    
    save_plot(output_path, title)


def plot_issues_timeline(issues: List[Dict], output_path: str, title: str = "Issues创建时间线") -> None:
    """
    绘制Issues创建时间线
    """
    apply_style()
    
    if not issues:
        logger.warning("没有Issues数据")
        return
    
    df = pd.DataFrame(issues)
    if "created_at" not in df.columns:
        logger.warning("缺少created_at字段")
        return
    
    df["created"] = pd.to_datetime(df["created_at"])
    df["month"] = df["created"].dt.to_period("M").astype(str)
    
    monthly = df["month"].value_counts().sort_index()
    recent = monthly.tail(36)
    
    plt.figure(figsize=(14, 6))
    
    plt.plot(range(len(recent)), recent.values, marker="o", color=get_color("primary"), linewidth=2)
    
    step = max(1, len(recent) // 12)
    ticks = range(0, len(recent), step)
    labels = [recent.index[i] for i in ticks]
    plt.xticks(list(ticks), labels, rotation=45, ha="right")
    
    plt.xlabel("月份")
    plt.ylabel("Issues数量")
    plt.grid(True, alpha=0.3)
    
    save_plot(output_path, title)


def plot_issues_labels(issues: List[Dict], output_path: str, title: str = "Issues标签分布") -> None:
    """
    绘制Issues标签分布
    """
    apply_style()
    
    if not issues:
        logger.warning("没有Issues数据")
        return
    
    label_counts = Counter()
    for issue in issues:
        labels = issue.get("labels", [])
        for label in labels:
            if isinstance(label, dict):
                label_counts[label.get("name", "unknown")] += 1
            else:
                label_counts[str(label)] += 1
    
    if not label_counts:
        logger.warning("没有标签数据")
        return
    
    top_labels = dict(label_counts.most_common(15))
    
    plt.figure(figsize=(12, 8))
    
    colors = get_palette()
    bars = plt.barh(list(top_labels.keys()), list(top_labels.values()), color=colors[:len(top_labels)])
    
    plt.xlabel("数量")
    plt.ylabel("标签")
    plt.gca().invert_yaxis()
    
    for bar, count in zip(bars, top_labels.values()):
        plt.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, str(count), va="center")
    
    save_plot(output_path, title)


def plot_top_issue_authors(issues: List[Dict], output_path: str, title: str = "Issues作者排行") -> None:
    """
    绘制Issues作者排行
    """
    apply_style()
    
    if not issues:
        logger.warning("没有Issues数据")
        return
    
    authors = Counter()
    for issue in issues:
        user = issue.get("user", {})
        if user:
            authors[user.get("login", "unknown")] += 1
    
    top_authors = dict(authors.most_common(15))
    
    plt.figure(figsize=(12, 8))
    
    colors = get_palette()
    bars = plt.barh(list(top_authors.keys()), list(top_authors.values()), color=colors[:len(top_authors)])
    
    plt.xlabel("Issues数量")
    plt.ylabel("作者")
    plt.gca().invert_yaxis()
    
    save_plot(output_path, title)
