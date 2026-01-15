# docs/INSTALL.md
"""
安装指南文档 - Flask仓库分析工具
"""

# Flask Repository Analyzer 安装指南

## 系统要求

- Python 3.8+
- Git 2.0+
- 网络连接（用于GitHub API）
- Windows/Linux/macOS

## 安装步骤

### 1. 克隆项目仓库

```bash
git clone https://github.com/ZelinZhou1/flask-analysis.git
cd flask-analysis
```

### 2. 克隆Flask仓库（分析目标）

```bash
cd ..
git clone https://github.com/pallets/flask.git
cd flask-analysis
```

### 3. 创建虚拟环境

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

## 依赖说明

| 包名 | 版本 | 用途 |
|------|------|------|
| pydriller | >=2.9 | Git仓库挖掘 |
| pandas | >=1.5.0 | 数据分析 |
| matplotlib | >=3.6.0 | 图表生成 |
| seaborn | >=0.12.0 | 统计可视化 |
| plotly | >=5.0.0 | 交互式图表 |
| wordcloud | >=1.8.0 | 词云生成 |
| networkx | >=3.0 | 依赖关系图 |
| radon | >=6.0.1 | 圈复杂度分析 |
| libcst | >=0.4.0 | CST分析 |
| pysnooper | >=1.1.0 | 动态追踪 |
| z3-solver | >=4.12.0 | 符号执行 |
| requests | >=2.28.0 | HTTP请求 |

## 验证安装

```bash
python -c "from src.config import FLASK_REPO_PATH; print('安装成功!')"
python -m pytest tests/ -v
```

## 常见问题

### Q: pydriller安装失败？
A: 尝试升级pip：`pip install --upgrade pip`

### Q: 中文图表显示方框？
A: 项目已配置中文字体，请确保系统安装了微软雅黑或黑体。

### Q: 运行太慢？
A: Flask仓库有5000+提交，首次分析需要10-30分钟，可使用缓存加速。
