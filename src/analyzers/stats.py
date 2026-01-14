import os
import logging
from typing import Dict, Any, List

# 配置日志记录器
logger = logging.getLogger(__name__)


class CodeStats:
    """
    基础代码统计分析器。
    用于统计行数、文件大小、字符数等基础指标。
    """

    def __init__(self):
        """初始化统计分析器"""
        pass

    def count_lines(self, content: str) -> Dict[str, int]:
        """
        统计代码行数信息。

        Args:
            content: 文件内容

        Returns:
            Dict: 包含总行数、空行数、注释行数（估算）的字典
        """
        lines = content.splitlines()
        total_lines = len(lines)
        empty_lines = len([l for l in lines if not l.strip()])
        # 简单的注释统计（以 # 开头）
        comment_lines = len([l for l in lines if l.strip().startswith("#")])

        code_lines = total_lines - empty_lines - comment_lines

        return {
            "total": total_lines,
            "empty": empty_lines,
            "comment": comment_lines,
            "code": code_lines,
        }

    def analyze_file_stats(self, file_path: str) -> Dict[str, Any]:
        """
        获取文件的基础统计信息。

        Args:
            file_path: 文件绝对路径

        Returns:
            Dict: 文件统计信息
        """
        try:
            stats = os.stat(file_path)
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            line_stats = self.count_lines(content)

            return {
                "size_bytes": stats.st_size,
                "line_stats": line_stats,
                "extension": os.path.splitext(file_path)[1],
            }
        except Exception as e:
            logger.error(f"统计文件 {file_path} 失败: {e}")
            return {}

    def analyze_directory(self, dir_path: str) -> Dict[str, Any]:
        """
        统计整个目录的代码信息。

        Args:
            dir_path: 目录路径

        Returns:
            Dict: 汇总统计信息
        """
        summary = {
            "files": 0,
            "total_lines": 0,
            "total_code": 0,
            "total_size": 0,
            "languages": {},
            "avg_file_size": 0,
            "max_file_size": 0,
        }

        for root, _, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                # 跳过隐藏文件和特定目录
                if file.startswith(".") or "venv" in root or "__pycache__" in root:
                    continue

                file_stats = self.analyze_file_stats(file_path)
                if file_stats:
                    summary["files"] += 1
                    summary["total_lines"] += file_stats["line_stats"]["total"]
                    summary["total_code"] += file_stats["line_stats"]["code"]
                    summary["total_size"] += file_stats["size_bytes"]
                    summary["max_file_size"] = max(
                        summary["max_file_size"], file_stats["size_bytes"]
                    )

                    ext = file_stats["extension"]
                    summary["languages"][ext] = summary["languages"].get(ext, 0) + 1

        if summary["files"] > 0:
            summary["avg_file_size"] = summary["total_size"] / summary["files"]

        return summary
