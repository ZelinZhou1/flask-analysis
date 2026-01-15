# -*- coding: utf-8 -*-
"""
Pull Requests可视化模块
生成PRs相关的图表
"""

import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict
from collections import Counter
import logging

from src.visualizers.style import apply_style, save_plot, get_palette, get_color

logger = logging.getLogger(__name__)


def plot_prs_state(prs: List[Dict], output_path: str, title: str = "PRs状态分布") -> None:
    """
    绘制PRs状态分布饼图
    """
    apply_style()
    
    if not prs:
        logger.warning("没有PRs数据")
        return
    
    states = Counter(pr.get("state", "unknown") for pr in prs)
    
    labels_map = {"open": "开放", "closed": "已关闭", "merged": "已合并", "unknown": "未知"}
    labels = [labels_map.get(s, s) for s in states.keys()]
    values = list(states.values())
    
    plt.figure(figsize=(10, 8))
    
    colors = get_palette()[:len(values)]
    plt.pie(values, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90)
    
    save_plot(output_path, title)


def plot_prs_timeline(prs: List[Dict], output_path: str, title: str = "PRs创建时间线") -> None:
    """
    绘制PRs创建时间线
    """
    apply_style()
    
    if not prs:
        logger.warning("没有PRs数据")
        return
    
    df = pd.DataFrame(prs)
    if "created_at" not in df.columns:
        logger.warning("缺少created_at字段")
        return
    
    df["created"] = pd.to_datetime(df["created_at"])
    df["month"] = df["created"].dt.to_period("M").astype(str)
    
    monthly = df["month"].value_counts().sort_index()
    recent = monthly.tail(36)
    
    plt.figure(figsize=(14, 6))
    
    plt.fill_between(range(len(recent)), recent.values, color=get_color("primary"), alpha=0.5)
    plt.plot(range(len(recent)), recent.values, color=get_color("dark"), linewidth=2)
    
    step = max(1, len(recent) // 12)
    ticks = range(0, len(recent), step)
    labels = [recent.index[i] for i in ticks]
    plt.xticks(list(ticks), labels, rotation=45, ha="right")
    
    plt.xlabel("月份")
    plt.ylabel("PRs数量")
    plt.grid(True, alpha=0.3)
    
    save_plot(output_path, title)


def plot_top_pr_authors(prs: List[Dict], output_path: str, title: str = "PRs作者排行") -> None:
    """
    绘制PRs作者排行
    """
    apply_style()
    
    if not prs:
        logger.warning("没有PRs数据")
        return
    
    authors = Counter()
    for pr in prs:
        user = pr.get("user", {})
        if user:
            authors[user.get("login", "unknown")] += 1
    
    top_authors = dict(authors.most_common(15))
    
    plt.figure(figsize=(12, 8))
    
    colors = get_palette()
    bars = plt.barh(list(top_authors.keys()), list(top_authors.values()), color=colors[:len(top_authors)])
    
    plt.xlabel("PRs数量")
    plt.ylabel("作者")
    plt.gca().invert_yaxis()
    
    for bar, count in zip(bars, top_authors.values()):
        plt.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2, str(count), va="center")
    
    save_plot(output_path, title)


def plot_pr_merge_time(prs: List[Dict], output_path: str, title: str = "PR合并时间分布") -> None:
    """
    绘制PR从创建到合并的时间分布
    """
    apply_style()
    
    if not prs:
        logger.warning("没有PRs数据")
        return
    
    merge_times = []
    for pr in prs:
        if pr.get("merged_at") and pr.get("created_at"):
            try:
                created = pd.to_datetime(pr["created_at"])
                merged = pd.to_datetime(pr["merged_at"])
                days = (merged - created).days
                if 0 <= days <= 365:
                    merge_times.append(days)
            except:
                pass
    
    if not merge_times:
        logger.warning("没有合并时间数据")
        return
    
    plt.figure(figsize=(12, 6))
    
    plt.hist(merge_times, bins=30, color=get_color("primary"), edgecolor="white", alpha=0.8)
    
    avg_time = sum(merge_times) / len(merge_times)
    plt.axvline(x=avg_time, color=get_color("dark"), linestyle="--", label=f"平均: {avg_time:.1f}天")
    
    plt.xlabel("合并天数")
    plt.ylabel("PRs数量")
    plt.legend()
    
    save_plot(output_path, title)
