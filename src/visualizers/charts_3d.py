# -*- coding: utf-8 -*-
"""
3D可视化模块
生成3D图表
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Optional
import logging

from src.visualizers.style import apply_style, save_plot, get_palette, get_color

logger = logging.getLogger(__name__)


def plot_commits_3d(
    commits_df: pd.DataFrame,
    output_path: str,
    title: str = "提交3D分布图"
) -> None:
    """
    绘制提交的3D散点图（年 x 月 x 提交数）
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
    
    grouped = df.groupby(["year", "month"]).size().reset_index(name="count")
    
    try:
        from mpl_toolkits.mplot3d import Axes3D
        
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection="3d")
        
        colors = plt.cm.YlOrRd(grouped["count"] / grouped["count"].max())
        
        ax.scatter(
            grouped["year"],
            grouped["month"],
            grouped["count"],
            c=colors,
            s=grouped["count"] * 2,
            alpha=0.8,
        )
        
        ax.set_xlabel("年份")
        ax.set_ylabel("月份")
        ax.set_zlabel("提交数")
        
        save_plot(output_path, title)
        
    except Exception as e:
        logger.warning(f"3D图表生成失败: {e}")


def plot_author_3d(
    commits_df: pd.DataFrame,
    output_path: str,
    title: str = "贡献者3D活动图",
    top_n: int = 10
) -> None:
    """
    绘制贡献者3D活动图（作者 x 年 x 提交数）
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
    
    grouped = df_top.groupby(["author_name", "year"]).size().reset_index(name="count")
    
    author_map = {name: i for i, name in enumerate(top_authors)}
    grouped["author_idx"] = grouped["author_name"].map(author_map)
    
    try:
        from mpl_toolkits.mplot3d import Axes3D
        
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection="3d")
        
        colors_palette = get_palette()
        
        for i, author in enumerate(top_authors):
            author_data = grouped[grouped["author_name"] == author]
            ax.bar3d(
                author_data["year"] - 0.4,
                [i] * len(author_data),
                [0] * len(author_data),
                0.8,
                0.8,
                author_data["count"],
                color=colors_palette[i % len(colors_palette)],
                alpha=0.8,
            )
        
        ax.set_xlabel("年份")
        ax.set_ylabel("贡献者")
        ax.set_zlabel("提交数")
        ax.set_yticks(range(len(top_authors)))
        ax.set_yticklabels([a[:10] for a in top_authors], fontsize=8)
        
        save_plot(output_path, title)
        
    except Exception as e:
        logger.warning(f"3D图表生成失败: {e}")
