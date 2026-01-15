# -*- coding: utf-8 -*-
"""
Flask Repository Analyzer - Main Entry Point
Orchestrates the data collection, analysis, and visualization pipeline.
"""

import sys
import os
import logging
import json
import pandas as pd
from pathlib import Path
from collections import Counter
from datetime import datetime

# Ensure src is in python path
sys.path.append(str(Path(__file__).parent / "src"))

from src.config import FLASK_REPO_PATH, DATA_DIR, OUTPUT_DIR, WARM_COLORS, CACHE_ENABLED
from src.collectors.pydriller_collector import PyDrillerCollector
from src.analyzers.stats import CodeStats
from src.analyzers.complexity_analyzer import ComplexityAnalyzer
from src.visualizers import charts, style

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("analyzer.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

def ensure_directories():
    """确保数据和输出目录存在"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_cached_commits():
    """尝试从缓存加载提交数据"""
    cache_file = DATA_DIR / "commits.json"
    if cache_file.exists():
        logger.info(f"发现缓存文件: {cache_file}")
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                commits = json.load(f)
            logger.info(f"从缓存加载了 {len(commits)} 条提交记录")
            return commits
        except Exception as e:
            logger.warning(f"缓存加载失败: {e}")
    return None


def collect_data(use_cache: bool = True):
    """
    Step 1: 从仓库采集数据
    
    Args:
        use_cache: 是否使用缓存，默认True
    """
    logger.info("Step 1: 采集数据...")
    
    # 尝试使用缓存
    if use_cache:
        cached = load_cached_commits()
        if cached:
            return cached

    if not FLASK_REPO_PATH.exists():
        logger.error(f"仓库不存在: {FLASK_REPO_PATH}")
        return None

    collector = PyDrillerCollector(str(FLASK_REPO_PATH))
    commits = list(collector.collect_commits())

    logger.info(f"采集到 {len(commits)} 条提交记录")

    # 保存到缓存
    raw_data_path = DATA_DIR / "commits.json"
    with open(raw_data_path, "w", encoding="utf-8") as f:
        json.dump(commits, f, default=str, indent=2, ensure_ascii=False)
    logger.info(f"数据已保存到: {raw_data_path}")

    return commits


def analyze_stats(commits):
    """Step 2: Analyze statistics."""
    logger.info("Step 2: Analyzing statistics...")

    # Repo file stats
    stats_analyzer = CodeStats()
    repo_stats = stats_analyzer.analyze_directory(str(FLASK_REPO_PATH))

    # Complexity analysis
    complexity_analyzer = ComplexityAnalyzer(str(FLASK_REPO_PATH))
    complexity_stats = complexity_analyzer.analyze_repository()

    # Process commit data for visualization
    df = pd.DataFrame(commits)
    if not df.empty:
        # 修复时区感知日期转换问题
        df["date"] = pd.to_datetime(df["committer_date"], utc=True)
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.to_period("M").astype(str)
        df["hour"] = df["date"].dt.hour
        df["weekday"] = df["date"].dt.day_name()

    return {
        "repo_stats": repo_stats,
        "complexity_stats": complexity_stats,
        "commit_df": df,
    }


def generate_visualizations(data):
    """Step 3: 生成可视化图表"""
    logger.info("Step 3: 生成可视化图表...")

    df = data.get("commit_df")
    repo_stats = data.get("repo_stats")
    complexity_stats = data.get("complexity_stats")

    if df is None or df.empty:
        logger.warning("没有提交数据可供可视化")
        return

    # 1. 年度提交统计
    yearly_counts = df["year"].value_counts().sort_index()
    charts.plot_bar(
        yearly_counts,
        "年度提交统计",
        "年份",
        "提交数量",
        str(OUTPUT_DIR / "annual_commits.png"),
    )

    # 2. 月度提交趋势（只显示最近36个月，避免拥挤）
    monthly_counts = df["month"].value_counts().sort_index()
    recent_months = monthly_counts.tail(36)  # 最近3年
    # 简化标签，只显示年份
    recent_months.index = [m[-5:] if len(m) > 5 else m for m in recent_months.index]
    charts.plot_line(
        recent_months,
        "月度提交趋势（近3年）",
        "月份",
        "提交数量",
        str(OUTPUT_DIR / "monthly_commits.png"),
    )

    # 3. Top 15贡献者
    author_counts = df["author_name"].value_counts().head(15)
    charts.plot_horizontal_bar(
        author_counts,
        "Top 15 贡献者",
        "提交数量",
        "作者",
        str(OUTPUT_DIR / "top_authors.png"),
    )

    # 4. 文件类型分布
    languages = repo_stats.get("languages", {})
    if languages:
        lang_series = pd.Series(languages).sort_values(ascending=False).head(10)
        charts.plot_pie(
            lang_series, "文件类型分布", str(OUTPUT_DIR / "file_types.png")
        )

    # 5. 高复杂度函数排行
    high_complexity = complexity_stats.get("high_complexity_functions", [])
    if high_complexity:
        comp_data = {}
        for func in high_complexity[:20]:
            name = func['name'][:25]  # 截断长名称
            comp_data[name] = func["complexity"]
        comp_series = pd.Series(comp_data).sort_values(ascending=False)
        charts.plot_horizontal_bar(
            comp_series,
            "高复杂度函数排行 (Top 20)",
            "圈复杂度",
            "函数名",
            str(OUTPUT_DIR / "complexity_ranking.png"),
        )

    # 6. 提交时间分布（按小时）
    hourly_counts = df["hour"].value_counts().sort_index()
    charts.plot_bar(
        hourly_counts,
        "提交时间分布（按小时）",
        "小时",
        "提交数量",
        str(OUTPUT_DIR / "commits_by_hour.png"),
    )

    # 7. 提交星期分布
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_labels = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday_counts = df["weekday"].value_counts().reindex(weekday_order)
    weekday_counts.index = weekday_labels
    charts.plot_bar(
        weekday_counts,
        "提交星期分布",
        "星期",
        "提交数量",
        str(OUTPUT_DIR / "commits_by_weekday.png"),
    )

    # 8. 提交消息长度分布
    df["msg_len"] = df["msg"].apply(len)
    msg_len_bins = (
        pd.cut(df["msg_len"], bins=[0, 20, 50, 100, 200, 500, 1000])
        .value_counts()
        .sort_index()
    )
    charts.plot_bar(
        msg_len_bins,
        "提交消息长度分布",
        "长度区间",
        "提交数量",
        str(OUTPUT_DIR / "message_length_dist.png"),
    )

    # 9. 作者贡献饼图（Top 10占比）
    top_authors = df["author_name"].value_counts().head(10)
    other_count = len(df) - top_authors.sum()
    if other_count > 0:
        top_authors["其他"] = other_count
    charts.plot_pie(
        top_authors,
        "贡献者占比分布",
        str(OUTPUT_DIR / "author_pie.png"),
    )

    # 10. 年度代码变更量
    if "insertions" in df.columns and "deletions" in df.columns:
        yearly_changes = df.groupby("year").agg({
            "insertions": "sum",
            "deletions": "sum"
        })
        yearly_changes["net"] = yearly_changes["insertions"] - yearly_changes["deletions"]
        charts.plot_bar(
            yearly_changes["insertions"],
            "年度代码新增行数",
            "年份",
            "新增行数",
            str(OUTPUT_DIR / "yearly_insertions.png"),
        )

    # 11. 每年活跃贡献者数
    yearly_authors = df.groupby("year")["author_name"].nunique()
    charts.plot_line(
        yearly_authors,
        "每年活跃贡献者数量",
        "年份",
        "贡献者数",
        str(OUTPUT_DIR / "yearly_authors.png"),
    )

    # 12. 提交消息类型分析（简单）
    from src.analyzers.message_analyzer import analyze_messages
    msg_analysis = analyze_messages(df["msg"].tolist())
    type_counts = pd.Series(msg_analysis.get("type_distribution", {}))
    if not type_counts.empty:
        type_labels = {
            "feat": "新功能", "fix": "修复", "docs": "文档",
            "refactor": "重构", "test": "测试", "chore": "杂项",
            "style": "样式", "perf": "性能", "other": "其他"
        }
        type_counts.index = [type_labels.get(t, t) for t in type_counts.index]
        charts.plot_pie(
            type_counts,
            "提交类型分布",
            str(OUTPUT_DIR / "commit_types.png"),
        )

    # 13. 修改文件数分布
    if "files" in df.columns:
        file_counts = df["files"].value_counts().sort_index().head(20)
        charts.plot_bar(
            file_counts,
            "每次提交修改文件数分布",
            "文件数",
            "提交次数",
            str(OUTPUT_DIR / "files_per_commit.png"),
        )

    logger.info(f"可视化图表已保存到: {OUTPUT_DIR}")



def main():
    """Main execution flow."""
    logger.info("Starting Flask Repo Analyzer...")
    ensure_directories()

    commits = collect_data()
    if not commits:
        logger.error("Data collection failed or no commits found. Exiting.")
        return

    analysis_results = analyze_stats(commits)

    # Save analysis summary
    summary = {
        "repo_stats": analysis_results["repo_stats"],
        "complexity_stats": {
            k: v
            for k, v in analysis_results["complexity_stats"].items()
            if k != "high_complexity_functions"
        },
        "total_commits": len(commits),
    }
    with open(DATA_DIR / "analysis_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    generate_visualizations(analysis_results)

    logger.info("Analysis complete!")


if __name__ == "__main__":
    main()
