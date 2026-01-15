# -*- coding: utf-8 -*-
"""
代码行数统计分析模块
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

LANGUAGE_EXTENSIONS = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".html": "HTML",
    ".css": "CSS",
    ".json": "JSON",
    ".md": "Markdown",
    ".rst": "reStructuredText",
    ".yml": "YAML",
    ".yaml": "YAML",
    ".txt": "Text",
    ".sh": "Shell",
    ".bat": "Batch",
    ".sql": "SQL",
    ".xml": "XML",
    ".toml": "TOML",
    ".ini": "INI",
    ".cfg": "Config",
}

IGNORE_DIRS = {
    "__pycache__", ".git", ".svn", ".hg", "node_modules",
    "venv", ".venv", "env", ".env", "build", "dist",
    ".tox", ".pytest_cache", ".mypy_cache", ".eggs",
}


class LOCAnalyzer:
    """代码行数分析器"""
    
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.stats: Dict[str, Dict] = defaultdict(lambda: {"files": 0, "lines": 0, "blank": 0, "comment": 0})
    
    def count_lines(self, file_path: Path) -> Tuple[int, int, int]:
        """
        统计文件行数
        
        Returns:
            (总行数, 空行数, 注释行数)
        """
        total = 0
        blank = 0
        comment = 0
        
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                in_multiline_comment = False
                
                for line in f:
                    total += 1
                    stripped = line.strip()
                    
                    if not stripped:
                        blank += 1
                        continue
                    
                    if file_path.suffix == ".py":
                        if stripped.startswith('"""') or stripped.startswith("'''"):
                            if in_multiline_comment:
                                in_multiline_comment = False
                            else:
                                in_multiline_comment = True
                            comment += 1
                        elif in_multiline_comment:
                            comment += 1
                        elif stripped.startswith("#"):
                            comment += 1
                    elif file_path.suffix in [".js", ".ts", ".css"]:
                        if stripped.startswith("//"):
                            comment += 1
                        elif stripped.startswith("/*"):
                            in_multiline_comment = True
                            comment += 1
                        elif stripped.endswith("*/"):
                            in_multiline_comment = False
                            comment += 1
                        elif in_multiline_comment:
                            comment += 1
                    elif file_path.suffix == ".html":
                        if "<!--" in stripped:
                            comment += 1
                            
        except Exception as e:
            logger.debug(f"无法读取文件 {file_path}: {e}")
        
        return total, blank, comment
    
    def analyze(self) -> Dict[str, Dict]:
        """分析整个目录"""
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for filename in files:
                file_path = Path(root) / filename
                ext = file_path.suffix.lower()
                
                if ext in LANGUAGE_EXTENSIONS:
                    lang = LANGUAGE_EXTENSIONS[ext]
                    total, blank, comment = self.count_lines(file_path)
                    
                    self.stats[lang]["files"] += 1
                    self.stats[lang]["lines"] += total
                    self.stats[lang]["blank"] += blank
                    self.stats[lang]["comment"] += comment
        
        return dict(self.stats)
    
    def get_summary(self) -> Dict:
        """获取汇总统计"""
        total_files = sum(s["files"] for s in self.stats.values())
        total_lines = sum(s["lines"] for s in self.stats.values())
        total_blank = sum(s["blank"] for s in self.stats.values())
        total_comment = sum(s["comment"] for s in self.stats.values())
        
        return {
            "total_files": total_files,
            "total_lines": total_lines,
            "total_blank": total_blank,
            "total_comment": total_comment,
            "code_lines": total_lines - total_blank - total_comment,
            "by_language": dict(self.stats),
        }
