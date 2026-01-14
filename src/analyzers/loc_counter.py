# src/analyzers/loc_counter.py
import os
from typing import Dict, List, Any
from pathlib import Path
from src.utils.file_scanner import FileScanner


class LOCCounter:
    """
    代码行数统计分析器
    用于统计项目中的代码行数、注释行数和空行数
    """

    def __init__(self, repo_path: str):
        """
        初始化LOC计数器

        Args:
            repo_path: 仓库根目录路径
        """
        self.repo_path = Path(repo_path)
        self.scanner = FileScanner(repo_path)

    def count_lines(self) -> Dict[str, Any]:
        """
        统计代码行数

        Returns:
            包含统计结果的字典，包括总行数、各语言行数等
        """
        stats = {
            "total_lines": 0,
            "code_lines": 0,
            "comment_lines": 0,
            "blank_lines": 0,
            "by_extension": {},
            "by_file": {},
        }

        # 获取所有相关文件
        files = self.scanner.scan_files()

        for file_path in files:
            try:
                file_stats = self._analyze_file(file_path)

                # 累加总计
                stats["total_lines"] += file_stats["total"]
                stats["code_lines"] += file_stats["code"]
                stats["comment_lines"] += file_stats["comment"]
                stats["blank_lines"] += file_stats["blank"]

                # 按文件记录
                rel_path = str(Path(file_path).relative_to(self.repo_path))
                stats["by_file"][rel_path] = file_stats

                # 按扩展名统计
                ext = Path(file_path).suffix or "no_extension"
                if ext not in stats["by_extension"]:
                    stats["by_extension"][ext] = {
                        "total": 0,
                        "code": 0,
                        "comment": 0,
                        "blank": 0,
                        "files": 0,
                    }

                stats["by_extension"][ext]["total"] += file_stats["total"]
                stats["by_extension"][ext]["code"] += file_stats["code"]
                stats["by_extension"][ext]["comment"] += file_stats["comment"]
                stats["by_extension"][ext]["blank"] += file_stats["blank"]
                stats["by_extension"][ext]["files"] += 1

            except Exception as e:
                print(f"Error analyzing file {file_path}: {e}")

        return stats

    def _analyze_file(self, file_path: str) -> Dict[str, int]:
        """
        分析单个文件的行数信息

        Args:
            file_path: 文件绝对路径

        Returns:
            包含total, code, comment, blank计数的字典
        """
        stats = {"total": 0, "code": 0, "comment": 0, "blank": 0}

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                stats["total"] = len(lines)

                for line in lines:
                    stripped = line.strip()
                    if not stripped:
                        stats["blank"] += 1
                    elif stripped.startswith("#") or stripped.startswith("//"):
                        # 简单的注释检测，对于多行注释可能不准确，但作为基础统计足够
                        stats["comment"] += 1
                    else:
                        stats["code"] += 1
        except Exception:
            pass

        return stats
