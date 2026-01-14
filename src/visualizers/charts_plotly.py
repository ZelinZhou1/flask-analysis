# -*- coding: utf-8 -*-
"""
交互式图表可视化模块 (Plotly)
生成3D分布图、交互式热力图等
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Dict, Any
from pathlib import Path

from src.config import OUTPUT_DIR, WARM_COLORS, WARM_PALETTE


def plot_interactive_commit_activity(commit_data: List[Dict[str, Any]]) -> None:
    """
    绘制交互式3D提交时间分布图 (小时 x 星期 x 提交量)

    Args:
        commit_data: 提交数据列表
    """
    if not commit_data:
        print("没有提交数据，跳过交互式图表绘制。")
        return

    df = pd.DataFrame(commit_data)
    if "date" not in df.columns:
        return

    df["date"] = pd.to_datetime(df["date"])
    df["weekday"] = df["date"].dt.day_name()
    df["hour"] = df["date"].dt.hour

    # 聚合数据
    activity = df.groupby(["weekday", "hour"]).size().reset_index(name="count")

    # 星期排序
    weekdays_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    # 3D 散点图
    fig = px.scatter_3d(
        activity,
        x="hour",
        y="weekday",
        z="count",
        color="count",
        size="count",
        color_continuous_scale=[
            [0, WARM_COLORS["background"]],
            [0.5, WARM_COLORS["secondary"]],
            [1, WARM_COLORS["primary"]],
        ],
        category_orders={"weekday": weekdays_order},
        title="3D Commit Activity Distribution",
    )

    fig.update_layout(
        scene=dict(
            xaxis_title="Hour of Day",
            yaxis_title="Weekday",
            zaxis_title="Number of Commits",
            bgcolor=WARM_COLORS["background"],
        ),
        paper_bgcolor=WARM_COLORS["background"],
        font=dict(color=WARM_COLORS["dark"]),
    )

    output_path = OUTPUT_DIR / "interactive_3d_activity.html"
    _save_plotly(fig, output_path)


def plot_interactive_author_timeline(commit_data: List[Dict[str, Any]]) -> None:
    """
    绘制交互式作者活跃时间线
    """
    if not commit_data:
        return

    df = pd.DataFrame(commit_data)
    df["date"] = pd.to_datetime(df["date"])

    # 按天和作者聚合
    df["date_day"] = df["date"].dt.date
    daily_counts = (
        df.groupby(["date_day", "author_name"]).size().reset_index(name="commits")
    )

    fig = px.scatter(
        daily_counts,
        x="date_day",
        y="author_name",
        size="commits",
        color="author_name",
        color_discrete_sequence=WARM_PALETTE,
        title="Author Activity Timeline",
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor=WARM_COLORS["background"],
        font=dict(color=WARM_COLORS["dark"]),
        xaxis_title="Date",
        yaxis_title="Author",
    )

    output_path = OUTPUT_DIR / "interactive_author_timeline.html"
    _save_plotly(fig, output_path)


def plot_interactive_file_changes(
    file_stats: List[Dict[str, Any]], top_n: int = 20
) -> None:
    """
    绘制交互式文件修改热力图 (Treemap)
    """
    if not file_stats:
        return

    df = pd.DataFrame(file_stats)
    if "commits" not in df.columns or "name" not in df.columns:
        return

    # 只取 Top N
    df = df.sort_values("commits", ascending=False).head(top_n)

    # 简单的路径处理来创建层级
    df["parent"] = "Root"

    fig = px.treemap(
        df,
        path=["parent", "name"],
        values="commits",
        color="commits",
        color_continuous_scale=[
            [0, WARM_COLORS["tertiary"]],
            [1, WARM_COLORS["primary"]],
        ],
        title=f"Top {top_n} Most Active Files",
    )

    fig.update_layout(
        paper_bgcolor=WARM_COLORS["background"], font=dict(color=WARM_COLORS["dark"])
    )

    output_path = OUTPUT_DIR / "interactive_file_treemap.html"
    _save_plotly(fig, output_path)


def _save_plotly(fig: go.Figure, path: Path) -> None:
    """
    辅助函数：保存Plotly图表，确保目录存在
    """
    import os

    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.write_html(str(path))
