# -*- coding: utf-8 -*-
"""
年度统计可视化模块
生成年度提交柱状图等
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Dict, List, Any

from src.config import OUTPUT_DIR, WARM_COLORS, WARM_PALETTE
from src.visualizers.style import apply_style, save_plot


def plot_yearly_commits(yearly_data: Dict[int, int]) -> None:
    """
    绘制年度提交数量柱状图

    Args:
        yearly_data: 年份到提交数的映射字典 {2020: 50, 2021: 120}
    """
    apply_style()

    if not yearly_data:
        print("没有年度数据，跳过绘制。")
        return

    # 转换为DataFrame
    df = pd.DataFrame(list(yearly_data.items()), columns=["Year", "Commits"])
    df = df.sort_values("Year")

    plt.figure(figsize=(10, 6))

    # 绘制柱状图
    barplot = sns.barplot(
        data=df,
        x="Year",
        y="Commits",
        palette=WARM_PALETTE,
        edgecolor=WARM_COLORS["dark"],
    )

    plt.xlabel("年份", fontsize=12)
    plt.ylabel("提交数量", fontsize=12)

    # 在柱子上方添加数值
    for p in barplot.patches:
        barplot.annotate(
            f"{int(p.get_height())}",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            xytext=(0, 10),
            textcoords="offset points",
            color=WARM_COLORS["dark"],
            fontweight="bold",
        )

    output_path = OUTPUT_DIR / "yearly_commits.png"
    save_plot(str(output_path), "年度提交统计")


def plot_monthly_activity(monthly_data: pd.DataFrame) -> None:
    """
    绘制月度活跃趋势

    Args:
        monthly_data: 包含 'Date' 和 'Commits' 列的 DataFrame
    """
    apply_style()

    if monthly_data.empty:
        return

    plt.figure(figsize=(14, 6))

    sns.lineplot(
        data=monthly_data,
        x="Date",
        y="Commits",
        color=WARM_COLORS["primary"],
        linewidth=2.5,
        marker="o",
    )

    plt.xlabel("日期", fontsize=12)
    plt.ylabel("提交数量", fontsize=12)
    plt.fill_between(
        monthly_data["Date"],
        monthly_data["Commits"],
        color=WARM_COLORS["secondary"],
        alpha=0.3,
    )

    output_path = OUTPUT_DIR / "monthly_trend.png"
    save_plot(str(output_path), "月度提交趋势")
