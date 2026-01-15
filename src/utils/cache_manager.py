# -*- coding: utf-8 -*-
"""
缓存管理模块
提供基于文件系统的缓存功能，用于加速重复分析
"""
import json
import os
import time
from pathlib import Path
from typing import Any, Optional
import hashlib


class CacheManager:
    """
    文件缓存管理器
    支持TTL过期、键值存储
    """
    
    def __init__(self, cache_dir: str = "cache"):
        """
        初始化缓存管理器
        
        Args:
            cache_dir: 缓存目录路径
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.meta_file = self.cache_dir / "_meta.json"
        self._load_meta()
    
    def _load_meta(self):
        """加载缓存元数据"""
        if self.meta_file.exists():
            try:
                with open(self.meta_file, "r", encoding="utf-8") as f:
                    self.meta = json.load(f)
            except:
                self.meta = {}
        else:
            self.meta = {}
    
    def _save_meta(self):
        """保存缓存元数据"""
        with open(self.meta_file, "w", encoding="utf-8") as f:
            json.dump(self.meta, f, indent=2)
    
    def _get_cache_path(self, key: str) -> Path:
        """获取缓存文件路径"""
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.json"
    
    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存值
        
        Args:
            key: 缓存键
            
        Returns:
            缓存值，如果不存在或过期返回None
        """
        if key not in self.meta:
            return None
        
        meta = self.meta[key]
        if meta.get("expires_at") and time.time() > meta["expires_at"]:
            self.delete(key)
            return None
        
        cache_path = self._get_cache_path(key)
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """
        设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 过期时间（秒），默认1小时
        """
        cache_path = self._get_cache_path(key)
        
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(value, f, ensure_ascii=False, indent=2, default=str)
        
        self.meta[key] = {
            "created_at": time.time(),
            "expires_at": time.time() + ttl if ttl > 0 else None,
            "path": str(cache_path)
        }
        self._save_meta()
    
    def delete(self, key: str):
        """删除缓存"""
        if key in self.meta:
            cache_path = self._get_cache_path(key)
            if cache_path.exists():
                cache_path.unlink()
            del self.meta[key]
            self._save_meta()
    
    def clear(self):
        """清空所有缓存"""
        for key in list(self.meta.keys()):
            self.delete(key)
    
    def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        return self.get(key) is not None
