# docs/API.md
"""
API参考文档 - Flask仓库分析工具
"""

# API 参考文档

本文档详细描述了Flask Repository Analyzer的所有公共API接口。

## 数据采集模块 (collectors)

### PyDrillerCollector

Git仓库历史采集器，使用PyDriller库进行仓库挖掘。

```python
from src.collectors.pydriller_collector import PyDrillerCollector

collector = PyDrillerCollector(repo_path="/path/to/repo", branch="main")

# 采集所有提交
for commit in collector.collect_commits():
    print(commit["hash"], commit["author_name"])

# 采集特定作者的提交
commits = collector.collect_commits_by_author("Armin")

# 采集文件变更历史
history = collector.collect_file_history("src/flask/app.py")
```

### GitHubAPI

GitHub REST API封装，用于获取Issues、PRs、Contributors等数据。

```python
from src.collectors.github_api import GitHubAPI

api = GitHubAPI(repo="pallets/flask", token="your_token")

# 获取Issues
issues = api.get_issues(state="all", max_pages=10)

# 获取贡献者
contributors = api.get_contributors()

# 获取PR
prs = api.get_pull_requests(state="closed")
```

## 代码分析模块 (analyzers)

### ASTAnalyzer

Python AST分析器，提取代码结构信息。

```python
from src.analyzers.ast_analyzer import ASTAnalyzer

analyzer = ASTAnalyzer()

# 解析代码
tree = analyzer.parse_code(source_code)

# 计算圈复杂度
complexity = analyzer.calculate_complexity(source_code)

# 提取定义
definitions = analyzer.extract_definitions(source_code)
# 返回: {"classes": [...], "functions": [...]}

# 分析导入
imports = analyzer.analyze_imports(source_code)
```

### ComplexityAnalyzer

代码复杂度分析器，使用Radon计算圈复杂度。

```python
from src.analyzers.complexity_analyzer import ComplexityAnalyzer

analyzer = ComplexityAnalyzer("/path/to/repo")

# 分析单个文件
result = analyzer.analyze_file("app.py")

# 分析整个仓库
stats = analyzer.analyze_repository()
# 返回: {
#     "average_complexity": 2.5,
#     "total_functions": 500,
#     "high_complexity_functions": [...]
# }
```

### LibCSTAnalyzer

LibCST具体语法树分析器。

```python
from src.analyzers.libcst_analyzer import LibCSTAnalyzer

analyzer = LibCSTAnalyzer()
result = analyzer.analyze_code(source_code)
```

### Z3Analyzer

Z3符号执行分析器。

```python
from src.analyzers.z3_analyzer import Z3Analyzer

analyzer = Z3Analyzer()
result = analyzer.analyze_constraints(constraints)
```

### DynamicTracer

PySnooper动态追踪器。

```python
from src.analyzers.dynamic_tracer import DynamicTracer

tracer = DynamicTracer(output_file="trace.log")
tracer.trace_function(my_function, args)
```

## 可视化模块 (visualizers)

### 基础图表

```python
from src.visualizers import charts

# 柱状图
charts.plot_bar(data, title, xlabel, ylabel, output_path)

# 横向柱状图
charts.plot_horizontal_bar(data, title, xlabel, ylabel, output_path)

# 饼图
charts.plot_pie(data, title, output_path)

# 折线图
charts.plot_line(data, title, xlabel, ylabel, output_path)
```

### 热力图

```python
from src.visualizers import heatmap

heatmap.plot_commit_heatmap(commits_df, output_path)
heatmap.plot_file_heatmap(file_changes, output_path)
```

### Plotly交互式图表

```python
from src.visualizers import charts_plotly

charts_plotly.plot_3d_commits(commits_df, output_path)
charts_plotly.plot_interactive_timeline(data, output_path)
```

## 工具模块 (utils)

### 字体配置

```python
from src.utils.font_config import configure_fonts

configure_fonts()  # 配置中文字体支持
```

### 缓存

```python
from src.utils.cache import Cache

cache = Cache("cache_dir")
cache.set("key", data, ttl=3600)
data = cache.get("key")
```

### 持久化

```python
from src.utils.persistence import save_json, load_json

save_json(data, "output.json")
data = load_json("output.json")
```
