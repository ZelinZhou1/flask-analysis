"""
标签信息采集器
分析仓库的 Tag 发布历史和版本时间线
"""

from typing import List, Dict, Any
from pydriller.git import Git
import logging

logger = logging.getLogger(__name__)


class TagCollector:
    """
    负责收集 Git 标签(Release)信息的采集器
    """

    def __init__(self, repo_path: str):
        """
        初始化标签采集器

        Args:
            repo_path: 仓库本地路径
        """
        self.repo_path = repo_path
        self.git = Git(repo_path)

    def collect_tags(self) -> List[Dict[str, Any]]:
        """
        采集所有标签信息，按时间排序

        Returns:
            标签信息列表
        """
        logger.info("开始采集标签信息...")
        tags_data = []

        try:
            repo = self.git.repo

            # 遍历所有标签
            for tag in repo.tags:
                # 获取标签对应的 commit 对象
                # tag.commit 指向 tag object 或 commit object
                commit = tag.commit

                tag_info = {
                    "name": tag.name,
                    "commit_hash": commit.hexsha,
                    "date": commit.committed_datetime,
                    "author": commit.author.name,
                    "message": getattr(tag.object, "message", None)
                    or commit.message.strip(),
                    "path": tag.path,
                }
                tags_data.append(tag_info)

            # 按日期排序
            tags_data.sort(key=lambda x: x["date"])

            # 计算版本间隔天数
            for i in range(1, len(tags_data)):
                prev = tags_data[i - 1]["date"]
                curr = tags_data[i]["date"]
                days_diff = (curr - prev).days
                tags_data[i]["days_since_last_release"] = days_diff

            logger.info(f"采集到 {len(tags_data)} 个标签")

        except Exception as e:
            logger.error(f"采集标签信息失败: {str(e)}")

        return tags_data

    def get_latest_tag(self) -> Dict[str, Any]:
        """
        获取最新的标签信息
        """
        tags = self.collect_tags()
        if tags:
            return tags[-1]
        return None
