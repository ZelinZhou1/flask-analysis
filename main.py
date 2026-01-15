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
    """Step 3: Generate visualizations."""
    logger.info("Step 3: Generating visualizations...")

    df = data.get("commit_df")
    repo_stats = data.get("repo_stats")
    complexity_stats = data.get("complexity_stats")

    if df is None or df.empty:
        logger.warning("No commit data to visualize.")
        return

    # 1. Annual Commits
    yearly_counts = df["year"].value_counts().sort_index()
    charts.plot_bar(
        yearly_counts,
        "Commits by Year",
        "Year",
        "Number of Commits",
        str(OUTPUT_DIR / "annual_commits.png"),
    )

    # 2. Monthly Commits Trend
    # Aggregate by month (sorting string periods correctly requires care,
    # but for simplicity we take top N or just sort by index)
    monthly_counts = df["month"].value_counts().sort_index()
    # Plotting all months might be too crowded, maybe last 24 months?
    # For now plot all
    charts.plot_bar(
        monthly_counts,
        "Monthly Commits Trend",
        "Month",
        "Number of Commits",
        str(OUTPUT_DIR / "monthly_commits.png"),
    )

    # 3. Top Authors
    author_counts = df["author_name"].value_counts().head(10)
    charts.plot_horizontal_bar(
        author_counts,
        "Top 10 Contributors",
        "Number of Commits",
        "Author",
        str(OUTPUT_DIR / "top_authors.png"),
    )

    # 4. File Type Distribution
    languages = repo_stats.get("languages", {})
    if languages:
        lang_series = pd.Series(languages).sort_values(ascending=False).head(10)
        charts.plot_pie(
            lang_series, "File Type Distribution", str(OUTPUT_DIR / "file_types.png")
        )

    # 5. Complexity Distribution (Top Complex Functions)
    high_complexity = complexity_stats.get("high_complexity_functions", [])
    if high_complexity:
        # Create a series for top 20 complex functions
        # Name format: class.method or just name
        comp_data = {}
        for func in high_complexity[:20]:
            name = f"{func['name']} ({func['complexity']})"
            comp_data[name] = func["complexity"]

        comp_series = pd.Series(comp_data).sort_values(ascending=False)
        charts.plot_horizontal_bar(
            comp_series,
            "Top 20 High Complexity Functions",
            "Cyclomatic Complexity",
            "Function",
            str(OUTPUT_DIR / "complexity_ranking.png"),
        )

    # 6. Commits by Hour
    hourly_counts = df["hour"].value_counts().sort_index()
    charts.plot_bar(
        hourly_counts,
        "Commits by Hour of Day",
        "Hour",
        "Commits",
        str(OUTPUT_DIR / "commits_by_hour.png"),
    )

    # 7. Commits by Weekday
    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    weekday_counts = df["weekday"].value_counts().reindex(weekday_order)
    charts.plot_bar(
        weekday_counts,
        "Commits by Weekday",
        "Weekday",
        "Commits",
        str(OUTPUT_DIR / "commits_by_weekday.png"),
    )

    # 8. Commit Message Length Analysis (Simple)
    df["msg_len"] = df["msg"].apply(len)
    # Binning message lengths
    msg_len_bins = (
        pd.cut(df["msg_len"], bins=[0, 20, 50, 100, 200, 500, 1000])
        .value_counts()
        .sort_index()
    )
    charts.plot_bar(
        msg_len_bins,
        "Commit Message Length Distribution",
        "Length Range",
        "Count",
        str(OUTPUT_DIR / "message_length_dist.png"),
    )

    logger.info(f"Visualizations saved to {OUTPUT_DIR}")


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
