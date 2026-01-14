# -*- coding: utf-8 -*-
"""
Style module
Provides functions to apply the warm color scheme and chart styles.
"""

import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any, Optional

from src.config import (
    WARM_COLORS,
    WARM_PALETTE,
    WARM_CMAP,
    CHART_STYLE,
    FIGURE_SIZE,
    FIGURE_DPI,
)
from src.utils.font_config import configure_chinese_font


def apply_style() -> None:
    """
    Apply the project's visual style to matplotlib and seaborn.
    Sets the color palette, font, and other plot configurations.
    """
    # Configure Chinese font support
    configure_chinese_font()

    # Apply matplotlib style settings
    for key, value in CHART_STYLE.items():
        plt.rcParams[key] = value

    # Set default figure size and DPI
    plt.rcParams["figure.figsize"] = FIGURE_SIZE
    plt.rcParams["figure.dpi"] = FIGURE_DPI

    # Apply seaborn style
    sns.set_theme(style="whitegrid", palette=WARM_PALETTE)

    # Re-apply custom rcParams because seaborn might overwrite some
    plt.rcParams.update(CHART_STYLE)


def get_color(name: str) -> str:
    """
    Get a specific color from the warm color scheme.

    Args:
        name: The name of the color ('primary', 'secondary', 'tertiary', 'background', 'accent', 'dark').

    Returns:
        The hex color code.
    """
    return WARM_COLORS.get(name, WARM_COLORS["primary"])


def get_palette() -> List[str]:
    """
    Get the warm color palette list.

    Returns:
        List of hex color codes.
    """
    return WARM_PALETTE


def get_cmap() -> Any:
    """
    Get the warm colormap for heatmaps.

    Returns:
        The LinearSegmentedColormap object.
    """
    return WARM_CMAP


def save_plot(filename: str, title: Optional[str] = None) -> None:
    """
    Helper to save the current plot with consistent settings.

    Args:
        filename: Path to save the file.
        title: Optional title for the plot.
    """
    if title:
        plt.title(
            title, pad=20, fontsize=16, fontweight="bold", color=WARM_COLORS["dark"]
        )

    plt.tight_layout()
    # Ensure the directory exists
    import os

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    plt.savefig(
        filename,
        dpi=FIGURE_DPI,
        bbox_inches="tight",
        facecolor=WARM_COLORS["background"],
    )
    plt.close()
