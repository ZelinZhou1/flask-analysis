# -*- coding: utf-8 -*-
"""
样式模块
提供暖色系配色和图表样式配置
"""

import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from typing import Dict, List, Any, Optional
from pathlib import Path

from src.config import (
    WARM_COLORS,
    WARM_PALETTE,
    WARM_CMAP,
    CHART_STYLE,
    FIGURE_SIZE,
    FIGURE_DPI,
)

_style_configured = False


def apply_style() -> None:
    """
    应用项目的视觉样式到matplotlib和seaborn
    """
    global _style_configured
    
    if _style_configured:
        return
    
    warnings.filterwarnings('ignore', category=UserWarning)
    
    font_path = Path("C:/Windows/Fonts/msyh.ttc")
    if font_path.exists():
        import matplotlib.font_manager as fm
        try:
            fm.fontManager.addfont(str(font_path))
        except:
            pass
    
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.unicode_minus'] = False
    
    for key, value in CHART_STYLE.items():
        try:
            plt.rcParams[key] = value
        except:
            pass

    plt.rcParams["figure.figsize"] = FIGURE_SIZE
    plt.rcParams["figure.dpi"] = FIGURE_DPI

    sns.set_theme(style="whitegrid", palette=WARM_PALETTE)

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    _style_configured = True


def get_color(name: str) -> str:
    """获取指定颜色"""
    return WARM_COLORS.get(name, WARM_COLORS["primary"])


def get_palette() -> List[str]:
    """获取暖色系调色板"""
    return WARM_PALETTE


def get_cmap() -> Any:
    """获取暖色系colormap"""
    return WARM_CMAP


def save_plot(filename: str, title: Optional[str] = None) -> None:
    """
    保存图表
    """
    import os
    
    if title:
        plt.title(
            title, pad=20, fontsize=14, fontweight="bold", color=WARM_COLORS["dark"]
        )

    plt.tight_layout()
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    plt.savefig(
        filename,
        dpi=FIGURE_DPI,
        bbox_inches="tight",
        facecolor=WARM_COLORS["background"],
    )
    plt.close()
