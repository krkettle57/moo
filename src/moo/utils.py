from datetime import datetime, timedelta, timezone
from logging import DEBUG, INFO, Formatter, Handler, Logger, NullHandler, StreamHandler, basicConfig, getLogger
from time import struct_time
from typing import Optional, Type

JST = timezone(timedelta(hours=9), "Asia/Tokyo")


def now_jst() -> datetime:
    return datetime.now(JST)


def jsttime(*args: Optional[float]) -> struct_time:
    return now_jst().timetuple()


class JSTFormatter(Formatter):
    converter = jsttime


def create_root_logger(name: str, level: int = INFO, handler: Type[Handler] = StreamHandler) -> Logger:
    sh = handler()
    sh.setLevel(level)

    fmt = JSTFormatter("%(asctime)s\t%(process)d\t%(thread)d\t%(name)s\t%(levelname)s\t%(message)s")
    sh.setFormatter(fmt)

    basicConfig(handlers=[sh])

    logger = getLogger(name)
    logger.setLevel(level)
    return logger


def create_logger(name: str, level: int = DEBUG) -> Logger:
    logger = getLogger(name)
    logger.setLevel(level)
    logger.addHandler(NullHandler())
    logger.propagate = True
    return logger
