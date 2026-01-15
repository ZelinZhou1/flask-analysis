# -*- coding: utf-8 -*-
"""
数据导出模块
支持导出为JSON、CSV、Markdown格式
"""
import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def export_to_json(data: Any, filepath: str, indent: int = 2) -> bool:
    """
    导出数据为JSON格式
    
    Args:
        data: 要导出的数据
        filepath: 文件路径
        indent: 缩进空格数
        
    Returns:
        是否成功
    """
    try:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent, default=str)
        
        logger.info(f"JSON导出成功: {filepath}")
        return True
    except Exception as e:
        logger.error(f"JSON导出失败: {e}")
        return False


def export_to_csv(data: List[Dict], filepath: str) -> bool:
    """
    导出数据为CSV格式
    
    Args:
        data: 字典列表
        filepath: 文件路径
        
    Returns:
        是否成功
    """
    if not data:
        logger.warning("数据为空，无法导出CSV")
        return False
    
    try:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        df = pd.DataFrame(data)
        df.to_csv(path, index=False, encoding="utf-8-sig")
        
        logger.info(f"CSV导出成功: {filepath}")
        return True
    except Exception as e:
        logger.error(f"CSV导出失败: {e}")
        return False


def export_to_markdown(data: Dict[str, Any], filepath: str, title: str = "分析报告") -> bool:
    """
    导出数据为Markdown格式报告
    
    Args:
        data: 数据字典
        filepath: 文件路径
        title: 报告标题
        
    Returns:
        是否成功
    """
    try:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        lines = [f"# {title}\n"]
        
        for key, value in data.items():
            lines.append(f"\n## {key}\n")
            
            if isinstance(value, dict):
                for k, v in value.items():
                    lines.append(f"- **{k}**: {v}")
            elif isinstance(value, list):
                for item in value[:20]:  # 限制显示数量
                    if isinstance(item, dict):
                        lines.append(f"- {item}")
                    else:
                        lines.append(f"- {item}")
            else:
                lines.append(f"{value}")
        
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        logger.info(f"Markdown导出成功: {filepath}")
        return True
    except Exception as e:
        logger.error(f"Markdown导出失败: {e}")
        return False


def load_json(filepath: str) -> Optional[Any]:
    """
    从JSON文件加载数据
    
    Args:
        filepath: 文件路径
        
    Returns:
        加载的数据
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"JSON加载失败: {e}")
        return None


def load_csv(filepath: str) -> Optional[pd.DataFrame]:
    """
    从CSV文件加载数据
    
    Args:
        filepath: 文件路径
        
    Returns:
        DataFrame
    """
    try:
        return pd.read_csv(filepath, encoding="utf-8-sig")
    except Exception as e:
        logger.error(f"CSV加载失败: {e}")
        return None
