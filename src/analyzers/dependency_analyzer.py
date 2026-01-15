# -*- coding: utf-8 -*-
"""
依赖关系分析器
分析Python项目的模块依赖关系
"""
import ast
import os
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

logger = logging.getLogger(__name__)


class DependencyAnalyzer:
    """
    项目依赖关系分析器
    分析import语句构建依赖图
    """
    
    def __init__(self, project_path: str):
        """
        初始化分析器
        
        Args:
            project_path: 项目根目录路径
        """
        self.project_path = Path(project_path)
        self.dependencies: Dict[str, Set[str]] = defaultdict(set)
        self.external_deps: Set[str] = set()
        self.internal_deps: Dict[str, Set[str]] = defaultdict(set)
    
    def analyze_file(self, file_path: str) -> Dict[str, List[str]]:
        """
        分析单个文件的导入依赖
        
        Args:
            file_path: 文件路径
            
        Returns:
            导入信息字典
        """
        result = {
            "imports": [],
            "from_imports": [],
            "external": [],
            "internal": []
        }
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        result["imports"].append(alias.name)
                        self._classify_import(alias.name, result)
                        
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        result["from_imports"].append(node.module)
                        self._classify_import(node.module, result)
                        
        except Exception as e:
            logger.debug(f"分析文件失败 {file_path}: {e}")
        
        return result
    
    def _classify_import(self, module: str, result: Dict):
        """分类导入为内部或外部"""
        # 检查是否为相对导入或项目内模块
        root_module = module.split(".")[0]
        
        # 简单规则：标准库和第三方库视为外部
        stdlib_modules = {
            "os", "sys", "json", "re", "time", "datetime", "pathlib",
            "logging", "collections", "typing", "functools", "itertools",
            "ast", "abc", "copy", "io", "math", "random", "hashlib"
        }
        
        if root_module in stdlib_modules or module in stdlib_modules:
            result["external"].append(module)
        elif root_module in ["src", "tests", "flask", "werkzeug", "jinja2"]:
            result["internal"].append(module)
        else:
            result["external"].append(module)
    
    def analyze_project(self) -> Dict[str, any]:
        """
        分析整个项目的依赖关系
        
        Returns:
            项目依赖分析结果
        """
        all_imports = defaultdict(int)
        file_deps = {}
        
        for py_file in self.project_path.rglob("*.py"):
            if "__pycache__" in str(py_file) or ".git" in str(py_file):
                continue
            
            rel_path = str(py_file.relative_to(self.project_path))
            file_result = self.analyze_file(str(py_file))
            file_deps[rel_path] = file_result
            
            # 统计导入频率
            for imp in file_result["imports"] + file_result["from_imports"]:
                all_imports[imp] += 1
        
        # 排序导入
        sorted_imports = sorted(all_imports.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "files_analyzed": len(file_deps),
            "total_imports": sum(all_imports.values()),
            "unique_imports": len(all_imports),
            "top_imports": sorted_imports[:30],
            "file_dependencies": file_deps,
        }
    
    def get_dependency_graph(self) -> Dict[str, List[str]]:
        """
        获取可用于可视化的依赖图
        
        Returns:
            邻接表形式的依赖图
        """
        graph = {}
        
        for py_file in self.project_path.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
            
            rel_path = str(py_file.relative_to(self.project_path))
            file_result = self.analyze_file(str(py_file))
            
            # 只保留内部依赖
            graph[rel_path] = file_result.get("internal", [])
        
        return graph
