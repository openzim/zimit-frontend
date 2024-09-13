import logging
import sys
from typing import IO

DEFAULT_FORMAT = "%(levelname)s: %(message)s"
VERBOSE_DEPENDENCIES = ["urllib3", "PIL", "boto3", "botocore", "s3transfer"]


def get_logger(
    name: str,
    level: int | str = logging.INFO,
    console: IO[str] | None = sys.stdout,
    log_format: str | None = DEFAULT_FORMAT,
    deps_level: int | str = logging.WARNING,
    additional_verbose_deps: list[str] | None = None,
):
    """configured logger for most usages

    - name: name of your logger
    - level: console level
    - log_format: format string
    - console: sys.stdout | sys.stderr | any other IO[str]
    - deps_level: log level for idendified verbose dependencies
    - additional_deps: additional modules names of verbose dependencies
        to assign deps_level to"""

    if additional_verbose_deps is None:  # pragma: no branch
        additional_verbose_deps = []

    # set arbitrary level for some known verbose dependencies
    # prevents them from polluting logs
    for logger_name in set(VERBOSE_DEPENDENCIES + additional_verbose_deps):
        logging.getLogger(logger_name).setLevel(deps_level)

    logger = logging.Logger(name)
    logger.setLevel(logging.DEBUG)

    # setup console logging
    console_handler = logging.StreamHandler(console)
    console_handler.setFormatter(logging.Formatter(log_format))
    console_handler.setLevel(level)
    logger.addHandler(console_handler)

    return logger
