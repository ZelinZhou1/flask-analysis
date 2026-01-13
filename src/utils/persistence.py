# -*- coding: utf-8 -*-
"""
数据持久化模块
提供JSON、CSV等格式的数据读写功能
"""

import csv
import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Union


class DateTimeEncoder(json.JSONEncoder):
    """处理datetime对象的JSON编码器"""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def save_json(
    data: Any, file_path: Union[str, Path], indent: int = 2, ensure_ascii: bool = False
) -> bool:
    """
    保存数据到JSON文件

    Args:
        data: 要保存的数据
        file_path: 文件路径
        indent: 缩进空格数
        ensure_ascii: 是否转义非ASCII字符

    Returns:
        是否成功
    """
    file_path = Path(file_path)

    try:
        # 确保目录存在
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(
                data, f, indent=indent, ensure_ascii=ensure_ascii, cls=DateTimeEncoder
            )
        return True

    except Exception as e:
        print(f"保存JSON失败: {file_path}, 错误: {e}")
        return False


def load_json(file_path: Union[str, Path], default: Any = None) -> Any:
    """
    从JSON文件加载数据

    Args:
        file_path: 文件路径
        default: 文件不存在或解析失败时的默认值

    Returns:
        加载的数据或默认值
    """
    file_path = Path(file_path)

    if not file_path.exists():
        return default

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"加载JSON失败: {file_path}, 错误: {e}")
        return default


def save_csv(
    data: List[Dict[str, Any]],
    file_path: Union[str, Path],
    fieldnames: Optional[List[str]] = None,
) -> bool:
    """
    保存数据到CSV文件

    Args:
        data: 字典列表
        file_path: 文件路径
        fieldnames: 列名列表，None则自动从第一行数据获取

    Returns:
        是否成功
    """
    file_path = Path(file_path)

    if not data:
        print("警告: 数据为空，跳过保存")
        return False

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if fieldnames is None:
            fieldnames = list(data[0].keys())

        with open(file_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        return True

    except Exception as e:
        print(f"保存CSV失败: {file_path}, 错误: {e}")
        return False


def load_csv(
    file_path: Union[str, Path], default: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    """
    从CSV文件加载数据

    Args:
        file_path: 文件路径
        default: 文件不存在时的默认值

    Returns:
        字典列表
    """
    file_path = Path(file_path)

    if default is None:
        default = []

    if not file_path.exists():
        return default

    try:
        with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception as e:
        print(f"加载CSV失败: {file_path}, 错误: {e}")
        return default


def save_text(
    content: str, file_path: Union[str, Path], encoding: str = "utf-8"
) -> bool:
    """
    保存文本到文件

    Args:
        content: 文本内容
        file_path: 文件路径
        encoding: 编码

    Returns:
        是否成功
    """
    file_path = Path(file_path)

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
        return True

    except Exception as e:
        print(f"保存文本失败: {file_path}, 错误: {e}")
        return False


def load_text(
    file_path: Union[str, Path], default: str = "", encoding: str = "utf-8"
) -> str:
    """
    从文件加载文本

    Args:
        file_path: 文件路径
        default: 文件不存在时的默认值
        encoding: 编码

    Returns:
        文本内容
    """
    file_path = Path(file_path)

    if not file_path.exists():
        return default

    try:
        with open(file_path, "r", encoding=encoding) as f:
            return f.read()
    except Exception as e:
        print(f"加载文本失败: {file_path}, 错误: {e}")
        return default


def append_jsonl(record: Dict[str, Any], file_path: Union[str, Path]) -> bool:
    """
    追加记录到JSONL文件（每行一个JSON对象）

    Args:
        record: 要追加的记录
        file_path: 文件路径

    Returns:
        是否成功
    """
    file_path = Path(file_path)

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, cls=DateTimeEncoder))
            f.write("\n")
        return True

    except Exception as e:
        print(f"追加JSONL失败: {file_path}, 错误: {e}")
        return False


def load_jsonl(
    file_path: Union[str, Path], default: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    """
    从JSONL文件加载数据

    Args:
        file_path: 文件路径
        default: 文件不存在时的默认值

    Returns:
        字典列表
    """
    file_path = Path(file_path)

    if default is None:
        default = []

    if not file_path.exists():
        return default

    records = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records

    except Exception as e:
        print(f"加载JSONL失败: {file_path}, 错误: {e}")
        return default


def file_exists(file_path: Union[str, Path]) -> bool:
    """检查文件是否存在"""
    return Path(file_path).exists()


def get_file_size(file_path: Union[str, Path]) -> int:
    """获取文件大小（字节）"""
    path = Path(file_path)
    if path.exists():
        return path.stat().st_size
    return 0


def get_file_mtime(file_path: Union[str, Path]) -> Optional[datetime]:
    """获取文件修改时间"""
    path = Path(file_path)
    if path.exists():
        return datetime.fromtimestamp(path.stat().st_mtime)
    return None
