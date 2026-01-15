# src/analyzers/complexity_analyzer.py
"""
复杂度分析器模块
使用Radon库计算Python代码的圈复杂度(Cyclomatic Complexity)
"""
from typing import Dict, List, Any, Optional
from pathlib import Path

try:
    from radon.complexity import cc_visit, cc_rank
    RADON_AVAILABLE = True
except ImportError:
    RADON_AVAILABLE = False
    cc_visit = None
    cc_rank = None


class ComplexityAnalyzer:
    """
    代码复杂度分析器
    使用Radon计算圈复杂度(Cyclomatic Complexity)
    """

    def __init__(self, repo_path: str):
        """
        初始化复杂度分析器

        Args:
            repo_path: 仓库根目录路径
        """
        self.repo_path = Path(repo_path)

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        分析单个文件的复杂度

        Args:
            file_path: 文件绝对路径

        Returns:
            包含平均复杂度、最大复杂度和函数级详细信息的字典
        """
        if not RADON_AVAILABLE:
            return {"error": "radon not installed", "functions": []}
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()

            blocks = cc_visit(code)

            if not blocks:
                return {"average_complexity": 0, "max_complexity": 0, "functions": []}

            total_cc = sum(block.complexity for block in blocks)
            max_cc = max(block.complexity for block in blocks)

            functions = []
            for block in blocks:
                functions.append({
                    "name": block.name,
                    "complexity": block.complexity,
                    "lineno": block.lineno,
                    "endline": getattr(block, 'endline', block.lineno),
                    "is_method": block.is_method if hasattr(block, 'is_method') else False,
                    "class_name": getattr(block, 'classname', None),
                    "rank": cc_rank(block.complexity) if cc_rank else 'N/A',
                })

            return {
                "average_complexity": total_cc / len(blocks),
                "max_complexity": max_cc,
                "functions": sorted(
                    functions, key=lambda x: x["complexity"], reverse=True
                ),
            }

        except Exception as e:
            return {"error": str(e), "functions": []}

    def analyze_repository(self) -> Dict[str, Any]:
        """
        分析整个仓库的复杂度

        Returns:
            仓库级的复杂度统计信息
        """
        stats = {
            "total_complexity": 0,
            "total_functions": 0,
            "high_complexity_functions": [],
            "files_analyzed": 0,
            "average_complexity": 0,
        }

        if not RADON_AVAILABLE:
            stats["error"] = "radon not installed"
            return stats

        for file_path in self.repo_path.rglob("*.py"):
            if '__pycache__' in str(file_path) or '.git' in str(file_path):
                continue
                
            file_result = self.analyze_file(str(file_path))

            if "error" in file_result:
                continue

            stats["files_analyzed"] += 1
            if file_result.get("functions"):
                stats["total_complexity"] += sum(
                    f["complexity"] for f in file_result["functions"]
                )
                stats["total_functions"] += len(file_result["functions"])

                for func in file_result["functions"]:
                    if func["complexity"] > 10:
                        func["file"] = str(file_path.relative_to(self.repo_path))
                        stats["high_complexity_functions"].append(func)

        if stats["total_functions"] > 0:
            stats["average_complexity"] = stats["total_complexity"] / stats["total_functions"]

        stats["high_complexity_functions"].sort(
            key=lambda x: x["complexity"], reverse=True
        )

        return stats
