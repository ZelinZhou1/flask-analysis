# Flask Repository Analyzer 使用指南


## 基本运行

### 默认运行（分析Flask仓库）

```bash
python main.py
```

### 输出目录结构

运行后会生成以下目录：

```
data/           # 采集的原始数据
├── commits.json        # 提交历史
├── analysis_summary.json  # 分析摘要
└── ...

output/         # 生成的图表
├── annual_commits.png      # 年度提交
├── monthly_commits.png     # 月度趋势
├── top_authors.png         # 贡献者排行
├── file_types.png          # 文件类型
├── complexity_ranking.png  # 复杂度排行
└── ...
```

## 命令行选项

```bash
# 完整分析（使用缓存）
python main.py

# 采集所有GitHub数据（Issues/PRs/Contributors）
python main.py --fetch

# 只采集Issues
python main.py --fetch issues

# 只采集PRs
python main.py --fetch prs

# 只采集贡献者
python main.py --fetch contributors

# 强制重新采集Git数据（忽略缓存）
python main.py --no-cache

# 单独生成图表
python generate_charts.py

# 显示帮助
python main.py --help
```


## 配置文件

编辑 `src/config.py` 自定义配置：

```python
# Flask仓库路径
FLASK_REPO_PATH = Path("C:/Users/l/Desktop/opensource/flask")

# 输出目录
DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")

# 暖色系配色
WARM_COLORS = {
    'primary': '#E85A4F',
    'secondary': '#E98074',
    ...
}
```

## 模块说明

### 数据采集 (collectors)

- `pydriller_collector.py` - Git提交历史采集
- `github_api.py` - GitHub API调用
- `issues_collector.py` - Issues数据采集
- `contributors_collector.py` - 贡献者数据采集

### 代码分析 (analyzers)

- `ast_analyzer.py` - AST语法树分析
- `libcst_analyzer.py` - CST具体语法树分析
- `complexity_analyzer.py` - 圈复杂度分析
- `z3_analyzer.py` - 符号执行分析
- `dynamic_tracer.py` - PySnooper动态追踪

### 可视化 (visualizers)

- `charts.py` - 基础图表
- `heatmap.py` - 热力图
- `trends.py` - 趋势图
- `charts_plotly.py` - Plotly交互式图表

## 常见问题

### Q: 分析太慢？
A: Flask有5000+提交，首次需要10-30分钟。建议使用缓存。

### Q: 内存不足？
A: 减少分析范围，或增加系统内存。

### Q: 图表中文乱码？
A: 检查 `src/visualizers/style.py` 中的字体配置。
