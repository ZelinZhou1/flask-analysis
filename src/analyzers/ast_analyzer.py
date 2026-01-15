import ast
import logging
from typing import Dict, List, Any, Optional

try:
    from radon.complexity import cc_visit, cc_rank
    RADON_AVAILABLE = True
except ImportError:
    cc_visit = None
    cc_rank = None
    RADON_AVAILABLE = False

logger = logging.getLogger(__name__)


class ASTAnalyzer:
    """
    基于 AST (Abstract Syntax Tree) 的代码分析器。
    用于分析代码的圈复杂度、提取类和函数定义等结构信息。
    """

    def __init__(self):
        """初始化 AST 分析器"""
        pass

    def parse_code(self, source_code: str) -> Optional[ast.AST]:
        """
        解析源代码为 AST 对象。

        Args:
            source_code: 源代码字符串

        Returns:
            ast.AST: 解析后的 AST 对象，如果解析失败返回 None
        """
        try:
            return ast.parse(source_code)
        except SyntaxError as e:
            logger.error(f"AST解析错误: {e}")
            return None

    def calculate_complexity(self, source_code: str) -> List[Dict[str, Any]]:
        """
        使用 Radon 计算代码的圈复杂度 (Cyclomatic Complexity)。

        Args:
            source_code: 源代码字符串

        Returns:
            List[Dict]: 包含每个函数/方法的复杂度信息的列表
        """
        if not RADON_AVAILABLE or cc_visit is None:
            return []
        try:
            blocks = cc_visit(source_code)
            results = []
            for block in blocks:
                results.append(
                    {
                        "name": block.name,
                        "type": getattr(block, 'type', 'unknown'),
                        "complexity": block.complexity,
                        "rank": cc_rank(block.complexity) if cc_rank else 'N/A',
                        "lineno": block.lineno,
                        "endline": getattr(block, 'endline', block.lineno),
                    }
                )
            return results
        except Exception as e:
            logger.error(f"圈复杂度计算失败: {e}")
            return []

    def extract_definitions(self, source_code: str) -> Dict[str, List[str]]:
        """
        从源代码中提取类和函数的名称。

        Args:
            source_code: 源代码字符串

        Returns:
            Dict: 包含 'classes' 和 'functions' 列表的字典
        """
        tree = self.parse_code(source_code)
        if not tree:
            return {"classes": [], "functions": []}

        definitions = {"classes": [], "functions": []}

        # 遍历 AST 节点
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                definitions["classes"].append(node.name)
            elif isinstance(node, ast.FunctionDef):
                definitions["functions"].append(node.name)
            elif isinstance(node, ast.AsyncFunctionDef):
                definitions["functions"].append(node.name)

        return definitions

    def analyze_imports(self, source_code: str) -> List[str]:
        """
        提取代码中的导入语句。

        Args:
            source_code: 源代码字符串

        Returns:
            List[str]: 导入的模块名称列表
        """
        tree = self.parse_code(source_code)
        if not tree:
            return []

        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        return list(set(imports))
