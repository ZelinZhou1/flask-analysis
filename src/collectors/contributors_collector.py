"""
贡献者数据采集器
负责统计和分析仓库贡献者数据，生成贡献者画像。
"""

from typing import Dict, List, Any, Optional
from collections import defaultdict
from pydriller import Repository
from datetime import datetime
import logging

# 配置日志
logger = logging.getLogger(__name__)


class ContributorsCollector:
    """
    贡献者数据采集器类
    """

    def __init__(self, repo_path: str):
        """
        初始化采集器

        Args:
            repo_path: 仓库本地路径
        """
        self.repo_path = repo_path
        self.contributors = defaultdict(
            lambda: {
                "name": "",
                "email": "",
                "commits": 0,
                "lines_added": 0,
                "lines_deleted": 0,
                "files_modified": 0,
                "first_commit": None,
                "last_commit": None,
                "active_days": set(),
            }
        )

    def collect(self, branch: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        采集贡献者数据

        Args:
            branch: 分支名称 (可选)

        Returns:
            贡献者统计列表，按提交数降序排列
        """
        logger.info(f"开始采集贡献者数据: {self.repo_path}")

        try:
            repo_kwargs = {"path_to_repo": self.repo_path}
            if branch:
                repo_kwargs["only_in_branch"] = branch

            for commit in Repository(**repo_kwargs).traverse_commits():
                email = commit.author.email
                name = commit.author.name
                date = commit.author_date

                # 使用邮箱作为唯一标识，如果需要合并同一人的多个邮箱，需在后续处理
                # 这里简单更新姓名以最新提交为准
                self.contributors[email]["name"] = name
                self.contributors[email]["email"] = email
                self.contributors[email]["commits"] += 1
                self.contributors[email]["lines_added"] += commit.insertions
                self.contributors[email]["lines_deleted"] += commit.deletions
                self.contributors[email]["files_modified"] += len(commit.modified_files)
                self.contributors[email]["active_days"].add(date.date())

                # 更新时间范围
                if (
                    not self.contributors[email]["first_commit"]
                    or date < self.contributors[email]["first_commit"]
                ):
                    self.contributors[email]["first_commit"] = date

                if (
                    not self.contributors[email]["last_commit"]
                    or date > self.contributors[email]["last_commit"]
                ):
                    self.contributors[email]["last_commit"] = date

            # 转换为列表并排序
            result = []
            for email, data in self.contributors.items():
                # 计算活跃天数
                data["active_days_count"] = len(data["active_days"])
                # 移除集合对象以便序列化
                del data["active_days"]

                # 格式化日期
                if data["first_commit"]:
                    data["first_commit"] = data["first_commit"].isoformat()
                if data["last_commit"]:
                    data["last_commit"] = data["last_commit"].isoformat()

                result.append(data)

            # 按提交数排序
            result.sort(key=lambda x: x["commits"], reverse=True)

            logger.info(f"贡献者采集完成，共发现 {len(result)} 位贡献者")
            return result

        except Exception as e:
            logger.error(f"采集贡献者数据失败: {str(e)}")
            return []
