"""
Issue 数据采集器
负责从 GitHub API 或其他源采集 Issue 和 Pull Request 数据。
"""

import requests
import logging
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

# 配置日志
logger = logging.getLogger(__name__)


class IssuesCollector:
    """
    Issue 采集器类
    用于获取仓库的 Issue 列表、状态、标签等信息
    """

    def __init__(self, owner: str, repo: str, token: Optional[str] = None):
        """
        初始化采集器

        Args:
            owner: 仓库拥有者 (如 'pallets')
            repo: 仓库名称 (如 'flask')
            token: GitHub Personal Access Token (可选，建议提供以提高 API 限制)
        """
        self.owner = owner
        self.repo = repo
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.session = requests.Session()

        if self.token:
            self.session.headers.update({"Authorization": f"token {self.token}"})
        self.session.headers.update({"Accept": "application/vnd.github.v3+json"})

    def collect_issues(
        self, state: str = "all", per_page: int = 100, max_pages: int = 10
    ) -> List[Dict[str, Any]]:
        """
        采集 Issue 数据 (包含 Pull Requests，GitHub API 将 PR 视为特殊的 Issue)

        Args:
            state: Issue 状态 ('open', 'closed', 'all')
            per_page: 每页数量
            max_pages: 最大抓取页数，防止请求过多

        Returns:
            Issue 数据列表
        """
        logger.info(f"开始采集 {self.owner}/{self.repo} 的 Issues (state={state})...")

        issues = []
        page = 1

        while page <= max_pages:
            try:
                url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues"
                params = {
                    "state": state,
                    "per_page": per_page,
                    "page": page,
                    "sort": "created",
                    "direction": "desc",
                }

                response = self.session.get(url, params=params, timeout=30)

                if response.status_code != 200:
                    logger.error(
                        f"请求 GitHub API 失败: {response.status_code} - {response.text}"
                    )
                    break

                data = response.json()
                if not data:
                    break

                for item in data:
                    # 简单的预处理
                    issue_data = self._process_issue(item)
                    issues.append(issue_data)

                logger.debug(f"已采集第 {page} 页，共 {len(data)} 条")
                page += 1

            except Exception as e:
                logger.error(f"采集 Issues 时发生异常: {str(e)}")
                break

        logger.info(f"Issue 采集完成，共获取 {len(issues)} 条数据")
        return issues

    def _process_issue(self, raw_issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理原始 Issue 数据，提取关键字段

        Args:
            raw_issue: GitHub API 返回的原始字典

        Returns:
            处理后的字典
        """
        return {
            "id": raw_issue.get("id"),
            "number": raw_issue.get("number"),
            "title": raw_issue.get("title"),
            "user": raw_issue.get("user", {}).get("login"),
            "state": raw_issue.get("state"),
            "created_at": raw_issue.get("created_at"),
            "closed_at": raw_issue.get("closed_at"),
            "updated_at": raw_issue.get("updated_at"),
            "labels": [label["name"] for label in raw_issue.get("labels", [])],
            "comments_count": raw_issue.get("comments", 0),
            "is_pr": "pull_request" in raw_issue,  # 判断是否为 PR
            "body_length": len(raw_issue.get("body") or ""),
        }

    def collect_issue_comments(self, issue_number: int) -> List[Dict[str, Any]]:
        """
        采集指定 Issue 的评论

        Args:
            issue_number: Issue 编号

        Returns:
            评论列表
        """
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues/{issue_number}/comments"
        comments = []

        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                for item in data:
                    comments.append(
                        {
                            "id": item.get("id"),
                            "user": item.get("user", {}).get("login"),
                            "created_at": item.get("created_at"),
                            "body_length": len(item.get("body") or ""),
                        }
                    )
        except Exception as e:
            logger.error(f"获取 Issue #{issue_number} 评论失败: {str(e)}")

        return comments
