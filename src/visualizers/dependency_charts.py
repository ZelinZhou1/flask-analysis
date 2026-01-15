# -*- coding: utf-8 -*-
"""
依赖关系图可视化模块
使用NetworkX生成依赖关系网络图
"""
import matplotlib.pyplot as plt
from typing import Dict, List, Optional
import logging

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    nx = None

from src.visualizers.style import apply_style, save_plot, get_color, get_palette

logger = logging.getLogger(__name__)


def plot_dependency_graph(
    dependencies: Dict[str, List[str]],
    output_path: str,
    title: str = "模块依赖关系图",
    max_nodes: int = 50,
) -> None:
    """
    绘制依赖关系网络图
    
    Args:
        dependencies: 依赖关系字典 {module: [dependencies]}
        output_path: 输出路径
        title: 图表标题
        max_nodes: 最大节点数
    """
    if not NETWORKX_AVAILABLE:
        logger.warning("NetworkX未安装，无法生成依赖图")
        return
    
    apply_style()
    
    # 创建有向图
    G = nx.DiGraph()
    
    # 添加边
    edge_count = 0
    for source, targets in dependencies.items():
        source_short = source.split("/")[-1].replace(".py", "")
        
        for target in targets:
            target_short = target.split(".")[-1]
            G.add_edge(source_short, target_short)
            edge_count += 1
            
            if G.number_of_nodes() >= max_nodes:
                break
        
        if G.number_of_nodes() >= max_nodes:
            break
    
    if G.number_of_nodes() == 0:
        logger.warning("没有依赖关系可绘制")
        return
    
    # 绘制
    plt.figure(figsize=(16, 12))
    
    # 使用spring布局
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    # 计算节点大小（基于入度）
    in_degrees = dict(G.in_degree())
    node_sizes = [300 + in_degrees.get(node, 0) * 100 for node in G.nodes()]
    
    # 暖色系节点颜色
    node_colors = get_palette()[:len(G.nodes())] if len(G.nodes()) <= len(get_palette()) else [get_color("primary")] * len(G.nodes())
    
    # 绘制边
    nx.draw_networkx_edges(
        G, pos,
        edge_color="#888888",
        alpha=0.5,
        arrows=True,
        arrowsize=15,
        connectionstyle="arc3,rad=0.1"
    )
    
    # 绘制节点
    nx.draw_networkx_nodes(
        G, pos,
        node_size=node_sizes,
        node_color=node_colors,
        alpha=0.9,
    )
    
    # 绘制标签
    nx.draw_networkx_labels(
        G, pos,
        font_size=8,
        font_color="black",
    )
    
    plt.axis("off")
    
    # 添加统计信息
    stats_text = f"节点: {G.number_of_nodes()} | 边: {G.number_of_edges()}"
    plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes,
             fontsize=10, verticalalignment="top")
    
    save_plot(output_path, title)


def plot_import_frequency(
    import_counts: List[tuple],
    output_path: str,
    title: str = "模块导入频率",
    top_n: int = 20,
) -> None:
    """
    绘制模块导入频率柱状图
    
    Args:
        import_counts: 导入频率列表 [(module, count), ...]
        output_path: 输出路径
        title: 图表标题
        top_n: 显示前N个
    """
    apply_style()
    
    # 取前N个
    data = import_counts[:top_n]
    
    if not data:
        logger.warning("没有导入数据")
        return
    
    modules = [item[0] for item in data]
    counts = [item[1] for item in data]
    
    plt.figure(figsize=(12, 8))
    
    colors = get_palette()
    bars = plt.barh(range(len(modules)), counts, color=colors[:len(modules)])
    
    plt.yticks(range(len(modules)), modules)
    plt.xlabel("导入次数")
    plt.ylabel("模块名")
    plt.gca().invert_yaxis()  # 最多的在上面
    
    # 添加数值标签
    for i, (bar, count) in enumerate(zip(bars, counts)):
        plt.text(bar.get_width() + 0.3, i, str(count), va="center")
    
    save_plot(output_path, title)
