# -*- coding: utf-8 -*-
"""
中文字体配置模块
为matplotlib图表提供完整的中文显示支持
"""

import platform
from pathlib import Path
from typing import Optional
import warnings

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

_is_configured: bool = False


def configure_chinese_font() -> bool:
    """
    配置matplotlib使用中文字体
    """
    global _is_configured
    
    if _is_configured:
        return True
    
    # 抑制字体警告
    warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')
    
    system = platform.system()
    
    if system == "Windows":
        # Windows系统字体
        font_options = [
            "Microsoft YaHei",
            "SimHei", 
            "SimSun",
            "KaiTi",
        ]
        
        # 配置字体
        plt.rcParams['font.sans-serif'] = font_options + ['DejaVu Sans']
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['axes.unicode_minus'] = False
        
        # 尝试直接添加字体文件
        font_paths = [
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simhei.ttf",
        ]
        
        for fp in font_paths:
            if Path(fp).exists():
                try:
                    fm.fontManager.addfont(fp)
                except:
                    pass
    else:
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    
    _is_configured = True
    return True


def get_chinese_font() -> Optional[fm.FontProperties]:
    """获取中文字体属性对象"""
    configure_chinese_font()
    
    font_path = "C:/Windows/Fonts/msyh.ttc"
    if Path(font_path).exists():
        return fm.FontProperties(fname=font_path)
    
    return None


def get_font_name() -> str:
    """获取配置的中文字体名称"""
    configure_chinese_font()
    return "Microsoft YaHei"
