# -*- coding: utf-8 -*-
"""
通用辅助函数
"""

from typing import Union, Optional
import os
from pathlib import Path


def truncate_label(label: str, max_len: int = 20) -> str:
    """截断标签"""
    if len(label) > max_len:
        return label[:max_len-2] + ".."
    return label


def safe_divide(a: Union[int, float], b: Union[int, float], default: float = 0.0) -> float:
    """安全除法"""
    if b == 0:
        return default
    return a / b


def format_number(n: Union[int, float], precision: int = 2) -> str:
    """格式化数字"""
    if isinstance(n, float):
        return f"{n:.{precision}f}"
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


def ensure_dir(path: Union[str, Path]) -> Path:
    """确保目录存在"""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def get_file_extension(filename: str) -> str:
    """获取文件扩展名"""
    return Path(filename).suffix.lower()


def is_code_file(filename: str) -> bool:
    """判断是否为代码文件"""
    code_extensions = {".py", ".js", ".ts", ".html", ".css", ".json", ".yml", ".yaml", ".md", ".rst"}
    return get_file_extension(filename) in code_extensions


def bytes_to_human(size: int) -> str:
    """字节转人类可读格式"""
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"
