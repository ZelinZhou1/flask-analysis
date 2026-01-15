# Flask仓库分析工具

分析Flask开源项目的提交历史、代码结构和贡献者活动。

## 功能

- Git提交历史分析（使用PyDriller）
- 代码复杂度分析（AST、LibCST、Radon）
- GitHub Issues/PRs/贡献者数据采集
- 20+张可视化图表（暖色系、支持中文）

## 技术栈

- 静态分析：ast、libcst、radon
- 动态追踪：pysnooper
- 符号执行：z3-solver
- Git分析：pydriller
- 可视化：matplotlib、seaborn、wordcloud

## 使用方法

```bash
# 安装依赖
pip install -r requirements.txt

# 运行分析
python main.py

# 采集GitHub数据
python main.py --fetch

# 查看帮助
python main.py --help
```

## 输出

- `data/` - 采集的数据（JSON格式）
- `output/` - 生成的图表（PNG格式）

## 团队成员

| 姓名 | GitHub |
|------|--------|
| 周泽林 | ZelinZhou1 |
| 王冠 | DUT-Abstracter |
| 刘建琪 | liujianqi258 |
| 李飞飞 | lff20041215 |
| 张天宇 | sasageiyou |

## 许可证

MIT License
