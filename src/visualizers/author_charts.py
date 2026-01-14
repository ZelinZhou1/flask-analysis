# -*- coding: utf-8 -*-
"""
Author charts module
Provides functions for visualizing author statistics.
"""

import pandas as pd
from typing import Dict, Any, Optional

from src.visualizers.charts import plot_bar, plot_pie, plot_horizontal_bar
from src.visualizers.style import apply_style, save_plot


def plot_author_stats(
    author_commits: pd.Series, author_loc: pd.Series, output_dir: str
) -> None:
    """
    Generate standard author statistics charts.

    Args:
        author_commits: Series with author names as index and commit counts as values.
        author_loc: Series with author names as index and LOC counts as values.
        output_dir: Directory to save the charts.
    """
    import os

    # Commit distribution (Pie)
    plot_pie(
        author_commits,
        "Author Commit Distribution",
        os.path.join(output_dir, "author_commits_pie.png"),
    )

    # Top authors by commits (Bar)
    plot_horizontal_bar(
        author_commits,
        "Top Authors by Commits",
        "Commits",
        "Author",
        os.path.join(output_dir, "author_commits_bar.png"),
        top_n=10,
    )

    # Top authors by LOC (Bar)
    # Ensure author_loc is sorted
    author_loc_sorted = author_loc.sort_values(ascending=False)
    plot_horizontal_bar(
        author_loc_sorted,
        "Top Authors by Lines of Code",
        "LOC",
        "Author",
        os.path.join(output_dir, "author_loc_bar.png"),
        top_n=10,
    )


def plot_author_activity_bubble(
    data: pd.DataFrame, title: str, output_path: str
) -> None:
    """
    Plot a bubble chart of author activity (e.g., Commits vs LOC).

    Args:
        data: DataFrame with 'commits', 'additions', 'deletions' columns, indexed by author.
        title: Chart title.
        output_path: Path to save the chart.
    """
    apply_style()
    import matplotlib.pyplot as plt
    import seaborn as sns
    from src.visualizers.style import get_palette

    plt.figure()

    # Create bubble chart using scatterplot
    # Size based on additions+deletions (churn) or just one of them
    if "churn" not in data.columns:
        data["churn"] = data.get("additions", 0) + data.get("deletions", 0)

    sns.scatterplot(
        data=data,
        x="commits",
        y="churn",
        size="churn",
        sizes=(100, 1000),
        alpha=0.6,
        palette=get_palette(),
        legend=False,
    )

    # Annotate points
    for i, author in enumerate(data.index):
        plt.annotate(
            author,
            (data.iloc[i]["commits"], data.iloc[i]["churn"]),
            xytext=(5, 5),
            textcoords="offset points",
        )

    plt.xlabel("Commits")
    plt.ylabel("Code Churn (Lines Changed)")
    plt.title(title)

    save_plot(output_path, title)
