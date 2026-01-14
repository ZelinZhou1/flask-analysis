# -*- coding: utf-8 -*-
"""
代码复杂度可视化模块
生成圈复杂度分布、高复杂度函数排行、维护性指数分布等图表
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List, Dict, Any
from pathlib import Path

from src.config import OUTPUT_DIR, WARM_COLORS, WARM_PALETTE
from src.visualizers.style import apply_style, save_plot


def plot_complexity_distribution(complexity_data: List[Dict[str, Any]]) -> None:
    """
    绘制圈复杂度(Cyclomatic Complexity)分布图

    Args:
        complexity_data: 包含复杂度信息的字典列表
    """
    apply_style()

    if not complexity_data:
        print("没有复杂度数据，跳过绘制。")
        return

    df = pd.DataFrame(complexity_data)

    # 确保有 complexity 字段
    if "complexity" not in df.columns:
        return

    plt.figure(figsize=(10, 6))

    # 使用直方图 + KDE
    sns.histplot(
        data=df,
        x="complexity",
        kde=True,
        color=WARM_COLORS["primary"],
        bins=30,
        edgecolor=WARM_COLORS["background"],
    )

    plt.xlabel("圈复杂度 (CC)", fontsize=12)
    plt.ylabel("函数/方法数量", fontsize=12)

    # 添加平均值线
    mean_cc = df["complexity"].mean()
    plt.axvline(
        mean_cc,
        color=WARM_COLORS["accent"],
        linestyle="--",
        label=f"平均值: {mean_cc:.2f}",
    )
    plt.legend()

    output_path = OUTPUT_DIR / "complexity_distribution.png"
    save_plot(str(output_path), "代码圈复杂度分布")


def plot_high_complexity_functions(
    complexity_data: List[Dict[str, Any]], top_n: int = 10
) -> None:
    """
    绘制高复杂度函数排行榜 (Top N)

    Args:
        complexity_data: 包含复杂度信息的字典列表
        top_n: 显示前N名
    """
    apply_style()

    if not complexity_data:
        return

    df = pd.DataFrame(complexity_data)

    if "complexity" not in df.columns or "name" not in df.columns:
        return

    # 按复杂度降序排序
    top_df = df.sort_values("complexity", ascending=False).head(top_n)

    plt.figure(figsize=(12, 8))

    # 绘制水平条形图
    sns.barplot(
        data=top_df, y="name", x="complexity", palette=WARM_PALETTE[:top_n], orient="h"
    )

    plt.xlabel("圈复杂度", fontsize=12)
    plt.ylabel("函数名称", fontsize=12)

    # 在条形图末尾添加数值标签
    for i, v in enumerate(top_df["complexity"]):
        plt.text(v + 0.5, i, str(v), color=WARM_COLORS["dark"], va="center")

    output_path = OUTPUT_DIR / "top_complexity_functions.png"
    save_plot(str(output_path), f"高复杂度函数 Top {top_n}")


def plot_maintainability_index(mi_data: List[float]) -> None:
    """
    绘制维护性指数(Maintainability Index)分布图

    Args:
        mi_data: MI 数值列表
    """
    apply_style()

    if not mi_data:
        return

    plt.figure(figsize=(10, 6))

    # 绘制箱线图和小提琴图结合
    sns.violinplot(x=mi_data, color=WARM_COLORS["tertiary"], inner="quartile")
    sns.stripplot(
        x=mi_data, color=WARM_COLORS["primary"], size=4, alpha=0.6, jitter=True
    )

    plt.xlabel("维护性指数 (MI)", fontsize=12)
    plt.title("代码维护性指数分布", pad=20)

    # 添加参考区间背景色 (MI < 65 难维护, 65-85 中等, > 85 易维护)
    # 注意：这里只是简单的可视化，不一定严格准确对应所有标准

    output_path = OUTPUT_DIR / "maintainability_index.png"
    save_plot(str(output_path), "代码维护性指数分布")
