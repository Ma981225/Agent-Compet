"""
日志工具模块
"""
import logging
import sys
from typing import Any

# 配置日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def log_info(message: str, *args: Any) -> None:
    """记录信息日志（懒插值）"""
    logger.info(message, *args)


def log_error(message: str, *args: Any) -> None:
    """记录错误日志（懒插值）"""
    logger.error(message, *args)


def log_warning(message: str, *args: Any) -> None:
    """记录警告日志（懒插值）"""
    logger.warning(message, *args)


def log_debug(message: str, *args: Any) -> None:
    """记录调试日志（懒插值）"""
    logger.debug(message, *args)
