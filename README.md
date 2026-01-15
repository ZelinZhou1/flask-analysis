# 🔥 Flask 仓库深度分析器

> 使用Python程序分析技术对Flask框架进行全方位代码分析与可视化

[![Python](https://img.shields.io/badge/Python-3.8+-orange?style=for-the-badge&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Target-Flask-red?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

## 📊 项目简介

本项目是一个综合性的开源软件仓库分析工具，专门用于分析 **Flask** Web框架的：

- 📈 **提交历史** - 5474+ commits 的完整分析
- 👥 **贡献者数据** - 700+ 贡献者的活动分析
- 🐛 **Issues追踪** - 2400+ issues 的状态与趋势
- 🔀 **Pull Requests** - PR 合并时间与作者分析
- 🔍 **代码结构** - AST/LibCST 静态分析
- 📐 **复杂度计算** - 圈复杂度与可维护性指数
- 🎨 **可视化输出** - 20+ 种图表（暖色系风格）

## 🛠️ 技术栈

### 课程要求技术

| 技术 | 用途 | 模块 |
|------|------|------|
| `ast` | Python AST分析 | `analyzers/ast_analyzer.py` |
| `libcst` | 具体语法树分析 | `analyzers/libcst_analyzer.py` |
| `pysnooper` | 动态追踪调试 | `analyzers/dynamic_tracer.py` |
| `z3-solver` | 符号执行/约束求解 | `analyzers/z3_analyzer.py` |

### 数据采集

| 技术 | 用途 |
|------|------|
| `PyDriller` | Git仓库数据挖掘 |
| `requests` | GitHub API调用 |

### 数据处理与可视化

| 技术 | 用途 |
|------|------|
| `pandas` | 数据处理与分析 |
| `matplotlib` | 基础图表绑定 |
| `seaborn` | 统计可视化 |
| `wordcloud` | 词云生成 |
| `networkx` | 依赖关系图 |

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 克隆Flask仓库（分析目标）

```bash
git clone https://github.com/pallets/flask.git ../flask
```

### 运行分析

```bash
# 完整分析（使用缓存）
python main.py

# 采集GitHub数据（Issues/PRs/Contributors）
python main.py --fetch

# 只采集Issues
python main.py --fetch issues

# 只采集PRs  
python main.py --fetch prs

# 只采集贡献者
python main.py --fetch contributors

# 强制重新采集Git数据
python main.py --no-cache
```

## 📁 项目结构

```
flask-analysis/
├── main.py                 # 主程序入口
├── src/
│   ├── config.py           # 配置文件
│   ├── collectors/         # 数据采集模块
│   │   ├── pydriller_collector.py  # Git数据采集
│   │   ├── issues_collector.py     # GitHub API采集
│   │   └── ...
│   ├── analyzers/          # 分析器模块
│   │   ├── ast_analyzer.py         # AST分析
│   │   ├── libcst_analyzer.py      # LibCST分析
│   │   ├── complexity_analyzer.py  # 复杂度分析
│   │   ├── z3_analyzer.py          # Z3符号执行
│   │   └── ...
│   ├── visualizers/        # 可视化模块
│   │   ├── style.py                # 暖色系样式
│   │   ├── charts.py               # 基础图表
│   │   ├── heatmap.py              # 热力图
│   │   ├── wordcloud_chart.py      # 词云
│   │   ├── charts_3d.py            # 3D图表
│   │   └── ...
│   └── utils/              # 工具模块
├── data/                   # 采集的数据
├── output/                 # 生成的图表
├── tests/                  # 测试用例
└── docs/                   # 文档
```

## 📈 输出示例

### 生成的图表类型

| 类别 | 图表 |
|------|------|
| 提交分析 | 年度统计、月度趋势、时间热力图、累积曲线 |
| 作者分析 | Top贡献者、贡献占比、活跃时间线 |
| 代码分析 | 文件类型、复杂度排行、依赖关系 |
| Issues分析 | 状态分布、时间线、标签云 |
| PRs分析 | 状态分布、合并时间、作者排行 |
| 其他 | 词云、3D图表、年度对比 |

### 配色方案

本项目采用**暖色系**（Warm Colors）配色方案：
- 主色：`#FF6B35` (橙红)
- 辅色：`#F7C59F` (杏色)
- 强调：`#EFEFD0` (米色)

## 👥 团队成员

| 成员 | 负责模块 |
|------|----------|
| ZelinZhou1 | 架构设计、主程序 |
| DUT-Abstracter | 数据采集、API |
| lff20041215 | 可视化图表 |
| liujianqi258 | 分析器模块 |
| sasageiyou | 测试与优化 |
