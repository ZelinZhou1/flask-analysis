import libcst as cst
from typing import Dict, List, Any
import logging

# 配置日志记录器
logger = logging.getLogger(__name__)


class ImportVisitor(cst.CSTVisitor):
    """
    LibCST 访问器，用于收集导入信息。
    """

    def __init__(self):
        self.imports = []

    def visit_Import(self, node: cst.Import) -> None:
        """访问 import 语句"""
        for name in node.names:
            self.imports.append(name.name.value)

    def visit_ImportFrom(self, node: cst.ImportFrom) -> None:
        """访问 from ... import 语句"""
        if node.module:
            # 处理模块名称
            module_name = cst.helpers.get_full_name_for_node(node.module)
            if module_name:
                self.imports.append(module_name)


class LibCSTAnalyzer:
    """
    基于 LibCST 的代码分析器。
    LibCST 保留了代码的格式信息（如注释、空格），适合进行更精细的静态分析。
    """

    def __init__(self):
        """初始化 LibCST 分析器"""
        pass

    def parse_module(self, source_code: str) -> cst.Module:
        """
        将源代码解析为 CST 模块。

        Args:
            source_code: 源代码字符串

        Returns:
            cst.Module: CST 模块对象
        """
        try:
            return cst.parse_module(source_code)
        except Exception as e:
            logger.error(f"LibCST 解析失败: {e}")
            return None

    def analyze_imports(self, source_code: str) -> List[str]:
        """
        使用 Visitor 模式提取导入的模块。

        Args:
            source_code: 源代码字符串

        Returns:
            List[str]: 导入列表
        """
        module = self.parse_module(source_code)
        if not module:
            return []

        visitor = ImportVisitor()
        module.visit(visitor)
        return visitor.imports

    def count_nodes(self, source_code: str) -> Dict[str, int]:
        """
        统计不同类型的 CST 节点数量。

        Args:
            source_code: 源代码字符串

        Returns:
            Dict: 节点类型及其计数的字典
        """
        module = self.parse_module(source_code)
        if not module:
            return {}

        stats = {"functions": 0, "classes": 0, "loops": 0, "conditionals": 0}

        # 简单的节点遍历统计
        # 注意: 这里使用简单的 isinstance 检查，实际遍历可能需要 visitor
        # 为了演示，我们使用 visitor 模式的简化版逻辑（手动 walk 或者使用 matcher）
        # 这里为了简单起见，我们定义一个统计 Visitor

        class StatVisitor(cst.CSTVisitor):
            def visit_FunctionDef(self, node: cst.FunctionDef):
                stats["functions"] += 1

            def visit_ClassDef(self, node: cst.ClassDef):
                stats["classes"] += 1

            def visit_For(self, node: cst.For):
                stats["loops"] += 1

            def visit_While(self, node: cst.While):
                stats["loops"] += 1

            def visit_If(self, node: cst.If):
                stats["conditionals"] += 1

        if module:
            module.visit(StatVisitor())

        return stats
