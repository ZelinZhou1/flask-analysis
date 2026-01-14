# -*- coding: utf-8 -*-
"""
依赖关系可视化模块
生成文件/模块依赖网络图
"""

import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Tuple, Dict
from pathlib import Path

from src.config import OUTPUT_DIR, WARM_COLORS, WARM_PALETTE
from src.visualizers.style import apply_style, save_plot


def plot_dependency_network(
    dependencies: List[Tuple[str, str]], max_nodes: int = 50
) -> None:
    """
    绘制依赖关系网络图

    Args:
        dependencies: 依赖对列表 [(source, target), ...]
        max_nodes: 最大节点数，防止图过于杂乱
    """
    apply_style()

    if not dependencies:
        print("没有依赖数据，跳过绘制。")
        return

    # 创建有向图
    G = nx.DiGraph()
    G.add_edges_from(dependencies)

    # 如果节点太多，只保留度数最高的节点
    if G.number_of_nodes() > max_nodes:
        degrees = dict(G.degree())
        top_nodes = sorted(degrees, key=degrees.get, reverse=True)[:max_nodes]
        G = G.subgraph(top_nodes)

    plt.figure(figsize=(12, 12))

    # 布局算法
    pos = nx.spring_layout(G, k=0.5, iterations=50)

    # 绘制节点
    # 根据度数设置节点大小
    d = dict(G.degree)
    node_sizes = [v * 100 + 300 for v in d.values()]

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=node_sizes,
        node_color=WARM_COLORS["primary"],
        alpha=0.8,
        edgecolors=WARM_COLORS["dark"],
    )

    # 绘制边
    nx.draw_networkx_edges(
        G, pos, width=1.0, alpha=0.5, edge_color=WARM_COLORS["accent"], arrowsize=20
    )

    # 绘制标签
    nx.draw_networkx_labels(
        G,
        pos,
        font_size=8,
        font_color=WARM_COLORS["dark"],
        font_family="Microsoft YaHei",  # 尝试使用中文字体
    )

    plt.axis("off")
    output_path = OUTPUT_DIR / "dependency_network.png"
    save_plot(str(output_path), "文件依赖关系网络图")


def plot_module_coupling(coupling_data: Dict[str, int], top_n: int = 15) -> None:
    """
    绘制模块耦合度排行

    Args:
        coupling_data: 模块到耦合度(Fan-out/Fan-in)的映射
        top_n: 显示前N名
    """
    apply_style()

    if not coupling_data:
        return

    import pandas as pd
    import seaborn as sns

    df = pd.DataFrame(list(coupling_data.items()), columns=["Module", "Coupling"])
    df = df.sort_values("Coupling", ascending=False).head(top_n)

    plt.figure(figsize=(10, 8))

    sns.barplot(
        data=df, y="Module", x="Coupling", palette=WARM_PALETTE[:top_n], orient="h"
    )

    plt.xlabel("耦合度 (引用次数)", fontsize=12)
    plt.ylabel("模块", fontsize=12)

    output_path = OUTPUT_DIR / "module_coupling.png"
    save_plot(str(output_path), f"模块耦合度 Top {top_n}")
