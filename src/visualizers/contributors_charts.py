# -*- coding: utf-8 -*-
"""
贡献者统计可视化模块
生成贡献者排行榜、活跃度分布等图表
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List, Dict, Any

from src.config import OUTPUT_DIR, WARM_COLORS, WARM_PALETTE
from src.visualizers.style import apply_style, save_plot


def plot_contributors_leaderboard(
    contributors_data: List[Dict[str, Any]], top_n: int = 10
) -> None:
    """
    绘制贡献者排行榜 (按提交数)

    Args:
        contributors_data: 贡献者数据列表
        top_n: 显示前N名
    """
    apply_style()

    if not contributors_data:
        print("没有贡献者数据，跳过绘制。")
        return

    df = pd.DataFrame(contributors_data)
    if "name" not in df.columns or "commits" not in df.columns:
        return

    # 按提交数排序
    df = df.sort_values("commits", ascending=False).head(top_n)

    plt.figure(figsize=(12, 8))

    sns.barplot(
        data=df, y="name", x="commits", palette=WARM_PALETTE[: len(df)], orient="h"
    )

    plt.xlabel("提交数量", fontsize=12)
    plt.ylabel("贡献者", fontsize=12)

    # 添加数值标签
    for i, v in enumerate(df["commits"]):
        plt.text(
            v + 0.5,
            i,
            str(v),
            color=WARM_COLORS["dark"],
            va="center",
            fontweight="bold",
        )

    output_path = OUTPUT_DIR / "contributors_leaderboard.png"
    save_plot(str(output_path), f"贡献者排行榜 Top {top_n}")


def plot_code_changes_by_author(
    contributors_data: List[Dict[str, Any]], top_n: int = 10
) -> None:
    """
    绘制每位作者的代码增删情况 (堆叠柱状图)

    Args:
        contributors_data: 贡献者数据列表
    """
    apply_style()

    if not contributors_data:
        return

    df = pd.DataFrame(contributors_data)
    if "additions" not in df.columns or "deletions" not in df.columns:
        return

    # 按总修改量排序
    df["total"] = df["additions"] + df["deletions"]
    df = df.sort_values("total", ascending=False).head(top_n)

    plt.figure(figsize=(12, 8))

    # 绘制增加行数
    plt.barh(
        df["name"],
        df["additions"],
        label="增加代码 (Additions)",
        color=WARM_COLORS["primary"],
    )

    # 绘制删除行数（使用负值让其向左，或者并在右边？通常堆叠或并列。这里使用堆叠）
    plt.barh(
        df["name"],
        df["deletions"],
        left=df["additions"],
        label="删除代码 (Deletions)",
        color=WARM_COLORS["tertiary"],
    )

    plt.xlabel("代码行数变更", fontsize=12)
    plt.ylabel("贡献者", fontsize=12)
    plt.legend()

    output_path = OUTPUT_DIR / "author_changes.png"
    save_plot(str(output_path), f"代码增删统计 Top {top_n}")


def plot_author_contribution_pie(contributors_data: List[Dict[str, Any]]) -> None:
    """
    绘制作者贡献占比饼图
    """
    apply_style()

    if not contributors_data:
        return

    df = pd.DataFrame(contributors_data)
    total_commits = df["commits"].sum()

    # 将小贡献者合并为 "Others"
    threshold = total_commits * 0.02  # 小于2%的

    main_contributors = df[df["commits"] >= threshold].copy()
    others_count = df[df["commits"] < threshold]["commits"].sum()

    if others_count > 0:
        new_row = pd.DataFrame([{"name": "Others", "commits": others_count}])
        main_contributors = pd.concat([main_contributors, new_row], ignore_index=True)

    # 排序
    main_contributors = main_contributors.sort_values("commits", ascending=False)

    plt.figure(figsize=(10, 10))

    plt.pie(
        main_contributors["commits"],
        labels=main_contributors["name"],
        autopct="%1.1f%%",
        startangle=140,
        pctdistance=0.85,
        colors=WARM_PALETTE[: len(main_contributors)],
        explode=[0.05] * len(main_contributors),
    )

    # 中心圆
    centre_circle = plt.Circle((0, 0), 0.70, fc=WARM_COLORS["background"])
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    output_path = OUTPUT_DIR / "author_distribution.png"
    save_plot(str(output_path), "贡献者分布")
