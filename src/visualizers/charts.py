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

    colors = get_palette()
    if horizontal:
        plt.barh(data.index, data.values, color=colors[:len(data)])
        plt.xlabel(ylabel)
        plt.ylabel(xlabel)
    else:
        plt.bar(data.index, data.values, color=colors[:len(data)])
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


def plot_line(
    data: pd.Series,
    title: str,
    xlabel: str,
    ylabel: str,
    output_path: str,
    marker: str = "o",
    color: str = None,
) -> None:
    """
    绘制折线图
    
    Args:
        data: 要绘制的数据
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签
        output_path: 保存路径
        marker: 标记样式
        color: 线条颜色
    """
    apply_style()
    
    plt.figure(figsize=(12, 6))
    
    line_color = color or get_color("primary")
    plt.plot(data.index, data.values, marker=marker, color=line_color, linewidth=2)
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, alpha=0.3)
    
    save_plot(output_path, title)


def plot_area(
    data: pd.Series,
    title: str,
    xlabel: str,
    ylabel: str,
    output_path: str,
    alpha: float = 0.7,
) -> None:
    """
    绘制面积图
    
    Args:
        data: 要绘制的数据
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签
        output_path: 保存路径
        alpha: 透明度
    """
    apply_style()
    
    plt.figure(figsize=(12, 6))
    
    plt.fill_between(
        range(len(data)), 
        data.values, 
        color=get_color("primary"), 
        alpha=alpha
    )
    plt.plot(data.values, color=get_color("dark"), linewidth=1.5)
    
    # 设置x轴标签
    if len(data) <= 20:
        plt.xticks(range(len(data)), data.index, rotation=45, ha="right")
    else:
        # 太多标签时只显示部分
        step = len(data) // 10
        indices = range(0, len(data), step)
        plt.xticks(indices, [data.index[i] for i in indices], rotation=45, ha="right")
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    
    save_plot(output_path, title)


def plot_stacked_bar(
    data: pd.DataFrame,
    title: str,
    xlabel: str,
    ylabel: str,
    output_path: str,
) -> None:
    """
    绘制堆叠柱状图
    
    Args:
        data: DataFrame，每列一个堆叠类别
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签
        output_path: 保存路径
    """
    apply_style()
    
    plt.figure(figsize=(14, 8))
    
    colors = get_palette()
    data.plot(kind="bar", stacked=True, color=colors[:len(data.columns)])
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="类别", bbox_to_anchor=(1.02, 1), loc="upper left")
    
    save_plot(output_path, title)

