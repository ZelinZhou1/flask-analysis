"""
GitHub API 采集器
使用 GitHub API 采集仓库的 Issues, Pull Requests 和其他元数据
"""

import requests
import logging
import os
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class GitHubCollector:
    """
    负责从 GitHub API 收集数据的采集器
    """

    BASE_URL = "https://api.github.com"

    def __init__(self, owner: str, repo: str, token: Optional[str] = None):
        """
        初始化 GitHub 采集器

        Args:
            owner: 仓库拥有者 (如 'pallets')
            repo: 仓库名称 (如 'flask')
            token: GitHub Personal Access Token (可选，建议提供以提高限流阈值)
        """
        self.owner = owner
        self.repo = repo
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        """
        发送 API 请求的通用方法，处理分页
        """
        url = f"{self.BASE_URL}/repos/{self.owner}/{self.repo}/{endpoint}"
        results = []
        page = 1

        while True:
            current_params = params.copy() if params else {}
            current_params["page"] = page
            current_params["per_page"] = 100  # 最大每页数量

            try:
                logger.debug(f"Requesting {url} page {page}")
                response = requests.get(
                    url, headers=self.headers, params=current_params
                )

                if response.status_code == 403:
                    logger.warning("GitHub API rate limit exceeded or forbidden")
                    break

                response.raise_for_status()
                data = response.json()

                if not data:
                    break

                if isinstance(data, list):
                    results.extend(data)
                    if len(data) < 100:  # 如果当前页不满，说明是最后一页
                        break
                else:
                    return data  # 非列表响应直接返回

                page += 1

            except requests.exceptions.RequestException as e:
                logger.error(f"GitHub API 请求失败: {str(e)}")
                break

        return results

    def collect_issues(self, state: str = "all") -> List[Dict[str, Any]]:
        """
        采集 Issues (包含 PR，因为 GitHub 将 PR 视为一种特殊的 Issue)

        Args:
            state: 状态 'open', 'closed', 'all'
        """
        logger.info(f"开始采集 Issues ({state})...")
        issues = self._make_request("issues", {"state": state})

        # 简单过滤，区分 Issue 和 PR
        processed_issues = []
        for item in issues:
            is_pr = "pull_request" in item
            processed_issues.append(
                {
                    "number": item["number"],
                    "title": item["title"],
                    "state": item["state"],
                    "created_at": item["created_at"],
                    "closed_at": item["closed_at"],
                    "author": item["user"]["login"],
                    "labels": [l["name"] for l in item["labels"]],
                    "comments_count": item["comments"],
                    "is_pr": is_pr,
                    "body_length": len(item.get("body") or ""),
                }
            )

        logger.info(f"采集到 {len(processed_issues)} 个 Issues/PRs")
        return processed_issues

    def collect_contributors(self) -> List[Dict[str, Any]]:
        """
        采集贡献者列表
        """
        logger.info("开始采集贡献者...")
        contributors = self._make_request("contributors")

        data = []
        if isinstance(contributors, list):
            for c in contributors:
                data.append(
                    {
                        "login": c["login"],
                        "contributions": c["contributions"],
                        "type": c["type"],
                        "site_admin": c["site_admin"],
                    }
                )

        return data

    def collect_repo_info(self) -> Dict[str, Any]:
        """
        采集仓库基本信息 (Stars, Forks, etc.)
        """
        url = f"{self.BASE_URL}/repos/{self.owner}/{self.repo}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return {
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "watchers": data.get("subscribers_count", 0),
                "open_issues": data.get("open_issues_count", 0),
                "created_at": data.get("created_at"),
                "updated_at": data.get("updated_at"),
                "language": data.get("language"),
                "size": data.get("size"),
            }
        except Exception as e:
            logger.error(f"获取仓库信息失败: {str(e)}")
            return {}
