# -*- coding: utf-8 -*-
"""
通用辅助函数模块
提供字符串处理、数值计算、目录操作等常用工具函数
"""

import os
from pathlib import Path
from typing import Any, Optional, Union


def truncate_label(label: str, max_length: int = 20, suffix: str = "...") -> str:
    """
    截断过长的标签文本，用于防止图表文字重叠

    Args:
        label: 原始标签文本
        max_length: 最大长度（包含后缀）
        suffix: 截断后添加的后缀

    Returns:
        处理后的标签文本
    """
    if len(label) <= max_length:
        return label

    return label[: max_length - len(suffix)] + suffix


def safe_divide(
    numerator: Union[int, float],
    denominator: Union[int, float],
    default: Union[int, float] = 0,
) -> float:
    """
    安全除法，避免除零错误

    Args:
        numerator: 分子
        denominator: 分母
        default: 除零时返回的默认值

    Returns:
        除法结果或默认值
    """
    if denominator == 0:
        return float(default)
    return numerator / denominator


def format_number(num: Union[int, float], precision: int = 2) -> str:
    """
    格式化数字，大数字使用K/M/B后缀

    Args:
        num: 要格式化的数字
        precision: 小数精度

    Returns:
        格式化后的字符串
    """
    if abs(num) >= 1_000_000_000:
        return f"{num / 1_000_000_000:.{precision}f}B"
    elif abs(num) >= 1_000_000:
        return f"{num / 1_000_000:.{precision}f}M"
    elif abs(num) >= 1_000:
        return f"{num / 1_000:.{precision}f}K"
    else:
        if isinstance(num, float):
            return f"{num:.{precision}f}"
        return str(num)


def format_percentage(value: float, precision: int = 1) -> str:
    """
    格式化百分比

    Args:
        value: 0-1之间的小数或0-100的百分比值
        precision: 小数精度

    Returns:
        格式化的百分比字符串
    """
    if value <= 1:
        value = value * 100
    return f"{value:.{precision}f}%"


def ensure_dir(path: Union[str, Path]) -> Path:
    """
    确保目录存在，如不存在则创建

    Args:
        path: 目录路径

    Returns:
        Path对象
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_file_extension(filename: str) -> str:
    """
    获取文件扩展名（小写，不含点）

    Args:
        filename: 文件名或路径

    Returns:
        小写的扩展名
    """
    ext = os.path.splitext(filename)[1]
    return ext.lower().lstrip(".")


def is_python_file(filename: str) -> bool:
    """
    判断是否为Python文件

    Args:
        filename: 文件名或路径

    Returns:
        是否为Python文件
    """
    return get_file_extension(filename) == "py"


def is_valid_file(filename: str, extensions: list[str]) -> bool:
    """
    检查文件是否在允许的扩展名列表中

    Args:
        filename: 文件名
        extensions: 允许的扩展名列表（不含点）

    Returns:
        是否有效
    """
    ext = get_file_extension(filename)
    return ext in [e.lower().lstrip(".") for e in extensions]


def clean_filename(filename: str) -> str:
    """
    清理文件名，移除不安全字符

    Args:
        filename: 原始文件名

    Returns:
        清理后的文件名
    """
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, "_")
    return filename


def flatten_dict(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    """
    扁平化嵌套字典

    Args:
        d: 嵌套字典
        parent_key: 父键前缀
        sep: 键分隔符

    Returns:
        扁平化后的字典
    """
    items: list = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def chunk_list(lst: list, chunk_size: int) -> list:
    """
    将列表分割成指定大小的块

    Args:
        lst: 原始列表
        chunk_size: 每块大小

    Returns:
        分块后的列表
    """
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def get_nested_value(d: dict, keys: list, default: Any = None) -> Any:
    """
    安全获取嵌套字典中的值

    Args:
        d: 字典
        keys: 键列表，如 ['a', 'b', 'c'] 表示 d['a']['b']['c']
        default: 默认值

    Returns:
        获取的值或默认值
    """
    current = d
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current
