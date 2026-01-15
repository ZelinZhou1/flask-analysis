# -*- coding: utf-8 -*-
"""
中文字体配置模块
为matplotlib图表提供中文显示支持，英文使用Consolas字体
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
]

# 缓存已配置的字体
_configured_font: Optional[str] = None
_is_configured: bool = False


def _find_chinese_font() -> Optional[str]:
    """查找系统中可用的中文字体"""
    system = platform.system()
    
    if system == "Windows":
        font_paths = WINDOWS_FONTS
    else:
        font_paths = WINDOWS_FONTS
    
    for font_path in font_paths:
        if Path(font_path).exists():
            return font_path
    
    return None


def configure_chinese_font(font_path: Optional[str] = None) -> bool:
    """
    配置matplotlib使用中文字体，英文使用Consolas
    
    Args:
        font_path: 可选的字体文件路径
        
    Returns:
        配置是否成功
    """
    global _configured_font, _is_configured
    
    if _is_configured:
        return True
    
    if font_path is None:
        font_path = _find_chinese_font()
    
    if font_path is None:
        print("警告: 未找到中文字体")
        return False
    
    if not Path(font_path).exists():
        print(f"警告: 字体文件不存在: {font_path}")
        return False
    
    try:
        # 添加字体到matplotlib
        fm.fontManager.addfont(font_path)
        font_prop = fm.FontProperties(fname=font_path)
        font_name = font_prop.get_name()
        
        # 配置全局字体：中文用微软雅黑，英文用Consolas
        plt.rcParams['font.sans-serif'] = [font_name, 'Consolas', 'DejaVu Sans']
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        
        # 设置Consolas作为等宽字体
        plt.rcParams['font.monospace'] = ['Consolas', 'DejaVu Sans Mono']
        
        _configured_font = font_path
        _is_configured = True
        return True
        
    except Exception as e:
        print(f"警告: 字体配置失败: {e}")
        return False


def get_chinese_font() -> Optional[fm.FontProperties]:
    """获取中文字体属性对象"""
    global _configured_font
    
    if _configured_font is None:
        configure_chinese_font()
    
    if _configured_font is not None:
        return fm.FontProperties(fname=_configured_font)
    
    return None


def get_font_name() -> Optional[str]:
    """获取已配置的中文字体名称"""
    global _configured_font
    
    if _configured_font is None:
        configure_chinese_font()
    
    if _configured_font is not None:
        font_prop = fm.FontProperties(fname=_configured_font)
        return font_prop.get_name()
    
    return None
