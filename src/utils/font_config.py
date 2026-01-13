# -*- coding: utf-8 -*-
"""
中文字体配置模块
为matplotlib图表提供中文显示支持，自动检测系统可用字体
"""

import platform
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


# Windows系统常用中文字体路径
WINDOWS_FONTS = [
    "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
    "C:/Windows/Fonts/simsun.ttc",  # 宋体
    "C:/Windows/Fonts/simhei.ttf",  # 黑体
    "C:/Windows/Fonts/simkai.ttf",  # 楷体
]

# Linux系统常用中文字体路径
LINUX_FONTS = [
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]

# macOS系统常用中文字体路径
MACOS_FONTS = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
]

# 缓存已配置的字体
_configured_font: Optional[str] = None


def _find_chinese_font() -> Optional[str]:
    """
    查找系统中可用的中文字体

    Returns:
        字体路径，如果未找到则返回None
    """
    system = platform.system()

    if system == "Windows":
        font_paths = WINDOWS_FONTS
    elif system == "Linux":
        font_paths = LINUX_FONTS
    elif system == "Darwin":
        font_paths = MACOS_FONTS
    else:
        font_paths = WINDOWS_FONTS + LINUX_FONTS + MACOS_FONTS

    for font_path in font_paths:
        if Path(font_path).exists():
            return font_path

    return None


def configure_chinese_font(font_path: Optional[str] = None) -> bool:
    """
    配置matplotlib使用中文字体

    Args:
        font_path: 可选的字体文件路径，如果不提供则自动检测

    Returns:
        配置是否成功
    """
    global _configured_font

    if font_path is None:
        font_path = _find_chinese_font()

    if font_path is None:
        print("警告: 未找到中文字体，图表中文可能无法正常显示")
        return False

    if not Path(font_path).exists():
        print(f"警告: 字体文件不存在: {font_path}")
        return False

    try:
        # 添加字体到matplotlib
        fm.fontManager.addfont(font_path)
        font_prop = fm.FontProperties(fname=font_path)
        font_name = font_prop.get_name()

        # 配置matplotlib全局字体
        plt.rcParams["font.sans-serif"] = [font_name] + plt.rcParams["font.sans-serif"]
        plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

        _configured_font = font_path
        return True

    except Exception as e:
        print(f"警告: 字体配置失败: {e}")
        return False


def get_chinese_font() -> Optional[fm.FontProperties]:
    """
    获取中文字体属性对象，用于在单个图表元素上设置字体

    Returns:
        FontProperties对象，如果未配置则返回None
    """
    global _configured_font

    if _configured_font is None:
        configure_chinese_font()

    if _configured_font is not None:
        return fm.FontProperties(fname=_configured_font)

    return None


def get_font_name() -> Optional[str]:
    """
    获取已配置的中文字体名称

    Returns:
        字体名称，如果未配置则返回None
    """
    global _configured_font

    if _configured_font is None:
        configure_chinese_font()

    if _configured_font is not None:
        font_prop = fm.FontProperties(fname=_configured_font)
        return font_prop.get_name()

    return None
