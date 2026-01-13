# -*- coding: utf-8 -*-
"""
自定义异常模块
定义项目中使用的各类异常
"""

from typing import Optional


class FlaskAnalyzerError(Exception):
    """Flask分析器基础异常类"""

    def __init__(self, message: str, details: Optional[str] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)

    def __str__(self):
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message


# =============================================================================
# 分析器相关异常
# =============================================================================


class AnalyzerError(FlaskAnalyzerError):
    """代码分析器异常"""

    pass


class ASTAnalyzerError(AnalyzerError):
    """AST分析异常"""

    pass


class LibCSTAnalyzerError(AnalyzerError):
    """LibCST分析异常"""

    pass


class ComplexityAnalyzerError(AnalyzerError):
    """复杂度分析异常"""

    pass


class DependencyAnalyzerError(AnalyzerError):
    """依赖分析异常"""

    pass


# =============================================================================
# 数据采集相关异常
# =============================================================================


class CollectorError(FlaskAnalyzerError):
    """数据采集器异常"""

    pass


class GitCollectorError(CollectorError):
    """Git数据采集异常"""

    pass


class PyDrillerError(CollectorError):
    """PyDriller采集异常"""

    pass


class GitHubAPIError(CollectorError):
    """GitHub API调用异常"""

    pass


class RateLimitError(GitHubAPIError):
    """API速率限制异常"""

    pass


# =============================================================================
# 可视化相关异常
# =============================================================================


class VisualizerError(FlaskAnalyzerError):
    """可视化异常"""

    pass


class ChartGenerationError(VisualizerError):
    """图表生成异常"""

    pass


class FontConfigError(VisualizerError):
    """字体配置异常"""

    pass


class ExportError(VisualizerError):
    """导出异常"""

    pass


# =============================================================================
# 配置和IO相关异常
# =============================================================================


class ConfigError(FlaskAnalyzerError):
    """配置错误异常"""

    pass


class PathError(FlaskAnalyzerError):
    """路径错误异常"""

    pass


class CacheError(FlaskAnalyzerError):
    """缓存操作异常"""

    pass


class FileOperationError(FlaskAnalyzerError):
    """文件操作异常"""

    pass


# =============================================================================
# 验证相关异常
# =============================================================================


class ValidationError(FlaskAnalyzerError):
    """数据验证异常"""

    pass


class InvalidRepositoryError(ValidationError):
    """无效仓库异常"""

    pass


class DataFormatError(ValidationError):
    """数据格式异常"""

    pass
