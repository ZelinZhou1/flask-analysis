"""
分支信息采集器
分析仓库的分支结构、活跃度和最后提交状态
"""

from typing import List, Dict, Any
from pydriller.git import Git
import logging

logger = logging.getLogger(__name__)


class BranchCollector:
    """
    负责收集 Git 分支信息的采集器
    """

    def __init__(self, repo_path: str):
        """
        初始化分支采集器

        Args:
            repo_path: 仓库本地路径
        """
        self.repo_path = repo_path
        self.git = Git(repo_path)

    def collect_branches(self) -> List[Dict[str, Any]]:
        """
        采集所有本地分支信息

        Returns:
            包含分支详情的列表
        """
        logger.info("开始采集分支信息...")
        branches_data = []

        try:
            # 获取 repo 对象 (pydriller.git.Git 封装了 gitpython 的 Repo)
            # 注意: PyDriller 的 Git 类主要用于获取 commit，直接操作分支可能需要访问底层的 gitpython Repo 对象
            # self.git.repo 是 git.Repo 对象

            repo = self.git.repo

            for head in repo.heads:
                last_commit = head.commit
                branch_info = {
                    "name": head.name,
                    "is_active": head == repo.active_branch,
                    "last_commit_hash": last_commit.hexsha,
                    "last_commit_date": last_commit.committed_datetime,
                    "last_commit_author": last_commit.author.name,
                    "last_commit_msg": last_commit.message.strip(),
                    # 尝试计算该分支相对于主分支的领先/落后提交数（如果需要更复杂分析可扩展）
                }
                branches_data.append(branch_info)

            logger.info(f"采集到 {len(branches_data)} 个分支")

        except Exception as e:
            logger.error(f"采集分支信息失败: {str(e)}")
            # 降级策略或抛出异常

        return branches_data

    def get_merged_branches(self, target_branch: str = "main") -> List[str]:
        """
        获取已合并到目标分支的分支列表

        Args:
            target_branch: 目标分支名称

        Returns:
            已合并分支名称列表
        """
        merged = []
        try:
            repo = self.git.repo
            if target_branch in repo.heads:
                target = repo.heads[target_branch]
                for head in repo.heads:
                    if head != target and repo.is_ancestor(head.commit, target.commit):
                        merged.append(head.name)
        except Exception as e:
            logger.error(f"检查合并分支失败: {str(e)}")

        return merged
