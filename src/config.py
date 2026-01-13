# -*- coding: utf-8 -*-
"""
全局配置模块
包含路径配置、暖色系配色方案、图表参数等
"""

from pathlib import Path
from matplotlib.colors import LinearSegmentedColormap

# =============================================================================
# 路径配置
# =============================================================================

# Flask仓库路径
FLASK_REPO_PATH = Path("C:/Users/l/Desktop/opensource/flask")

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 输出目录（存放生成的图表）
OUTPUT_DIR = PROJECT_ROOT / "output"

# 数据目录（存放中间数据文件）
DATA_DIR = PROJECT_ROOT / "data"

# =============================================================================
# 暖色系配色方案
# =============================================================================

# 主要颜色定义
WARM_COLORS = {
    "primary": "#E85A4F",  # 珊瑚红 - 主色调
    "secondary": "#E98074",  # 浅珊瑚 - 次要色
    "tertiary": "#D8C3A5",  # 米色 - 第三色
    "background": "#EAE7DC",  # 奶白色 - 背景色
    "accent": "#8E8D8A",  # 灰色 - 强调色
    "dark": "#4A4A48",  # 深灰 - 文字/边框
}

# 暖色调色板（用于多系列图表）
WARM_PALETTE = [
    "#E85A4F",  # 珊瑚红
    "#E98074",  # 浅珊瑚
    "#F4A460",  # 沙棕色
    "#DEB887",  # 原木色
    "#D2691E",  # 巧克力色
    "#CD853F",  # 秘鲁色
    "#B8860B",  # 暗金色
    "#DAA520",  # 金麒麟色
    "#F4A460",  # 沙棕色
    "#D2B48C",  # 棕褐色
]

# 渐变色映射（用于热力图等）
WARM_CMAP_COLORS = [
    "#EAE7DC",  # 最浅 - 背景色
    "#D8C3A5",  # 浅米色
    "#E98074",  # 浅珊瑚
    "#E85A4F",  # 珊瑚红
    "#D2691E",  # 巧克力色
]

# 创建自定义colormap
WARM_CMAP = LinearSegmentedColormap.from_list("warm", WARM_CMAP_COLORS)

# =============================================================================
# 图表参数
# =============================================================================

# 图表DPI（分辨率）
FIGURE_DPI = 150

# 默认图表尺寸（宽, 高）
FIGURE_SIZE = (14, 8)

# 图表样式配置
CHART_STYLE = {
    "figure.facecolor": WARM_COLORS["background"],
    "axes.facecolor": "#FFFFFF",
    "axes.edgecolor": WARM_COLORS["dark"],
    "axes.labelcolor": WARM_COLORS["dark"],
    "text.color": WARM_COLORS["dark"],
    "xtick.color": WARM_COLORS["dark"],
    "ytick.color": WARM_COLORS["dark"],
    "grid.color": WARM_COLORS["tertiary"],
    "grid.alpha": 0.5,
}

# =============================================================================
# 缓存配置
# =============================================================================

# 是否启用缓存
CACHE_ENABLED = True

# 缓存过期时间（秒）
CACHE_TTL = 3600

# =============================================================================
# GitHub API配置
# =============================================================================

# GitHub API Token（可选，用于提高API限制）
GITHUB_TOKEN = None

# Flask仓库信息
GITHUB_REPO_OWNER = "pallets"
GITHUB_REPO_NAME = "flask"
