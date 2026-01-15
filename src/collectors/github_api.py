# -*- coding: utf-8 -*-
"""
GitHub API访问模块
用于获取Issues、PRs和贡献者数据
"""
import requests
import time
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class GitHubAPI:
    """
    GitHub REST API封装类
    支持获取Issues、PRs、贡献者等数据
    """
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, repo: str, token: Optional[str] = None):
        """
        初始化GitHub API客户端
        
        Args:
            repo: 仓库名称，格式为 "owner/repo"
            token: GitHub Personal Access Token（可选，用于提高速率限制）
        """
        self.repo = repo
        self.token = token
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Flask-Repo-Analyzer"
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
    
    def _request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """
        发送API请求
        
        Args:
            endpoint: API端点
            params: 查询参数
            
        Returns:
            JSON响应数据
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            resp = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            # 检查速率限制
            if resp.status_code == 403:
                reset_time = int(resp.headers.get("X-RateLimit-Reset", 0))
                wait_time = max(reset_time - int(time.time()), 60)
                logger.warning(f"API速率限制，等待{wait_time}秒...")
                time.sleep(min(wait_time, 300))
                return self._request(endpoint, params)
            
            resp.raise_for_status()
            return resp.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API请求失败: {e}")
            return None
    
    def get_issues(self, state: str = "all", max_pages: int = 10) -> List[Dict]:
        """
        获取Issues列表
        
        Args:
            state: 状态过滤 ("open", "closed", "all")
            max_pages: 最大页数
            
        Returns:
            Issues列表
        """
        all_issues = []
        page = 1
        
        while page <= max_pages:
            logger.info(f"获取Issues第{page}页...")
            
            data = self._request(
                f"/repos/{self.repo}/issues",
                params={"state": state, "per_page": 100, "page": page}
            )
            
            if not data:
                break
            
            # 过滤掉PRs（Issues API会包含PRs）
            issues = [i for i in data if "pull_request" not in i]
            all_issues.extend(issues)
            
            if len(data) < 100:
                break
            page += 1
        
        logger.info(f"共获取{len(all_issues)}个Issues")
        return all_issues
    
    def get_pull_requests(self, state: str = "all", max_pages: int = 10) -> List[Dict]:
        """
        获取Pull Requests列表
        
        Args:
            state: 状态过滤 ("open", "closed", "all")
            max_pages: 最大页数
            
        Returns:
            PRs列表
        """
        all_prs = []
        page = 1
        
        while page <= max_pages:
            logger.info(f"获取PRs第{page}页...")
            
            data = self._request(
                f"/repos/{self.repo}/pulls",
                params={"state": state, "per_page": 100, "page": page}
            )
            
            if not data:
                break
            
            all_prs.extend(data)
            
            if len(data) < 100:
                break
            page += 1
        
        logger.info(f"共获取{len(all_prs)}个PRs")
        return all_prs
    
    def get_contributors(self, max_pages: int = 5) -> List[Dict]:
        """
        获取贡献者列表
        
        Args:
            max_pages: 最大页数
            
        Returns:
            贡献者列表
        """
        all_contributors = []
        page = 1
        
        while page <= max_pages:
            logger.info(f"获取贡献者第{page}页...")
            
            data = self._request(
                f"/repos/{self.repo}/contributors",
                params={"per_page": 100, "page": page}
            )
            
            if not data:
                break
            
            all_contributors.extend(data)
            
            if len(data) < 100:
                break
            page += 1
        
        logger.info(f"共获取{len(all_contributors)}个贡献者")
        return all_contributors
    
    def get_repo_info(self) -> Optional[Dict]:
        """
        获取仓库信息
        
        Returns:
            仓库信息字典
        """
        return self._request(f"/repos/{self.repo}")
    
    def save_data(self, data: Any, filename: str, data_dir: str = "data"):
        """
        保存数据到JSON文件
        
        Args:
            data: 要保存的数据
            filename: 文件名
            data_dir: 数据目录
        """
        path = Path(data_dir) / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"数据已保存到: {path}")
