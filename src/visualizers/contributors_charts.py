# -*- coding: utf-8 -*-
"""
贡献者分析可视化模块
"""

import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict
from collections import Counter
import logging

from src.visualizers.style import apply_style, save_plot, get_palette, get_color

logger = logging.getLogger(__name__)


def plot_contributors_ranking(
    contributors: List[Dict],
    output_path: str,
    title: str = "贡献者提交排行",
    top_n: int = 20
) -> None:
    """
    绘制贡献者提交排行
    """
    apply_style()
    
    if not contributors:
        logger.warning("没有贡献者数据")
        return
    
    data = {}
    for c in contributors[:top_n]:
        login = c.get("login", "unknown")
        contributions = c.get("contributions", 0)
        data[login] = contributions
    
    plt.figure(figsize=(12, 10))
    
    colors = get_palette()
    names = list(data.keys())
    values = list(data.values())
    
    bars = plt.barh(names, values, color=colors[:len(names)])
    
    plt.xlabel("贡献数")
    plt.ylabel("贡献者")
    plt.gca().invert_yaxis()
    
    for bar, val in zip(bars, values):
        plt.text(bar.get_width() + max(values)*0.01, bar.get_y() + bar.get_height()/2, 
                 str(val), va="center", fontsize=9)
    
    save_plot(output_path, title)


def plot_contributions_pie(
    contributors: List[Dict],
    output_path: str,
    title: str = "贡献占比分布",
    top_n: int = 10
) -> None:
    """
    绘制贡献占比饼图
    """
    apply_style()
    
    if not contributors:
        logger.warning("没有贡献者数据")
        return
    
    data = {}
    total = 0
    for c in contributors:
        contributions = c.get("contributions", 0)
        total += contributions
    
    for c in contributors[:top_n]:
        login = c.get("login", "unknown")
        contributions = c.get("contributions", 0)
        data[login] = contributions
    
    top_total = sum(data.values())
    if total > top_total:
        data["其他"] = total - top_total
    
    plt.figure(figsize=(10, 10))
    
    colors = get_palette()
    plt.pie(data.values(), labels=data.keys(), autopct="%1.1f%%", 
            colors=colors[:len(data)], startangle=90)
    
    save_plot(output_path, title)


def plot_contributors_timeline(
    commits_df: pd.DataFrame,
    output_path: str,
    title: str = "贡献者活跃时间线",
    top_n: int = 10
) -> None:
    """
    绘制贡献者活跃时间线
    """
    apply_style()
    
    if commits_df.empty:
        logger.warning("没有提交数据")
        return
    
    df = commits_df.copy()
    
    if "date" not in df.columns:
        if "committer_date" in df.columns:
            df["date"] = pd.to_datetime(df["committer_date"], utc=True)
        else:
            return
    else:
        df["date"] = pd.to_datetime(df["date"], utc=True)
    
    df["year"] = df["date"].dt.year
    
    top_authors = df["author_name"].value_counts().head(top_n).index.tolist()
    
    plt.figure(figsize=(14, 8))
    
    colors = get_palette()
    for i, author in enumerate(top_authors):
        author_df = df[df["author_name"] == author]
        yearly = author_df.groupby("year").size()
        plt.plot(yearly.index, yearly.values, marker="o", 
                 label=author[:15], color=colors[i % len(colors)], linewidth=2)
    
    plt.xlabel("年份")
    plt.ylabel("提交数")
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.grid(True, alpha=0.3)
    
    save_plot(output_path, title)


def plot_first_contribution_timeline(
    commits_df: pd.DataFrame,
    output_path: str,
    title: str = "新贡献者加入趋势"
) -> None:
    """
    绘制每年新加入贡献者数量
    """
    apply_style()
    
    if commits_df.empty:
        logger.warning("没有提交数据")
        return
    
    df = commits_df.copy()
    
    if "date" not in df.columns:
        if "committer_date" in df.columns:
            df["date"] = pd.to_datetime(df["committer_date"], utc=True)
        else:
            return
    else:
        df["date"] = pd.to_datetime(df["date"], utc=True)
    
    df["year"] = df["date"].dt.year
    
    first_year = df.groupby("author_name")["year"].min()
    new_contributors = first_year.value_counts().sort_index()
    
    plt.figure(figsize=(12, 6))
    
    plt.bar(new_contributors.index.astype(str), new_contributors.values, color=get_color("primary"))
    
    plt.xlabel("年份")
    plt.ylabel("新贡献者数")
    plt.xticks(rotation=45, ha="right")
    
    save_plot(output_path, title)
