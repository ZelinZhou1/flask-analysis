# -*- coding: utf-8 -*-
"""
提交热力图模块
生成提交时间热力图
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from typing import Dict, List
import logging

from src.visualizers.style import apply_style, save_plot, get_cmap

logger = logging.getLogger(__name__)


def plot_commit_heatmap(
    commits_df: pd.DataFrame,
    output_path: str,
    title: str = "提交时间热力图"
) -> None:
    """
    绘制提交时间热力图（小时 x 星期）
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
            logger.warning("缺少日期字段")
            return
    else:
        df["date"] = pd.to_datetime(df["date"], utc=True)
    
    df["hour"] = df["date"].dt.hour
    df["weekday"] = df["date"].dt.day_name()
    
    pivot = df.groupby(["weekday", "hour"]).size().unstack(fill_value=0)
    
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_chinese = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    
    existing_days = [d for d in weekday_order if d in pivot.index]
    pivot = pivot.reindex(existing_days)
    
    new_index = []
    for day in pivot.index:
        idx = weekday_order.index(day)
        new_index.append(weekday_chinese[idx])
    pivot.index = new_index
    
    plt.figure(figsize=(16, 8))
    
    sns.heatmap(
        pivot,
        cmap="YlOrRd",
        linewidths=0.5,
        annot=False,
        cbar_kws={"label": "提交数量"},
    )
    
    plt.xlabel("小时")
    plt.ylabel("星期")
    
    save_plot(output_path, title)


def plot_yearly_heatmap(
    commits_df: pd.DataFrame,
    output_path: str,
    title: str = "年度提交热力图"
) -> None:
    """
    绘制年度提交热力图（月 x 年）
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
    
    pivot = df.groupby(["year", "month"]).size().unstack(fill_value=0)
    
    month_labels = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
    pivot.columns = month_labels
    
    plt.figure(figsize=(14, 10))
    
    sns.heatmap(
        pivot,
        cmap="YlOrRd",
        linewidths=0.5,
        annot=True,
        fmt="d",
        cbar_kws={"label": "提交数量"},
    )
    
    plt.xlabel("月份")
    plt.ylabel("年份")
    
    save_plot(output_path, title)


def plot_author_activity_heatmap(
    commits_df: pd.DataFrame,
    output_path: str,
    title: str = "贡献者活动热力图",
    top_n: int = 15
) -> None:
    """
    绘制贡献者提交活动热力图（作者 x 年）
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
    df_top = df[df["author_name"].isin(top_authors)]
    
    pivot = df_top.groupby(["author_name", "year"]).size().unstack(fill_value=0)
    
    pivot = pivot.reindex(top_authors)
    
    plt.figure(figsize=(14, 10))
    
    sns.heatmap(
        pivot,
        cmap="YlOrRd",
        linewidths=0.5,
        annot=True,
        fmt="d",
        cbar_kws={"label": "提交数量"},
    )
    
    plt.xlabel("年份")
    plt.ylabel("贡献者")
    
    save_plot(output_path, title)
