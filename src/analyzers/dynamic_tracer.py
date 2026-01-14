import pysnooper
import logging
from typing import Callable, Any, Dict, List
import functools

# 配置日志记录器
logger = logging.getLogger(__name__)


class DynamicTracer:
    """
    动态追踪分析器，基于 PySnooper。
    用于在运行时追踪函数的执行路径、变量变化等。
    """

    def __init__(self, log_file: str = "trace.log"):
        """
        初始化动态追踪器。

        Args:
            log_file: 追踪日志保存路径
        """
        self.log_file = log_file

    def trace_function(self, func: Callable, *args, **kwargs) -> Any:
        """
        追踪特定函数的执行。

        Args:
            func: 要追踪的函数
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            Any: 函数的返回值
        """
        # 使用 pysnooper 装饰器包装函数
        # 注意: 这里我们动态应用装饰器，而不是在定义时应用

        @pysnooper.snoop(self.log_file)
        def wrapper(*w_args, **w_kwargs):
            return func(*w_args, **w_kwargs)

        try:
            return wrapper(*args, **kwargs)
        except Exception as e:
            logger.error(f"动态追踪执行失败: {e}")
            raise

    def create_trace_decorator(self, **snoop_kwargs):
        """
        创建一个配置好的追踪装饰器，可直接用于装饰函数。

        Args:
            **snoop_kwargs: 传递给 pysnooper.snoop 的参数

        Returns:
            Callable: 装饰器
        """
        return pysnooper.snoop(self.log_file, **snoop_kwargs)
