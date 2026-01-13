# Flask Repository Analyzer

> 🔍 Flask 仓库综合分析工具 - 使用 PyDriller、LibCST、Z3 等高级技术进行深度代码分析

## 📖 项目简介

Flask Repository Analyzer 是一个专门用于分析 Flask 仓库的综合性工具。它结合了多种先进的代码分析技术，能够从多个维度深入分析代码库，并生成 20+ 张精美的暖色系可视化图表。

## ✨ 主要特性

- **PyDriller 集成**: 替代传统 subprocess 进行 Git 历史分析
- **LibCST 代码分析**: 精确的 Python 代码结构分析
- **Z3 符号执行**: 约束求解与路径分析
- **PySnooper 动态追踪**: 运行时行为分析
- **Radon 复杂度分析**: 圈复杂度和维护性指数计算
- **20+ 可视化图表**: 暖色系配色，支持中文，无文字交叠

## 📊 生成的图表

### 静态图表 (Matplotlib/Seaborn)
1. 年度提交柱状图
2. 月度提交趋势图
3. 作者贡献饼图
4. 作者提交排行榜
5. 文件修改热力图
6. 提交时间热力图（小时 x 星期）
7. 代码行数变化图
8. 文件类型分布饼图
9. 圈复杂度分布图
10. 高复杂度函数排行
11. 提交消息词云
12. 分支统计图
13. 标签版本时间线
14. Issue 状态分布
15. Issue 标签分布
16. 贡献者排行榜
17. 依赖关系网络图
18. 代码增删趋势图
19. 维护性指数分布
20. 函数参数数量分布
21. 装饰器使用统计
22. 类继承关系图

### 交互式图表 (Plotly)
23. 3D 提交时间分布
24. 交互式作者活动图
25. 交互式文件热力图

## 🛠️ 技术栈

| 分类 | 技术 |
|------|------|
| Git 分析 | PyDriller, GitPython |
| 代码分析 | LibCST, Radon, AST |
| 符号执行 | Z3-solver |
| 动态追踪 | PySnooper |
| 数据处理 | Pandas, NumPy |
| 静态可视化 | Matplotlib, Seaborn, WordCloud |
| 交互式可视化 | Plotly |
| 网络图 | NetworkX |
| API 调用 | Requests |

## 📁 项目结构

```
flask-repo-analyzer/
├── config.py              # 配置（暖色系）
├── constants.py           # 常量定义
├── exceptions.py          # 自定义异常
├── main.py                # 主程序入口
├── collectors/            # 数据采集器
│   ├── pydriller_collector.py
│   ├── branch_collector.py
│   ├── tag_collector.py
│   ├── github_api.py
│   ├── issues_collector.py
│   └── contributors_collector.py
├── analyzers/             # 代码分析器
│   ├── ast_analyzer.py
│   ├── libcst_analyzer.py
│   ├── dynamic_tracer.py
│   ├── z3_analyzer.py
│   ├── stats.py
│   ├── message_analyzer.py
│   ├── loc_counter.py
│   ├── dependency_analyzer.py
│   └── pr_analyzer.py
├── visualizers/           # 可视化模块
│   ├── style.py
│   ├── charts.py
│   ├── heatmap.py
│   ├── trends.py
│   ├── author_charts.py
│   ├── file_charts.py
│   ├── complexity_charts.py
│   ├── message_charts.py
│   ├── yearly_charts.py
│   ├── dependency_charts.py
│   ├── issues_charts.py
│   ├── contributors_charts.py
│   ├── pr_charts.py
│   └── charts_plotly.py
├── utils/                 # 工具模块
│   ├── font_config.py
│   ├── cache.py
│   ├── persistence.py
│   ├── helpers.py
│   ├── date_utils.py
│   ├── exporter.py
│   └── file_scanner.py
├── tests/                 # 测试文件
├── docs/                  # 文档
├── data/                  # 生成的数据
└── output/                # 生成的图表
```

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行分析

```bash
python main.py
```

### 查看结果

- 数据文件: `data/` 目录
- 图表文件: `output/` 目录

## ⚙️ 配置

编辑 `config.py` 文件自定义配置：

```python
# Flask 仓库路径
FLASK_REPO_PATH = "C:/Users/l/Desktop/opensource/flask"

# 暖色系配色
WARM_COLORS = {
    'primary': '#E85A4F',
    'secondary': '#E98074',
    'tertiary': '#D8C3A5',
    'background': '#EAE7DC',
    'accent': '#8E8D8A',
    'dark': '#4A4A48',
}
```

## 📋 开发团队

- Alice Chen
- Bob Wang
- Charlie Liu
- Diana Zhang
- Edward Wu

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

Made with ❤️ for Flask community
