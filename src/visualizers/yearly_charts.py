# -*- coding: utf-8 -*-
"""
年度统计图表模块
按年度分析提交数据
"""
import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict
import logging

from src.visualizers.style import apply_style, save_plot, get_palette, get_color

logger = logging.getLogger(__name__)


def plot_yearly_commits(
    commits_df: pd.DataFrame,
    output_path: str,
    title: str = "年度提交统计",
) -> None:
    """
    绘制年度提交柱状图
    
    Args:
        commits_df: 包含提交数据的DataFrame
        output_path: 输出路径
        title: 图表标题
    """
    apply_style()
    
    if commits_df.empty:
        logger.warning("没有提交数据")
        return
    
    # 确保有date列
    if "date" not in commits_df.columns and "committer_date" in commits_df.columns:
        commits_df["date"] = pd.to_datetime(commits_df["committer_date"])
    else:
        commits_df["date"] = pd.to_datetime(commits_df["date"])
    
    # 按年统计
    commits_df["year"] = commits_df["date"].dt.year
    yearly = commits_df["year"].value_counts().sort_index()
    
    plt.figure(figsize=(12, 6))
    
    colors = get_palette()
    bars = plt.bar(yearly.index.astype(str), yearly.values, color=colors[:len(yearly)])
    
    plt.xlabel("年份")
    plt.ylabel("提交数量")
    plt.xticks(rotation=45, ha="right")
    
    # 添加数值标签
    for bar, count in zip(bars, yearly.values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + yearly.max() * 0.01,
            str(count),
            ha="center",
            va="bottom",
            fontsize=9,
        )
    
    save_plot(output_path, title)


def plot_yearly_authors(
    commits_df: pd.DataFrame,
    output_path: str,
    title: str = "年度活跃贡献者数量",
) -> None:
    """
    绘制年度活跃贡献者数量
    
    Args:
        commits_df: 包含提交数据的DataFrame
        output_path: 输出路径
        title: 图表标题
    """
    apply_style()
    
    if commits_df.empty:
        logger.warning("没有提交数据")
        return
    
    # 确保有date列
    if "date" not in commits_df.columns:
        commits_df["date"] = pd.to_datetime(commits_df.get("committer_date", commits_df.iloc[:, 0]))
    
    commits_df["year"] = pd.to_datetime(commits_df["date"]).dt.year
    
    # 统计每年唯一作者数
    yearly_authors = commits_df.groupby("year")["author_name"].nunique()
    
    plt.figure(figsize=(12, 6))
    
    plt.plot(yearly_authors.index.astype(str), yearly_authors.values, 
             marker="o", color=get_color("primary"), linewidth=2, markersize=8)
    
    plt.xlabel("年份")
    plt.ylabel("活跃贡献者数")
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, alpha=0.3)
    
    # 填充面积
    plt.fill_between(yearly_authors.index.astype(str), yearly_authors.values, 
                     alpha=0.3, color=get_color("primary"))
    
    save_plot(output_path, title)


def plot_yearly_comparison(
    commits_df: pd.DataFrame,
    output_path: str,
    title: str = "年度提交对比（增删行数）",
) -> None:
    """
    绘制年度代码增删对比
    
    Args:
        commits_df: 包含insertions和deletions的DataFrame
        output_path: 输出路径
        title: 图表标题
    """
    apply_style()
    
    if commits_df.empty:
        logger.warning("没有提交数据")
        return
    
    if "insertions" not in commits_df.columns or "deletions" not in commits_df.columns:
        logger.warning("缺少insertions/deletions列")
        return
    
    commits_df["date"] = pd.to_datetime(commits_df.get("committer_date", commits_df.get("date")))
    commits_df["year"] = commits_df["date"].dt.year
    
    # 按年汇总
    yearly_stats = commits_df.groupby("year").agg({
        "insertions": "sum",
        "deletions": "sum"
    })
    
    plt.figure(figsize=(12, 6))
    
    x = range(len(yearly_stats))
    width = 0.35
    
    bars1 = plt.bar([i - width/2 for i in x], yearly_stats["insertions"], 
                    width, label="增加行数", color=get_color("primary"))
    bars2 = plt.bar([i + width/2 for i in x], yearly_stats["deletions"], 
                    width, label="删除行数", color=get_color("secondary"))
    
    plt.xlabel("年份")
    plt.ylabel("行数")
    plt.xticks(x, yearly_stats.index.astype(str), rotation=45, ha="right")
    plt.legend()
    
    save_plot(output_path, title)
