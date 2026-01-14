# src/analyzers/pr_analyzer.py
from typing import List, Dict, Any
from datetime import datetime, timedelta
import statistics


class PRAnalyzer:
    """
    Pull Request 分析器
    分析PR的生命周期、审查情况和合并趋势
    """

    def __init__(self, pr_data: List[Dict[str, Any]]):
        """
        初始化PR分析器

        Args:
            pr_data: PR数据列表，每个元素包含PR的详细信息
        """
        self.pr_data = pr_data

    def analyze_lifecycle(self) -> Dict[str, Any]:
        """
        分析PR生命周期（开启到合并/关闭的时间）

        Returns:
            包含平均耗时、中位数耗时等统计信息
        """
        durations = []
        for pr in self.pr_data:
            if pr.get("state") == "closed" or pr.get("merged_at"):
                created_at = self._parse_date(pr.get("created_at"))
                closed_at = self._parse_date(pr.get("closed_at") or pr.get("merged_at"))

                if created_at and closed_at:
                    duration = (closed_at - created_at).total_seconds() / 3600  # 小时
                    durations.append(duration)

        if not durations:
            return {"average_hours": 0, "median_hours": 0}

        return {
            "average_hours": statistics.mean(durations),
            "median_hours": statistics.median(durations),
            "max_hours": max(durations),
            "min_hours": min(durations),
            "count": len(durations),
        }

    def analyze_size(self) -> Dict[str, Any]:
        """
        分析PR大小（变更行数）

        Returns:
            关于PR大小的统计分布
        """
        additions = [pr.get("additions", 0) for pr in self.pr_data]
        deletions = [pr.get("deletions", 0) for pr in self.pr_data]
        changes = [a + d for a, d in zip(additions, deletions)]

        if not changes:
            return {}

        return {
            "avg_additions": statistics.mean(additions),
            "avg_deletions": statistics.mean(deletions),
            "avg_changes": statistics.mean(changes),
            "large_prs": len([c for c in changes if c > 500]),  # 假设 >500 行为大PR
            "small_prs": len([c for c in changes if c < 50]),  # 假设 <50 行为小PR
        }

    def analyze_review_engagement(self) -> Dict[str, Any]:
        """
        分析审查参与度

        Returns:
            评论数和审查者数量的统计
        """
        comments = [pr.get("comments", 0) for pr in self.pr_data]
        reviewers = [len(pr.get("requested_reviewers", [])) for pr in self.pr_data]

        if not comments:
            return {}

        return {
            "avg_comments": statistics.mean(comments),
            "max_comments": max(comments),
            "avg_reviewers": statistics.mean(reviewers),
            "unreviewed_prs": len([r for r in reviewers if r == 0]),
        }

    def _parse_date(self, date_str: str) -> datetime:
        """解析ISO格式日期字符串"""
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except ValueError:
            return None
