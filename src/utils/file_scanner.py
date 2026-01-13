"""
文件扫描工具
用于递归扫描项目目录，筛选指定类型的文件，并排除忽略目录。
"""

import os
import logging
import fnmatch
from typing import List, Generator, Set, Optional

# 配置日志
logger = logging.getLogger(__name__)


class FileScanner:
    """
    文件扫描器类
    """

    # 默认忽略的目录
    DEFAULT_IGNORE_DIRS = {
        ".git",
        ".idea",
        ".vscode",
        "__pycache__",
        "venv",
        "env",
        "node_modules",
        "build",
        "dist",
        "migrations",
        ".pytest_cache",
        "htmlcov",
    }

    def __init__(self, root_path: str, ignore_dirs: Optional[Set[str]] = None):
        """
        初始化文件扫描器

        Args:
            root_path: 根目录路径
            ignore_dirs: 忽略目录集合 (可选，默认使用 DEFAULT_IGNORE_DIRS)
        """
        self.root_path = os.path.abspath(root_path)
        self.ignore_dirs = (
            ignore_dirs if ignore_dirs is not None else self.DEFAULT_IGNORE_DIRS
        )

    def scan_files(
        self, extensions: Optional[List[str]] = None
    ) -> Generator[str, None, None]:
        """
        扫描文件

        Args:
            extensions: 文件扩展名列表 (如 ['.py', '.js'])，若为 None 则返回所有文件

        Yields:
            文件绝对路径
        """
        logger.info(f"开始扫描目录: {self.root_path}")
        if extensions:
            extensions = [
                ext.lower() if ext.startswith(".") else f".{ext.lower()}"
                for ext in extensions
            ]
            logger.info(f"过滤扩展名: {extensions}")

        count = 0
        for root, dirs, files in os.walk(self.root_path):
            # 修改 dirs 列表以排除忽略目录 (原地修改)
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]

            for file in files:
                if extensions:
                    _, ext = os.path.splitext(file)
                    if ext.lower() not in extensions:
                        continue

                full_path = os.path.join(root, file)
                count += 1
                yield full_path

        logger.info(f"扫描完成，共找到 {count} 个文件")

    def count_lines(self, file_path: str) -> int:
        """
        统计文件行数

        Args:
            file_path: 文件路径

        Returns:
            行数
        """
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return sum(1 for _ in f)
        except Exception as e:
            logger.warning(f"无法读取文件 {file_path}: {str(e)}")
            return 0
