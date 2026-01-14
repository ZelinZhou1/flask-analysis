# -*- coding: utf-8 -*-
"""
Trends module
Provides functions for creating trend charts (line and area).
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from typing import Optional, List

from src.visualizers.style import apply_style, save_plot, get_palette


def plot_line_chart(
    data: pd.Series,
    title: str,
    xlabel: str,
    ylabel: str,
    output_path: str,
    hue: Optional[pd.Series] = None,
) -> None:
    """
    Plot a line chart (e.g., for time series).

    Args:
        data: The data to plot (index as x-axis, values as y-axis).
        title: Chart title.
        xlabel: Label for x-axis.
        ylabel: Label for y-axis.
        output_path: Path to save the chart.
        hue: Optional grouping variable.
    """
    apply_style()

    plt.figure()

    # Check if data is Series or DataFrame for sns.lineplot
    # If Series, index is x, values are y.
    sns.lineplot(data=data, palette=get_palette(), linewidth=2.5)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45, ha="right")

    save_plot(output_path, title)


def plot_area_chart(
    data: pd.DataFrame, title: str, xlabel: str, ylabel: str, output_path: str
) -> None:
    """
    Plot a stacked area chart.

    Args:
        data: DataFrame where index is x-axis (time) and columns are categories.
        title: Chart title.
        xlabel: Label for x-axis.
        ylabel: Label for y-axis.
        output_path: Path to save the chart.
    """
    apply_style()

    plt.figure()

    data.plot.area(stacked=True, color=get_palette())

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45, ha="right")

    # We need to get the current figure because pandas plot might create its own or use the current one
    # But generally pandas uses the current axis if ax is not provided.
    # save_plot closes the figure.

    save_plot(output_path, title)
