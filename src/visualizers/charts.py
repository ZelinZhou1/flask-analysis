# -*- coding: utf-8 -*-
"""
Basic charts module
Provides functions for creating bar charts and pie charts.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from typing import List, Optional, Union, Dict, Any

from src.visualizers.style import apply_style, save_plot, get_color, get_palette


def plot_bar(
    data: pd.Series,
    title: str,
    xlabel: str,
    ylabel: str,
    output_path: str,
    top_n: Optional[int] = None,
    horizontal: bool = False,
) -> None:
    """
    Plot a bar chart.

    Args:
        data: The data to plot (index as labels, values as heights).
        title: Chart title.
        xlabel: Label for x-axis.
        ylabel: Label for y-axis.
        output_path: Path to save the chart.
        top_n: If provided, only plot the top N items.
        horizontal: If True, plot a horizontal bar chart.
    """
    apply_style()

    if top_n and len(data) > top_n:
        data = data.head(top_n)

    plt.figure()

    if horizontal:
        sns.barplot(x=data.values, y=data.index, palette=get_palette())
        plt.xlabel(ylabel)  # Swap labels for horizontal
        plt.ylabel(xlabel)
    else:
        sns.barplot(x=data.index, y=data.values, palette=get_palette())
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45, ha="right")

    save_plot(output_path, title)


def plot_horizontal_bar(
    data: pd.Series,
    title: str,
    xlabel: str,
    ylabel: str,
    output_path: str,
    top_n: Optional[int] = None,
) -> None:
    """
    Wrapper for plot_bar with horizontal=True.
    """
    plot_bar(data, title, xlabel, ylabel, output_path, top_n, horizontal=True)


def plot_pie(
    data: pd.Series, title: str, output_path: str, show_legend: bool = True
) -> None:
    """
    Plot a pie chart.

    Args:
        data: The data to plot.
        title: Chart title.
        output_path: Path to save the chart.
        show_legend: Whether to show legend.
    """
    apply_style()

    plt.figure()

    colors = get_palette()
    # Ensure we have enough colors
    if len(colors) < len(data):
        colors = colors * (len(data) // len(colors) + 1)
    colors = colors[: len(data)]

    patches, texts, autotexts = plt.pie(
        data.values,
        labels=data.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        pctdistance=0.85,
        labeldistance=1.1,
    )

    # Draw a circle at the center to make it a donut chart (optional, but looks nice)
    centre_circle = plt.Circle((0, 0), 0.70, fc="white")
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    if show_legend:
        plt.legend(patches, data.index, loc="best")

    save_plot(output_path, title)
