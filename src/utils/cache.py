# -*- coding: utf-8 -*-
"""
缓存管理模块
提供内存缓存和文件缓存功能，支持过期时间控制
"""

import hashlib
import pickle
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, Optional, Union, Callable, Dict
from functools import wraps


class CacheManager:
    """
    缓存管理器
    支持内存缓存和文件持久化缓存，可设置过期时间
    """

    def __init__(
        self, cache_dir: Optional[Union[str, Path]] = None, default_ttl: int = 3600
    ):
        """
        初始化缓存管理器

        Args:
            cache_dir: 文件缓存目录，None则只使用内存缓存
            default_ttl: 默认过期时间（秒），默认1小时
        """
        self._memory_cache: Dict[str, Any] = {}
        self._cache_times: Dict[str, datetime] = {}
        self._default_ttl = default_ttl

        self._cache_dir: Optional[Path] = None
        if cache_dir is not None:
            self._cache_dir = Path(cache_dir)
            self._cache_dir.mkdir(parents=True, exist_ok=True)

    def _is_expired(self, key: str, ttl: Optional[int] = None) -> bool:
        """检查缓存项是否过期"""
        if key not in self._cache_times:
            return True

        cache_time = self._cache_times[key]
        effective_ttl = ttl if ttl is not None else self._default_ttl

        if effective_ttl <= 0:
            return False

        return datetime.now() > cache_time + timedelta(seconds=effective_ttl)

    def _get_file_path(self, key: str) -> Path:
        """获取缓存文件路径（调用前需确保_cache_dir不为None）"""
        assert self._cache_dir is not None
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self._cache_dir / f"{key_hash}.cache"

    def get(self, key: str, default: Any = None, ttl: Optional[int] = None) -> Any:
        """
        获取缓存值

        Args:
            key: 缓存键
            default: 默认值
            ttl: 过期时间（秒），None使用默认值

        Returns:
            缓存值或默认值
        """
        if key in self._memory_cache:
            if not self._is_expired(key, ttl):
                return self._memory_cache[key]
            else:
                del self._memory_cache[key]
                del self._cache_times[key]

        if self._cache_dir is not None:
            file_path = self._get_file_path(key)
            if file_path.exists():
                try:
                    with open(file_path, "rb") as f:
                        data = pickle.load(f)

                    cache_time = data.get("time")
                    value = data.get("value")

                    if cache_time is not None:
                        self._cache_times[key] = cache_time
                        if not self._is_expired(key, ttl):
                            self._memory_cache[key] = value
                            return value

                    file_path.unlink()

                except Exception:
                    pass

        return default

    def set(
        self, key: str, value: Any, ttl: Optional[int] = None, persist: bool = True
    ) -> None:
        """
        设置缓存值

        Args:
            key: 缓存键
            value: 缓存值
            ttl: 过期时间（秒），None使用默认值
            persist: 是否持久化到文件
        """
        now = datetime.now()
        self._memory_cache[key] = value
        self._cache_times[key] = now

        if persist and self._cache_dir is not None:
            file_path = self._get_file_path(key)
            try:
                with open(file_path, "wb") as f:
                    pickle.dump(
                        {
                            "time": now,
                            "value": value,
                            "ttl": ttl if ttl is not None else self._default_ttl,
                        },
                        f,
                    )
            except Exception:
                pass

    def delete(self, key: str) -> bool:
        """
        删除缓存项

        Args:
            key: 缓存键

        Returns:
            是否成功删除
        """
        deleted = False

        if key in self._memory_cache:
            del self._memory_cache[key]
            del self._cache_times[key]
            deleted = True

        if self._cache_dir is not None:
            file_path = self._get_file_path(key)
            if file_path.exists():
                file_path.unlink()
                deleted = True

        return deleted

    def clear(self) -> None:
        """清空所有缓存"""
        self._memory_cache.clear()
        self._cache_times.clear()

        if self._cache_dir is not None:
            for file_path in self._cache_dir.glob("*.cache"):
                try:
                    file_path.unlink()
                except Exception:
                    pass

    def has(self, key: str, ttl: Optional[int] = None) -> bool:
        """
        检查是否存在有效的缓存

        Args:
            key: 缓存键
            ttl: 过期时间

        Returns:
            是否存在
        """
        return self.get(key, default=None, ttl=ttl) is not None

    def get_or_set(
        self, key: str, factory: Callable[[], Any], ttl: Optional[int] = None
    ) -> Any:
        """
        获取缓存，如不存在则通过factory创建并缓存

        Args:
            key: 缓存键
            factory: 值工厂函数
            ttl: 过期时间

        Returns:
            缓存值
        """
        value = self.get(key, default=None, ttl=ttl)
        if value is None:
            value = factory()
            self.set(key, value, ttl=ttl)
        return value

    def stats(self) -> dict:
        """
        获取缓存统计信息

        Returns:
            统计信息字典
        """
        file_count = 0
        if self._cache_dir is not None:
            file_count = len(list(self._cache_dir.glob("*.cache")))

        return {
            "memory_items": len(self._memory_cache),
            "file_items": file_count,
            "cache_dir": str(self._cache_dir) if self._cache_dir else None,
            "default_ttl": self._default_ttl,
        }


def cached(
    cache_manager: CacheManager, key_prefix: str = "", ttl: Optional[int] = None
) -> Callable:
    """
    缓存装饰器

    Args:
        cache_manager: 缓存管理器实例
        key_prefix: 缓存键前缀
        ttl: 过期时间

    Returns:
        装饰器函数
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key_parts = [key_prefix, func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = ":".join(key_parts)

            result = cache_manager.get(cache_key, ttl=ttl)
            if result is not None:
                return result

            result = func(*args, **kwargs)
            if result is not None:
                cache_manager.set(cache_key, result, ttl=ttl)

            return result

        return wrapper

    return decorator
