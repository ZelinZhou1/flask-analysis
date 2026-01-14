# -*- coding: utf-8 -*-
"""
File charts module
Provides functions for visualizing file statistics.
"""

import pandas as pd
from typing import Dict, Any, Optional

from src.visualizers.charts import plot_bar, plot_pie, plot_horizontal_bar
from src.visualizers.style import apply_style, save_plot


def plot_file_stats(
    file_types: pd.Series, file_complexity: pd.Series, output_dir: str
) -> None:
    """
    Generate standard file statistics charts.

    Args:
        file_types: Series with file extensions as index and counts as values.
        file_complexity: Series with file paths as index and complexity scores as values.
        output_dir: Directory to save the charts.
    """
    import os

    # File type distribution (Pie)
    plot_pie(
        file_types,
        "File Type Distribution",
        os.path.join(output_dir, "file_types_pie.png"),
    )

    # File type distribution (Bar) - Better for many types
    plot_bar(
        file_types,
        "File Counts by Type",
        "File Type",
        "Count",
        os.path.join(output_dir, "file_types_bar.png"),
    )

    # Top complex files (Horizontal Bar)
    # Ensure sorted
    file_complexity_sorted = file_complexity.sort_values(ascending=False)

    # Truncate long file paths for display if necessary
    # (The plot_horizontal_bar handles standard plotting, but truncation might be needed for labels)
    # Let's assume the complexity series has valid paths.

    plot_horizontal_bar(
        file_complexity_sorted,
        "Top Most Complex Files",
        "Cyclomatic Complexity",
        "File Path",
        os.path.join(output_dir, "complex_files_bar.png"),
        top_n=10,
    )


def plot_file_size_dist(file_sizes: pd.Series, title: str, output_path: str) -> None:
    """
    Plot file size distribution (Histogram/Boxplot).

    Args:
        file_sizes: Series of file sizes.
        title: Chart title.
        output_path: Path to save the chart.
    """
    apply_style()
    import matplotlib.pyplot as plt
    import seaborn as sns
    from src.visualizers.style import get_palette

    plt.figure()

    # Using a histogram with KDE
    sns.histplot(data=file_sizes, kde=True, color=get_palette()[0])

    plt.xlabel("File Size (LOC)")
    plt.ylabel("Frequency")
    plt.title(title)

    save_plot(output_path, title)
