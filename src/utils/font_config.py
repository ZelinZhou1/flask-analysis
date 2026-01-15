# -*- coding: utf-8 -*-
"""
中文字体配置模块
确保matplotlib图表中文正常显示
"""

import platform
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

_configured = False


def configure_chinese_font() -> bool:
    """配置中文字体"""
    global _configured
    
    if _configured:
        return True
    
    warnings.filterwarnings('ignore', category=UserWarning)
    
    if platform.system() == "Windows":
        font_path = Path("C:/Windows/Fonts/msyh.ttc")
        if font_path.exists():
            try:
                fm.fontManager.addfont(str(font_path))
                font_prop = fm.FontProperties(fname=str(font_path))
                font_name = font_prop.get_name()
                
                plt.rcParams['font.sans-serif'] = [font_name, 'Microsoft YaHei', 'SimHei', 'DejaVu Sans']
            except Exception as e:
                plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
        else:
            plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
    else:
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.unicode_minus'] = False
    
    _configured = True
    return True


def get_chinese_font():
    """获取中文字体属性"""
    configure_chinese_font()
    font_path = Path("C:/Windows/Fonts/msyh.ttc")
    if font_path.exists():
        return fm.FontProperties(fname=str(font_path))
    return None


def get_font_name() -> str:
    """获取字体名称"""
    return "Microsoft YaHei"
