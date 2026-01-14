# src/analyzers/complexity_analyzer.py
from typing import Dict, List, Any, Optional
from pathlib import Path
import radon.complexity as radon_cc
from radon.visitors import ComplexityVisitor


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
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()

            # 使用Radon计算复杂度
            blocks = radon_cc.cc_visit(code)

            if not blocks:
                return {"average_complexity": 0, "max_complexity": 0, "functions": []}

            total_cc = sum(block.complexity for block in blocks)
            max_cc = max(block.complexity for block in blocks)

            functions = []
            for block in blocks:
                if isinstance(block, (radon_cc.Function, radon_cc.Method)):
                    functions.append(
                        {
                            "name": block.name,
                            "complexity": block.complexity,
                            "lineno": block.lineno,
                            "endline": block.endline,
                            "is_method": isinstance(block, radon_cc.Method),
                            "class_name": block.classname
                            if hasattr(block, "classname")
                            else None,
                        }
                    )

            return {
                "average_complexity": total_cc / len(blocks),
                "max_complexity": max_cc,
                "functions": sorted(
                    functions, key=lambda x: x["complexity"], reverse=True
                ),
            }

        except Exception as e:
            print(f"Error analyzing complexity for {file_path}: {e}")
            return {"error": str(e)}

    def analyze_repository(self) -> Dict[str, Any]:
        """
        分析整个仓库的复杂度

        Returns:
            仓库级的复杂度统计信息
        """
        stats = {
            "total_complexity": 0,
            "total_functions": 0,
            "high_complexity_functions": [],  # CC > 10
            "files_analyzed": 0,
        }

        for file_path in self.repo_path.rglob("*.py"):
            file_result = self.analyze_file(str(file_path))

            if "error" in file_result:
                continue

            stats["files_analyzed"] += 1
            if file_result.get("functions"):
                stats["total_complexity"] += sum(
                    f["complexity"] for f in file_result["functions"]
                )
                stats["total_functions"] += len(file_result["functions"])

                # 收集高复杂度函数
                for func in file_result["functions"]:
                    if func["complexity"] > 10:
                        func["file"] = str(file_path.relative_to(self.repo_path))
                        stats["high_complexity_functions"].append(func)

        # 计算总体平均值
        stats["average_complexity"] = (
            stats["total_complexity"] / stats["total_functions"]
            if stats["total_functions"] > 0
            else 0
        )

        # 排序高复杂度函数
        stats["high_complexity_functions"].sort(
            key=lambda x: x["complexity"], reverse=True
        )

        return stats
