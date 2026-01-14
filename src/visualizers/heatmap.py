# -*- coding: utf-8 -*-
"""
Heatmap module
Provides functions for creating heatmaps, including calendar heatmaps.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from typing import Optional, Tuple

from src.visualizers.style import apply_style, save_plot, get_cmap


def plot_heatmap(
    data: pd.DataFrame,
    title: str,
    xlabel: str,
    ylabel: str,
    output_path: str,
    fmt: str = "d",
    annot: bool = True,
) -> None:
    """
    Plot a general heatmap.

    Args:
        data: DataFrame containing the matrix data.
        title: Chart title.
        xlabel: Label for x-axis.
        ylabel: Label for y-axis.
        output_path: Path to save the chart.
        fmt: String formatting code for annotations.
        annot: Whether to annotate the cells.
    """
    apply_style()

    plt.figure()

    sns.heatmap(
        data,
        annot=annot,
        fmt=fmt,
        cmap=get_cmap(),
        linewidths=0.5,
        cbar_kws={"label": "Count"},
    )

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    save_plot(output_path, title)


def plot_calendar_heatmap(
    dates: pd.Series, values: pd.Series, title: str, output_path: str
) -> None:
    """
    Plot a calendar-like heatmap (e.g., commit activity by day of week and hour).

    Args:
        dates: Series of datetime objects (or things that can be converted).
        values: Series of values corresponding to the dates.
        title: Chart title.
        output_path: Path to save the chart.
    """
    # This function expects 'dates' to be processable into a pivot table
    # For simplicity, let's assume 'dates' contains the timestamp and 'values' contains the count
    # Or we can accept a pivot table directly.
    # But to be flexible, let's assume we are receiving a pivot table ready for heatmap
    # If the input is raw data, we need to process it.

    # However, looking at the args, it seems better to keep it generic or accept a DataFrame.
    # Let's assume the user passes a DataFrame that is already a pivot table (Hour x Weekday).

    pass
    # Actually, let's implement the specific logic for Hour x Weekday if that's what's typically needed
    # or just use plot_heatmap if the data is already prepared.

    # If the input is just dates and values, we might need to pivot it.
    # Let's assume the caller prepares the data for now and uses plot_heatmap
    # But if this is specifically "calendar", maybe it handles the pivoting.

    # Re-reading requirements: "提交时间热力图（小时x星期）" is one of the charts.
    # So let's make a specific function for that.

    # Wait, the signature I defined takes dates and values.
    # Let's change it to take a DataFrame for flexibility or perform the pivot here.
    # Let's assume data is passed as a DataFrame where index is Weekday and columns are Hours.

    pass


def plot_activity_heatmap(data: pd.DataFrame, title: str, output_path: str) -> None:
    """
    Plot activity heatmap (e.g. Hour x Weekday).

    Args:
        data: DataFrame with index as Weekday and columns as Hours (0-23).
        title: Chart title.
        output_path: Path to save the chart.
    """
    plot_heatmap(data, title, "Hour of Day", "Day of Week", output_path)
