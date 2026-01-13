# -*- coding: utf-8 -*-
"""
日期处理工具模块
提供日期解析、格式化和提取等功能，用于时间维度的数据分析
"""

from datetime import datetime, timezone
from typing import Optional, Union

# 星期名称映射（中文）
WEEKDAY_NAMES_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

# 星期名称映射（英文）
WEEKDAY_NAMES_EN = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# 月份名称映射（中文）
MONTH_NAMES_CN = [
    "一月",
    "二月",
    "三月",
    "四月",
    "五月",
    "六月",
    "七月",
    "八月",
    "九月",
    "十月",
    "十一月",
    "十二月",
]


def parse_date(date_input: Union[str, datetime, None]) -> Optional[datetime]:
    """
    解析日期字符串为datetime对象

    Args:
        date_input: 日期字符串、datetime对象或None

    Returns:
        datetime对象，解析失败返回None
    """
    if date_input is None:
        return None

    if isinstance(date_input, datetime):
        return date_input

    # 尝试多种常见日期格式
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_input, fmt)
        except ValueError:
            continue

    return None


def get_year_month(date_input: Union[str, datetime]) -> Optional[str]:
    """
    获取年月字符串，格式为 YYYY-MM

    Args:
        date_input: 日期输入

    Returns:
        年月字符串，如 '2024-01'
    """
    dt = parse_date(date_input)
    if dt is None:
        return None
    return dt.strftime("%Y-%m")


def get_year(date_input: Union[str, datetime]) -> Optional[int]:
    """
    提取年份

    Args:
        date_input: 日期输入

    Returns:
        年份整数
    """
    dt = parse_date(date_input)
    if dt is None:
        return None
    return dt.year


def get_month(date_input: Union[str, datetime]) -> Optional[int]:
    """
    提取月份（1-12）

    Args:
        date_input: 日期输入

    Returns:
        月份整数
    """
    dt = parse_date(date_input)
    if dt is None:
        return None
    return dt.month


def get_weekday(date_input: Union[str, datetime]) -> Optional[int]:
    """
    获取星期几（0=周一, 6=周日）

    Args:
        date_input: 日期输入

    Returns:
        星期索引
    """
    dt = parse_date(date_input)
    if dt is None:
        return None
    return dt.weekday()


def get_hour(date_input: Union[str, datetime]) -> Optional[int]:
    """
    提取小时（0-23）

    Args:
        date_input: 日期输入

    Returns:
        小时整数
    """
    dt = parse_date(date_input)
    if dt is None:
        return None
    return dt.hour


def get_weekday_name(
    date_input: Union[str, datetime], lang: str = "cn"
) -> Optional[str]:
    """
    获取星期名称

    Args:
        date_input: 日期输入
        lang: 语言，'cn'为中文，'en'为英文

    Returns:
        星期名称
    """
    weekday = get_weekday(date_input)
    if weekday is None:
        return None

    names = WEEKDAY_NAMES_CN if lang == "cn" else WEEKDAY_NAMES_EN
    return names[weekday]


def get_month_name(date_input: Union[str, datetime], lang: str = "cn") -> Optional[str]:
    """
    获取月份名称

    Args:
        date_input: 日期输入
        lang: 语言，'cn'为中文

    Returns:
        月份名称
    """
    month = get_month(date_input)
    if month is None:
        return None

    if lang == "cn":
        return MONTH_NAMES_CN[month - 1]
    return datetime(2000, month, 1).strftime("%B")


def format_date(
    date_input: Union[str, datetime], fmt: str = "%Y-%m-%d"
) -> Optional[str]:
    """
    格式化日期

    Args:
        date_input: 日期输入
        fmt: 输出格式

    Returns:
        格式化后的日期字符串
    """
    dt = parse_date(date_input)
    if dt is None:
        return None
    return dt.strftime(fmt)


def get_date_range_days(
    start: Union[str, datetime], end: Union[str, datetime]
) -> Optional[int]:
    """
    计算两个日期之间的天数差

    Args:
        start: 开始日期
        end: 结束日期

    Returns:
        天数差
    """
    start_dt = parse_date(start)
    end_dt = parse_date(end)

    if start_dt is None or end_dt is None:
        return None

    return (end_dt - start_dt).days


def is_weekend(date_input: Union[str, datetime]) -> Optional[bool]:
    """
    判断是否为周末

    Args:
        date_input: 日期输入

    Returns:
        是否为周末
    """
    weekday = get_weekday(date_input)
    if weekday is None:
        return None
    return weekday >= 5


def is_business_day(date_input: Union[str, datetime]) -> Optional[bool]:
    """
    判断是否为工作日

    Args:
        date_input: 日期输入

    Returns:
        是否为工作日
    """
    weekend = is_weekend(date_input)
    if weekend is None:
        return None
    return not weekend


def get_quarter(date_input: Union[str, datetime]) -> Optional[int]:
    """
    获取季度（1-4）

    Args:
        date_input: 日期输入

    Returns:
        季度
    """
    month = get_month(date_input)
    if month is None:
        return None
    return (month - 1) // 3 + 1


def now_utc() -> datetime:
    """
    获取当前UTC时间

    Returns:
        UTC datetime对象
    """
    return datetime.now(timezone.utc)


def now_local() -> datetime:
    """
    获取当前本地时间

    Returns:
        本地 datetime对象
    """
    return datetime.now()
