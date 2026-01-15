# -*- coding: utf-8 -*-
"""
Heatmap module
Provides functions for creating heatmaps, including calendar heatmaps.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from typing import Optional, Tuple

from src.visualizers.style import apply_style, save_plot, get_cmap


def plot_heatmap(
    data: pd.DataFrame,
    title: str,
    xlabel: str,
    ylabel: str,
    output_path: str,
    fmt: str = "d",
    annot: bool = True,
) -> None:
    """
    Plot a general heatmap.

    Args:
        data: DataFrame containing the matrix data.
        title: Chart title.
        xlabel: Label for x-axis.
        ylabel: Label for y-axis.
        output_path: Path to save the chart.
        fmt: String formatting code for annotations.
        annot: Whether to annotate the cells.
    """
    apply_style()

    plt.figure()

    sns.heatmap(
        data,
        annot=annot,
        fmt=fmt,
        cmap=get_cmap(),
        linewidths=0.5,
        cbar_kws={"label": "Count"},
    )

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    save_plot(output_path, title)


def plot_calendar_heatmap(
    dates: pd.Series, values: pd.Series, title: str, output_path: str
) -> None:
    """
    绘制日历热力图（按日期分布）
    
    Args:
        dates: 日期序列
        values: 对应的数值序列
        title: 图表标题
        output_path: 保存路径
    """
    apply_style()
    
    # 创建日期-数值的DataFrame
    df = pd.DataFrame({"date": pd.to_datetime(dates), "value": values})
    df["weekday"] = df["date"].dt.day_name()
    df["hour"] = df["date"].dt.hour
    
    # 按星期和小时分组统计
    pivot = df.groupby(["weekday", "hour"])["value"].sum().unstack(fill_value=0)
    
    # 按正确的星期顺序排列
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = pivot.reindex([w for w in weekday_order if w in pivot.index])
    
    plt.figure(figsize=(14, 6))
    
    sns.heatmap(
        pivot,
        cmap=get_cmap(),
        linewidths=0.5,
        annot=True,
        fmt="g",
        cbar_kws={"label": "活动数量"},
    )
    
    plt.xlabel("小时")
    plt.ylabel("星期")
    
    save_plot(output_path, title)


def plot_activity_heatmap(data: pd.DataFrame, title: str, output_path: str) -> None:
    """
    绘制活动热力图（小时 x 星期）
    
    Args:
        data: DataFrame，索引为星期，列为小时(0-23)
        title: 图表标题
        output_path: 保存路径
    """
    apply_style()
    
    plt.figure(figsize=(14, 6))
    
    # 确保星期顺序正确
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if all(w in data.index for w in weekday_order):
        data = data.reindex(weekday_order)
    
    sns.heatmap(
        data,
        cmap=get_cmap(),
        linewidths=0.5,
        annot=True,
        fmt="g",
        cbar_kws={"label": "提交数量"},
    )
    
    plt.xlabel("小时")
    plt.ylabel("星期")
    
    save_plot(output_path, title)


def plot_contribution_heatmap(
    commits_df: pd.DataFrame, 
    title: str = "贡献者活动热力图",
    output_path: str = None
) -> None:
    """
    绘制贡献者活动热力图（作者 x 月份）
    
    Args:
        commits_df: 包含author_name和date列的DataFrame
        title: 图表标题
        output_path: 保存路径
    """
    apply_style()
    
    df = commits_df.copy()
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
    
    # 按作者和月份统计
    pivot = df.groupby(["author_name", "month"]).size().unstack(fill_value=0)
    
    # 只显示top 15贡献者
    top_authors = df["author_name"].value_counts().head(15).index
    pivot = pivot.loc[pivot.index.isin(top_authors)]
    
    # 只显示最近24个月
    recent_months = sorted(pivot.columns)[-24:]
    pivot = pivot[recent_months]
    
    plt.figure(figsize=(16, 10))
    
    sns.heatmap(
        pivot,
        cmap=get_cmap(),
        linewidths=0.3,
        cbar_kws={"label": "提交数量"},
    )
    
    plt.xlabel("月份")
    plt.ylabel("贡献者")
    plt.xticks(rotation=45, ha="right")
    
    save_plot(output_path, title)

