# -*- coding: utf-8 -*-
"""
日期时间工具模块
提供日期解析、格式化和范围计算功能
"""
from datetime import datetime, timedelta
from typing import Optional, List, Tuple
import pandas as pd


def parse_date(date_str: str) -> Optional[datetime]:
    """
    解析日期字符串
    
    Args:
        date_str: 日期字符串
        
    Returns:
        datetime对象
    """
    formats = [
        "%Y-%m-%d %H:%M:%S%z",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d",
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(str(date_str).split("+")[0].split("Z")[0], fmt.replace("%z", ""))
        except ValueError:
            continue
    
    # 尝试pandas解析
    try:
        return pd.to_datetime(date_str).to_pydatetime()
    except:
        return None


def get_date_range(start: datetime, end: datetime) -> List[datetime]:
    """
    获取日期范围内的所有日期
    
    Args:
        start: 开始日期
        end: 结束日期
        
    Returns:
        日期列表
    """
    dates = []
    current = start
    while current <= end:
        dates.append(current)
        current += timedelta(days=1)
    return dates


def get_week_boundaries(date: datetime) -> Tuple[datetime, datetime]:
    """
    获取给定日期所在周的起止日期
    
    Args:
        date: 日期
        
    Returns:
        (周一, 周日)
    """
    monday = date - timedelta(days=date.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday


def get_month_boundaries(date: datetime) -> Tuple[datetime, datetime]:
    """
    获取给定日期所在月的起止日期
    
    Args:
        date: 日期
        
    Returns:
        (月初, 月末)
    """
    first_day = date.replace(day=1)
    if date.month == 12:
        last_day = date.replace(month=12, day=31)
    else:
        last_day = date.replace(month=date.month + 1, day=1) - timedelta(days=1)
    return first_day, last_day


def format_date(date: datetime, fmt: str = "%Y-%m-%d") -> str:
    """
    格式化日期
    
    Args:
        date: datetime对象
        fmt: 格式字符串
        
    Returns:
        格式化后的字符串
    """
    return date.strftime(fmt)


def get_year_month(date: datetime) -> str:
    """获取年月字符串 (YYYY-MM)"""
    return date.strftime("%Y-%m")


def get_weekday_name(date: datetime) -> str:
    """获取星期名称"""
    return date.strftime("%A")


def days_between(date1: datetime, date2: datetime) -> int:
    """计算两个日期之间的天数"""
    return abs((date2 - date1).days)


def is_weekend(date: datetime) -> bool:
    """判断是否为周末"""
    return date.weekday() >= 5


def group_by_period(dates: List[datetime], period: str = "month") -> dict:
    """
    按时间段分组
    
    Args:
        dates: 日期列表
        period: 分组周期 ("day", "week", "month", "year")
        
    Returns:
        分组字典 {period_key: count}
    """
    groups = {}
    
    for date in dates:
        if period == "day":
            key = format_date(date)
        elif period == "week":
            monday, _ = get_week_boundaries(date)
            key = format_date(monday)
        elif period == "month":
            key = get_year_month(date)
        elif period == "year":
            key = str(date.year)
        else:
            key = format_date(date)
        
        groups[key] = groups.get(key, 0) + 1
    
    return groups
