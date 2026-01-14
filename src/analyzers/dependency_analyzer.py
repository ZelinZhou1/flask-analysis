# src/analyzers/dependency_analyzer.py
import ast
import os
from pathlib import Path
from typing import Dict, List, Set, Any, Tuple
import networkx as nx


class DependencyAnalyzer:
    """
    依赖关系分析器
    使用NetworkX构建项目内部文件之间的依赖关系图
    """

    def __init__(self, repo_path: str):
        """
        初始化依赖分析器

        Args:
            repo_path: 仓库根目录路径
        """
        self.repo_path = Path(repo_path)
        self.graph = nx.DiGraph()

    def analyze(self) -> nx.DiGraph:
        """
        分析项目依赖关系

        Returns:
            NetworkX有向图，节点为文件相对路径，边表示导入关系
        """
        self.graph.clear()
        python_files = self._get_python_files()

        # 添加所有节点
        for file_path in python_files:
            rel_path = self._get_rel_path(file_path)
            self.graph.add_node(rel_path, size=os.path.getsize(file_path))

        # 分析导入构建边
        for file_path in python_files:
            source_node = self._get_rel_path(file_path)
            imports = self._get_imports(file_path)

            for module_name in imports:
                target_node = self._resolve_import(module_name, file_path)
                if target_node and self.graph.has_node(target_node):
                    self.graph.add_edge(source_node, target_node)

        return self.graph

    def get_stats(self) -> Dict[str, Any]:
        """
        获取依赖图的统计信息

        Returns:
            包含节点数、边数、密度、中心性等信息的字典
        """
        if not self.graph.nodes:
            self.analyze()

        try:
            stats = {
                "node_count": self.graph.number_of_nodes(),
                "edge_count": self.graph.number_of_edges(),
                "density": nx.density(self.graph),
                "avg_degree": sum(d for n, d in self.graph.degree())
                / float(self.graph.number_of_nodes())
                if self.graph.number_of_nodes() > 0
                else 0,
                "top_centrality": sorted(
                    nx.degree_centrality(self.graph).items(),
                    key=lambda x: x[1],
                    reverse=True,
                )[:5],
            }
        except Exception as e:
            stats = {"error": str(e)}

        return stats

    def _get_python_files(self) -> List[Path]:
        """获取所有Python文件"""
        return list(self.repo_path.rglob("*.py"))

    def _get_rel_path(self, path: Path) -> str:
        """获取相对路径（作为节点ID）"""
        return str(path.relative_to(self.repo_path)).replace(os.sep, "/")

    def _get_imports(self, file_path: Path) -> Set[str]:
        """
        解析文件获取导入的模块名

        Args:
            file_path: Python文件路径

        Returns:
            导入的模块名集合
        """
        imports = set()
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=str(file_path))

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module)
        except Exception:
            pass
        return imports

    def _resolve_import(self, module_name: str, current_file: Path) -> str:
        """
        将模块名解析为文件相对路径
        这是一个简化的解析逻辑，主要处理项目内引用

        Args:
            module_name: 导入的模块名 (e.g., 'src.utils')
            current_file: 当前文件路径

        Returns:
            对应的文件相对路径或None
        """
        # 尝试直接映射 module.name -> module/name.py
        parts = module_name.split(".")
        potential_path = self.repo_path.joinpath(*parts).with_suffix(".py")

        if potential_path.exists():
            return self._get_rel_path(potential_path)

        # 尝试 module.name -> module/name/__init__.py
        potential_init = self.repo_path.joinpath(*parts).joinpath("__init__.py")
        if potential_init.exists():
            return self._get_rel_path(potential_init)

        return None
