# -*- coding: utf-8 -*-
"""
数据持久化模块
提供JSON和CSV的保存和加载功能
"""

import json
import csv
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def save_json(data: Any, filepath: str, indent: int = 2) -> bool:
    """保存数据到JSON文件"""
    try:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent, default=str)
        
        logger.debug(f"已保存JSON: {filepath}")
        return True
    except Exception as e:
        logger.error(f"保存JSON失败: {e}")
        return False


def load_json(filepath: str) -> Optional[Any]:
    """从JSON文件加载数据"""
    try:
        path = Path(filepath)
        if not path.exists():
            return None
        
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"加载JSON失败: {e}")
        return None


def save_csv(data: List[Dict], filepath: str, fieldnames: Optional[List[str]] = None) -> bool:
    """保存数据到CSV文件"""
    try:
        if not data:
            return False
        
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        if fieldnames is None:
            fieldnames = list(data[0].keys())
        
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        logger.debug(f"已保存CSV: {filepath}")
        return True
    except Exception as e:
        logger.error(f"保存CSV失败: {e}")
        return False


def load_csv(filepath: str) -> Optional[List[Dict]]:
    """从CSV文件加载数据"""
    try:
        path = Path(filepath)
        if not path.exists():
            return None
        
        with open(path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception as e:
        logger.error(f"加载CSV失败: {e}")
        return None


def backup_file(filepath: str) -> Optional[str]:
    """备份文件"""
    try:
        path = Path(filepath)
        if not path.exists():
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{timestamp}{path.suffix}")
        shutil.copy2(path, backup_path)
        
        logger.debug(f"已备份: {backup_path}")
        return str(backup_path)
    except Exception as e:
        logger.error(f"备份失败: {e}")
        return None
