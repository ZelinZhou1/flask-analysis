# -*- coding: utf-8 -*-
"""
PR (Pull Request) 可视化模块
生成PR大小分布、合并时间等图表
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List, Dict, Any

from src.config import OUTPUT_DIR, WARM_COLORS, WARM_PALETTE
from src.visualizers.style import apply_style, save_plot


def plot_pr_size_distribution(pr_data: List[Dict[str, Any]]) -> None:
    """
    绘制PR大小分布图 (代码变更行数)

    Args:
        pr_data: PR数据列表
    """
    apply_style()

    if not pr_data:
        print("没有PR数据，跳过绘制。")
        return

    df = pd.DataFrame(pr_data)

    # 计算总变更行数
    if "additions" in df.columns and "deletions" in df.columns:
        df["total_changes"] = df["additions"] + df["deletions"]
    elif "changed_files" in df.columns:  # fallback if lines not available
        df["total_changes"] = df["changed_files"]
    else:
        return

    plt.figure(figsize=(10, 6))

    # 使用对数刻度，因为PR大小通常符合幂律分布
    sns.histplot(
        data=df,
        x="total_changes",
        kde=True,
        log_scale=True,
        color=WARM_COLORS["primary"],
        edgecolor=WARM_COLORS["background"],
    )

    plt.xlabel("代码变更行数 (Log Scale)", fontsize=12)
    plt.ylabel("PR 数量", fontsize=12)
    plt.title("Pull Request 大小分布", pad=20)

    output_path = OUTPUT_DIR / "pr_size_distribution.png"
    save_plot(str(output_path), "PR 大小分布")


def plot_pr_time_to_merge(pr_data: List[Dict[str, Any]]) -> None:
    """
    绘制PR合并耗时分布

    Args:
        pr_data: PR数据列表
    """
    apply_style()

    if not pr_data:
        return

    df = pd.DataFrame(pr_data)

    # 确保有时间字段
    if "created_at" not in df.columns or "merged_at" not in df.columns:
        return

    # 过滤未合并的PR
    merged_prs = df.dropna(subset=["merged_at"]).copy()

    if merged_prs.empty:
        return

    merged_prs["created_at"] = pd.to_datetime(merged_prs["created_at"])
    merged_prs["merged_at"] = pd.to_datetime(merged_prs["merged_at"])

    # 计算小时数
    merged_prs["hours_to_merge"] = (
        merged_prs["merged_at"] - merged_prs["created_at"]
    ).dt.total_seconds() / 3600

    plt.figure(figsize=(10, 6))

    sns.boxplot(x=merged_prs["hours_to_merge"], color=WARM_COLORS["tertiary"])

    plt.xlabel("合并耗时 (小时)", fontsize=12)
    plt.title("PR 合并耗时分布", pad=20)

    # 如果数据跨度大，使用对数刻度
    if merged_prs["hours_to_merge"].max() > 100:
        plt.xscale("log")
        plt.xlabel("合并耗时 (小时) - Log Scale", fontsize=12)

    output_path = OUTPUT_DIR / "pr_merge_time.png"
    save_plot(str(output_path), "PR 合并耗时")


def plot_pr_comments_vs_size(pr_data: List[Dict[str, Any]]) -> None:
    """
    绘制PR评论数与大小的关系 (散点图)
    """
    apply_style()

    if not pr_data:
        return

    df = pd.DataFrame(pr_data)

    if "comments" not in df.columns:
        return

    # 计算大小
    if "additions" in df.columns:
        df["size"] = df["additions"] + df["deletions"]
    else:
        return

    plt.figure(figsize=(10, 8))

    sns.scatterplot(
        data=df,
        x="size",
        y="comments",
        color=WARM_COLORS["secondary"],
        alpha=0.6,
        s=100,
    )

    plt.xscale("log")
    plt.xlabel("PR 大小 (代码行数)", fontsize=12)
    plt.ylabel("评论数量", fontsize=12)

    output_path = OUTPUT_DIR / "pr_comments_vs_size.png"
    save_plot(str(output_path), "PR 评论数 vs 大小")
