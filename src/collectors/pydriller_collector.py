"""
PyDriller 采集器
使用 PyDriller 库分析 Git 仓库历史
"""

from typing import List, Dict, Any, Generator, Optional
from pydriller import Repository
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)


class PyDrillerCollector:
    """
    负责收集 Git 提交历史信息的采集器
    """

    def __init__(self, repo_path: str, branch: Optional[str] = None):
        """
        初始化采集器

        Args:
            repo_path: 仓库本地路径
            branch: 分支名称 (可选)
        """
        self.repo_path = repo_path
        self.branch = branch

    def collect_commits(self) -> Generator[Dict[str, Any], None, None]:
        """
        采集所有提交记录

        Yields:
            包含提交信息的字典
        """
        logger.info(f"开始分析仓库: {self.repo_path}")

        try:
            # 配置 Repository 对象，如果指定了分支则只分析该分支
            repo_kwargs = {"path_to_repo": self.repo_path}
            if self.branch:
                repo_kwargs["only_in_branch"] = self.branch

            # 遍历提交
            for commit in Repository(**repo_kwargs).traverse_commits():
                commit_data = {
                    "hash": commit.hash,
                    "msg": commit.msg,
                    "author_name": commit.author.name,
                    "author_email": commit.author.email,
                    "author_date": commit.author_date,
                    "committer_name": commit.committer.name,
                    "committer_email": commit.committer.email,
                    "committer_date": commit.committer_date,
                    "lines": commit.lines,
                    "insertions": commit.insertions,
                    "deletions": commit.deletions,
                    "files": len(commit.modified_files),
                    "dmm_unit_size": commit.dmm_unit_size,
                    "dmm_complexity": commit.dmm_complexity,
                    "dmm_interfacing": commit.dmm_interfacing,
                    "modified_files_list": [f.filename for f in commit.modified_files],
                }
                yield commit_data

        except Exception as e:
            logger.error(f"采集提交历史时出错: {str(e)}")
            raise

    def collect_commits_by_author(self, author_name: str) -> List[Dict[str, Any]]:
        """
        采集特定作者的所有提交

        Args:
            author_name: 作者名字（模糊匹配）

        Returns:
            提交列表
        """
        commits = []
        for commit in self.collect_commits():
            if author_name.lower() in commit["author_name"].lower():
                commits.append(commit)
        return commits

    def collect_file_history(self, file_path: str) -> List[Dict[str, Any]]:
        """
        采集特定文件的变更历史

        Args:
            file_path: 相对仓库根目录的文件路径

        Returns:
            文件变更历史列表
        """
        history = []
        try:
            for commit in Repository(
                self.repo_path, filepath=file_path
            ).traverse_commits():
                for mod in commit.modified_files:
                    if mod.new_path == file_path or mod.old_path == file_path:
                        history.append(
                            {
                                "hash": commit.hash,
                                "date": commit.committer_date,
                                "author": commit.author.name,
                                "msg": commit.msg,
                                "change_type": mod.change_type.name,
                                "added_lines": mod.added_lines,
                                "deleted_lines": mod.deleted_lines,
                            }
                        )
        except Exception as e:
            logger.error(f"分析文件历史出错 {file_path}: {str(e)}")

        return history
