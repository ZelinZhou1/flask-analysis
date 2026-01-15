# -*- coding: utf-8 -*-
"""
综合可视化生成脚本
生成所有图表
"""

import sys
import json
import logging
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.visualizers.style import apply_style
from src.visualizers import charts
from src.visualizers.heatmap import plot_heatmap, plot_activity_heatmap
from src.visualizers.commit_heatmap import plot_commit_heatmap, plot_yearly_heatmap, plot_author_activity_heatmap
from src.visualizers.wordcloud_chart import generate_wordcloud
from src.visualizers.trends import plot_cumulative_commits, plot_monthly_trend, plot_yearly_comparison
from src.visualizers.charts_3d import plot_commits_3d, plot_author_3d
from src.visualizers.issues_charts import plot_issues_state, plot_issues_timeline, plot_issues_labels, plot_top_issue_authors
from src.visualizers.pr_charts import plot_prs_state, plot_prs_timeline, plot_top_pr_authors, plot_pr_merge_time
from src.visualizers.contributors_charts import plot_contributors_ranking, plot_contributions_pie, plot_contributors_timeline, plot_first_contribution_timeline
from src.analyzers.message_analyzer import analyze_messages

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")


def load_json(filename: str):
    """加载JSON数据"""
    path = DATA_DIR / filename
    if not path.exists():
        logger.warning(f"文件不存在: {path}")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_all_charts():
    """生成所有图表"""
    apply_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    logger.info("加载数据...")
    commits = load_json("commits.json")
    issues = load_json("issues.json")
    prs = load_json("pull_requests.json")
    contributors = load_json("contributors.json")
    
    if commits:
        logger.info(f"Commits: {len(commits)}")
        df = pd.DataFrame(commits)
        df["date"] = pd.to_datetime(df["committer_date"], utc=True)
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.to_period("M").astype(str)
        df["hour"] = df["date"].dt.hour
        df["weekday"] = df["date"].dt.day_name()
        
        logger.info("生成Commits图表...")
        
        yearly = df["year"].value_counts().sort_index()
        charts.plot_bar(yearly, "年度提交统计", "年份", "提交数", str(OUTPUT_DIR / "commits_by_year.png"))
        
        weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekday_labels = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        weekday = df["weekday"].value_counts().reindex(weekday_order)
        weekday.index = weekday_labels
        charts.plot_bar(weekday, "星期提交分布", "星期", "提交数", str(OUTPUT_DIR / "commits_by_weekday.png"))
        
        hourly = df["hour"].value_counts().sort_index()
        charts.plot_bar(hourly, "小时提交分布", "小时", "提交数", str(OUTPUT_DIR / "commits_by_hour.png"))
        
        top_authors = df["author_name"].value_counts().head(20)
        charts.plot_horizontal_bar(top_authors, "Top 20贡献者", "提交数", "作者", str(OUTPUT_DIR / "top_authors.png"))
        
        top_10 = df["author_name"].value_counts().head(10)
        other = len(df) - top_10.sum()
        if other > 0:
            top_10["其他"] = other
        charts.plot_pie(top_10, "贡献占比", str(OUTPUT_DIR / "authors_pie.png"))
        
        plot_commit_heatmap(df, str(OUTPUT_DIR / "commit_heatmap.png"))
        plot_yearly_heatmap(df, str(OUTPUT_DIR / "yearly_heatmap.png"))
        plot_author_activity_heatmap(df, str(OUTPUT_DIR / "author_heatmap.png"))
        
        plot_cumulative_commits(df, str(OUTPUT_DIR / "cumulative.png"))
        plot_monthly_trend(df, str(OUTPUT_DIR / "monthly_trend.png"))
        plot_yearly_comparison(df, str(OUTPUT_DIR / "yearly_comparison.png"))
        
        plot_commits_3d(df, str(OUTPUT_DIR / "commits_3d.png"))
        plot_author_3d(df, str(OUTPUT_DIR / "author_3d.png"))
        
        plot_contributors_timeline(df, str(OUTPUT_DIR / "contributors_timeline.png"))
        plot_first_contribution_timeline(df, str(OUTPUT_DIR / "new_contributors.png"))
        
        messages = df["msg"].tolist()
        generate_wordcloud(messages, str(OUTPUT_DIR / "wordcloud.png"))
        
        msg_analysis = analyze_messages(messages)
        type_dist = pd.Series(msg_analysis.get("type_distribution", {}))
        type_labels = {"feat": "新功能", "fix": "修复", "docs": "文档", "refactor": "重构", "test": "测试", "chore": "杂项", "style": "样式", "perf": "性能", "other": "其他"}
        type_dist.index = [type_labels.get(t, t) for t in type_dist.index]
        if not type_dist.empty:
            charts.plot_pie(type_dist, "提交类型分布", str(OUTPUT_DIR / "commit_types.png"))
    
    if issues:
        logger.info(f"Issues: {len(issues)}")
        plot_issues_state(issues, str(OUTPUT_DIR / "issues_state.png"))
        plot_issues_timeline(issues, str(OUTPUT_DIR / "issues_timeline.png"))
        plot_issues_labels(issues, str(OUTPUT_DIR / "issues_labels.png"))
        plot_top_issue_authors(issues, str(OUTPUT_DIR / "top_issue_authors.png"))
    
    if prs:
        logger.info(f"PRs: {len(prs)}")
        plot_prs_state(prs, str(OUTPUT_DIR / "pr_state.png"))
        plot_prs_timeline(prs, str(OUTPUT_DIR / "pr_timeline.png"))
        plot_top_pr_authors(prs, str(OUTPUT_DIR / "top_pr_authors.png"))
        plot_pr_merge_time(prs, str(OUTPUT_DIR / "pr_merge_time.png"))
    
    if contributors:
        logger.info(f"Contributors: {len(contributors)}")
        plot_contributors_ranking(contributors, str(OUTPUT_DIR / "top_contributors.png"))
        plot_contributions_pie(contributors, str(OUTPUT_DIR / "contributions_pie.png"))
    
    logger.info(f"图表生成完成，保存到: {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_all_charts()
