# -*- coding: utf-8 -*-
"""
Issues数据采集模块
从GitHub API获取仓库的所有Issues数据
"""

import requests
import time
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class IssuesCollector:
    """
    GitHub Issues采集器
    """
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, repo: str, token: Optional[str] = None):
        """
        初始化Issues采集器
        
        Args:
            repo: 仓库名称，格式为 "owner/repo"
            token: GitHub Personal Access Token
        """
        self.repo = repo
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Flask-Repo-Analyzer"
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
    
    def _request(self, endpoint: str, params: Dict = None) -> Optional[List]:
        """发送API请求"""
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            resp = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if resp.status_code == 403:
                logger.warning("API速率限制，等待60秒...")
                time.sleep(60)
                return self._request(endpoint, params)
            
            resp.raise_for_status()
            return resp.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API请求失败: {e}")
            return None
    
    def collect_issues(self, state: str = "all", max_pages: int = 20) -> List[Dict]:
        """
        采集Issues
        
        Args:
            state: 状态筛选 ("open", "closed", "all")
            max_pages: 最大页数
            
        Returns:
            Issues列表
        """
        all_issues = []
        page = 1
        
        while page <= max_pages:
            logger.info(f"采集Issues第{page}页...")
            
            data = self._request(
                f"/repos/{self.repo}/issues",
                params={
                    "state": state,
                    "per_page": 100,
                    "page": page,
                    "sort": "created",
                    "direction": "desc"
                }
            )
            
            if not data:
                break
            
            # 过滤掉PRs（Issues API会包含PRs）
            issues_only = [i for i in data if "pull_request" not in i]
            all_issues.extend(issues_only)
            
            if len(data) < 100:
                break
            page += 1
        
        logger.info(f"共采集{len(all_issues)}个Issues")
        return all_issues
    
    def collect_prs(self, state: str = "all", max_pages: int = 20) -> List[Dict]:
        """
        采集Pull Requests
        
        Args:
            state: 状态筛选 ("open", "closed", "all")
            max_pages: 最大页数
            
        Returns:
            PRs列表
        """
        all_prs = []
        page = 1
        
        while page <= max_pages:
            logger.info(f"采集PRs第{page}页...")
            
            data = self._request(
                f"/repos/{self.repo}/pulls",
                params={
                    "state": state,
                    "per_page": 100,
                    "page": page
                }
            )
            
            if not data:
                break
            
            all_prs.extend(data)
            
            if len(data) < 100:
                break
            page += 1
        
        logger.info(f"共采集{len(all_prs)}个PRs")
        return all_prs
    
    def collect_contributors(self, max_pages: int = 10) -> List[Dict]:
        """
        采集贡献者
        
        Returns:
            贡献者列表
        """
        all_contributors = []
        page = 1
        
        while page <= max_pages:
            logger.info(f"采集贡献者第{page}页...")
            
            data = self._request(
                f"/repos/{self.repo}/contributors",
                params={
                    "per_page": 100,
                    "page": page
                }
            )
            
            if not data:
                break
            
            all_contributors.extend(data)
            
            if len(data) < 100:
                break
            page += 1
        
        logger.info(f"共采集{len(all_contributors)}个贡献者")
        return all_contributors
    
    def save_to_json(self, data: Any, filepath: str):
        """保存数据到JSON文件"""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        
        logger.info(f"已保存到: {filepath}")
