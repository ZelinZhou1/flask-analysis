# -*- coding: utf-8 -*-
"""
常量定义模块
包含提交类型、文件扩展名映射、分析参数等常量
"""

# =============================================================================
# Git提交类型
# =============================================================================

COMMIT_TYPES = {
    "feat": "新功能",
    "fix": "修复Bug",
    "docs": "文档更新",
    "style": "代码格式",
    "refactor": "代码重构",
    "test": "测试相关",
    "chore": "构建/工具",
    "perf": "性能优化",
    "ci": "持续集成",
    "build": "构建系统",
    "revert": "回滚提交",
}

# =============================================================================
# 文件扩展名映射
# =============================================================================

FILE_EXTENSIONS = {
    # Python
    ".py": "Python",
    ".pyx": "Cython",
    ".pyi": "Python Stub",
    # Web前端
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".jsx": "React JSX",
    ".tsx": "React TSX",
    ".html": "HTML",
    ".htm": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".sass": "Sass",
    ".less": "Less",
    # 配置和数据
    ".json": "JSON",
    ".yaml": "Configuration",
    ".yml": "Configuration",
    ".toml": "Configuration",
    ".ini": "Configuration",
    ".cfg": "Configuration",
    ".conf": "Configuration",
    ".dockerfile": "Configuration",
    "Dockerfile": "Configuration",
    # 数据库
    ".sql": "Database",
    ".db": "Database",
    ".sqlite": "Database",
    ".sqlite3": "Database",
    # 脚本
    ".sh": "Shell",
    ".bash": "Shell",
    ".bat": "Batch",
    ".ps1": "PowerShell",
    ".xml": "XML",
}

# 需要分析的文件扩展名
ANALYZABLE_EXTENSIONS = {".py", ".pyx", ".pyi"}

# 忽略的目录
IGNORED_DIRECTORIES = {
    "__pycache__",
    ".git",
    ".svn",
    ".hg",
    "node_modules",
    "venv",
    ".venv",
    "env",
    ".env",
    ".tox",
    ".pytest_cache",
    ".mypy_cache",
    "build",
    "dist",
    "*.egg-info",
}

# 忽略的文件
IGNORED_FILES = {
    ".gitignore",
    ".gitattributes",
    ".DS_Store",
    "Thumbs.db",
}

# =============================================================================
# 分析参数
# =============================================================================

# 圈复杂度阈值
COMPLEXITY_THRESHOLDS = {
    "low": 5,  # 低复杂度
    "moderate": 10,  # 中等复杂度
    "high": 20,  # 高复杂度
    "very_high": 30,  # 非常高复杂度
}

# 函数参数数量阈值
PARAMS_THRESHOLDS = {
    "good": 3,  # 良好
    "acceptable": 5,  # 可接受
    "too_many": 7,  # 过多
}

# 代码行数阈值
LOC_THRESHOLDS = {
    "small": 100,  # 小文件
    "medium": 500,  # 中等文件
    "large": 1000,  # 大文件
}

# =============================================================================
# 图表标签
# =============================================================================

CHART_LABELS = {
    "commits": "提交次数",
    "authors": "作者",
    "files": "文件",
    "lines": "代码行数",
    "additions": "新增行数",
    "deletions": "删除行数",
    "complexity": "圈复杂度",
    "date": "日期",
    "month": "月份",
    "year": "年份",
    "hour": "小时",
    "weekday": "星期",
    "count": "数量",
    "percentage": "百分比",
}

# 星期几标签
WEEKDAY_LABELS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

# 月份标签
MONTH_LABELS = [
    "一月",
    "二月",
    "三月",
    "四月",
    "五月",
    "六月",
    "七月",
    "八月",
    "九月",
    "十月",
    "十一月",
    "十二月",
]
