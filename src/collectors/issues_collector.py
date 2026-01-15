# -*- coding: utf-8 -*-
"""
Issues数据采集模块
从GitHub API获取仓库的所有Issues数据
支持断点续传
"""

import requests
import time
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

PROGRESS_FILE = "data/.fetch_progress.json"


def load_progress() -> Dict:
    """加载采集进度"""
    try:
        if Path(PROGRESS_FILE).exists():
            with open(PROGRESS_FILE, "r") as f:
                return json.load(f)
    except:
        pass
    return {}


def save_progress(progress: Dict):
    """保存采集进度"""
    Path(PROGRESS_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)


class IssuesCollector:
    """
    GitHub Issues采集器
    支持断点续传
    """
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, repo: str, token: Optional[str] = None):
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
                reset_time = int(resp.headers.get("X-RateLimit-Reset", 0))
                wait_time = max(reset_time - int(time.time()), 60)
                wait_time = min(wait_time, 300)
                logger.warning(f"API速率限制，等待{wait_time}秒...")
                time.sleep(wait_time)
                return self._request(endpoint, params)
            
            resp.raise_for_status()
            return resp.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API请求失败: {e}")
            return None
    
    def collect_issues(self, state: str = "all", max_pages: int = 50, resume: bool = True) -> List[Dict]:
        """
        采集Issues（支持断点续传）
        """
        progress = load_progress() if resume else {}
        start_page = progress.get("issues_page", 1)
        all_issues = []
        
        if resume and Path("data/issues_partial.json").exists():
            try:
                with open("data/issues_partial.json", "r", encoding="utf-8") as f:
                    all_issues = json.load(f)
                logger.info(f"从断点恢复，已有{len(all_issues)}个Issues，从第{start_page}页继续")
            except:
                pass
        
        page = start_page
        
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
            
            issues_only = [i for i in data if "pull_request" not in i]
            all_issues.extend(issues_only)
            
            progress["issues_page"] = page + 1
            save_progress(progress)
            
            if page % 10 == 0:
                self.save_to_json(all_issues, "data/issues_partial.json")
            
            if len(data) < 100:
                break
            page += 1
        
        if Path("data/issues_partial.json").exists():
            Path("data/issues_partial.json").unlink()
        progress.pop("issues_page", None)
        save_progress(progress)
        
        logger.info(f"共采集{len(all_issues)}个Issues")
        return all_issues
    
    def collect_prs(self, state: str = "all", max_pages: int = 50, resume: bool = True) -> List[Dict]:
        """
        采集Pull Requests（支持断点续传）
        """
        progress = load_progress() if resume else {}
        start_page = progress.get("prs_page", 1)
        all_prs = []
        
        if resume and Path("data/prs_partial.json").exists():
            try:
                with open("data/prs_partial.json", "r", encoding="utf-8") as f:
                    all_prs = json.load(f)
                logger.info(f"从断点恢复，已有{len(all_prs)}个PRs，从第{start_page}页继续")
            except:
                pass
        
        page = start_page
        
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
            
            progress["prs_page"] = page + 1
            save_progress(progress)
            
            if page % 10 == 0:
                self.save_to_json(all_prs, "data/prs_partial.json")
            
            if len(data) < 100:
                break
            page += 1
        
        if Path("data/prs_partial.json").exists():
            Path("data/prs_partial.json").unlink()
        progress.pop("prs_page", None)
        save_progress(progress)
        
        logger.info(f"共采集{len(all_prs)}个PRs")
        return all_prs
    
    def collect_contributors(self, max_pages: int = 20) -> List[Dict]:
        """采集贡献者"""
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
