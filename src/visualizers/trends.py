# -*- coding: utf-8 -*-
"""
趋势图模块
绘制提交趋势和累积图
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Optional
import logging

from src.visualizers.style import apply_style, save_plot, get_color, get_palette

logger = logging.getLogger(__name__)


def plot_cumulative_commits(
    commits_df: pd.DataFrame,
    output_path: str,
    title: str = "累积提交趋势"
) -> None:
    """
    绘制累积提交趋势图
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
    
    df = df.sort_values("date")
    df["cumulative"] = range(1, len(df) + 1)
    
    plt.figure(figsize=(14, 6))
    
    plt.fill_between(df["date"], df["cumulative"], color=get_color("primary"), alpha=0.5)
    plt.plot(df["date"], df["cumulative"], color=get_color("dark"), linewidth=1.5)
    
    plt.xlabel("时间")
    plt.ylabel("累积提交数")
    plt.grid(True, alpha=0.3)
    
    save_plot(output_path, title)


def plot_monthly_trend(
    commits_df: pd.DataFrame,
    output_path: str,
    title: str = "月度提交趋势"
) -> None:
    """
    绘制月度提交趋势
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
    
    df["month"] = df["date"].dt.to_period("M")
    monthly = df.groupby("month").size()
    
    plt.figure(figsize=(16, 6))
    
    x = range(len(monthly))
    plt.bar(x, monthly.values, color=get_color("primary"), alpha=0.7, width=0.8)
    
    window = 6
    if len(monthly) > window:
        ma = monthly.rolling(window=window).mean()
        plt.plot(x, ma.values, color=get_color("dark"), linewidth=2, label=f"{window}个月移动平均")
        plt.legend()
    
    step = max(1, len(monthly) // 15)
    ticks = range(0, len(monthly), step)
    labels = [str(monthly.index[i]) for i in ticks]
    plt.xticks(list(ticks), labels, rotation=45, ha="right")
    
    plt.xlabel("月份")
    plt.ylabel("提交数")
    plt.grid(True, alpha=0.3, axis="y")
    
    save_plot(output_path, title)


def plot_yearly_comparison(
    commits_df: pd.DataFrame,
    output_path: str,
    title: str = "年度对比分析"
) -> None:
    """
    绘制年度对比分析图
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
    df["month"] = df["date"].dt.month
    
    years = sorted(df["year"].unique())[-5:]
    
    plt.figure(figsize=(14, 8))
    
    colors = get_palette()
    months = range(1, 13)
    month_labels = ["1月", "2月", "3月", "4月", "5月", "6月", 
                    "7月", "8月", "9月", "10月", "11月", "12月"]
    
    for i, year in enumerate(years):
        year_df = df[df["year"] == year]
        monthly = year_df.groupby("month").size().reindex(months, fill_value=0)
        plt.plot(months, monthly.values, marker="o", label=str(year), 
                 color=colors[i % len(colors)], linewidth=2)
    
    plt.xticks(months, month_labels)
    plt.xlabel("月份")
    plt.ylabel("提交数")
    plt.legend(title="年份")
    plt.grid(True, alpha=0.3)
    
    save_plot(output_path, title)


def plot_line_chart(
    data: pd.Series,
    title: str,
    xlabel: str,
    ylabel: str,
    output_path: str,
    marker: str = "o",
) -> None:
    """
    绘制通用折线图
    """
    apply_style()
    
    plt.figure(figsize=(12, 6))
    
    plt.plot(data.index, data.values, marker=marker, color=get_color("primary"), linewidth=2)
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, alpha=0.3)
    
    save_plot(output_path, title)


def plot_area_chart(
    data: pd.Series,
    title: str,
    xlabel: str,
    ylabel: str,
    output_path: str,
) -> None:
    """
    绘制通用面积图
    """
    apply_style()
    
    plt.figure(figsize=(12, 6))
    
    x = range(len(data))
    plt.fill_between(x, data.values, color=get_color("primary"), alpha=0.6)
    plt.plot(x, data.values, color=get_color("dark"), linewidth=1.5)
    
    step = max(1, len(data) // 15)
    ticks = range(0, len(data), step)
    labels = [str(data.index[i]) for i in ticks]
    plt.xticks(list(ticks), labels, rotation=45, ha="right")
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    
    save_plot(output_path, title)
