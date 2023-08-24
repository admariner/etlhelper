"""
Library to simplify data transfer between databases
"""
import logging
import sys
import warnings
from importlib.metadata import (
    PackageNotFoundError,
    version,
)

# Import helper functions here for more convenient access
# flake8: noqa
from etlhelper.abort import abort_etlhelper_threads
from etlhelper.db_params import DbParams
from etlhelper.etl import (
    copy_rows,
    execute,
    executemany,
    fetchone,
    fetchall,
    generate_insert_sql,
    get_rows,
    iter_chunks,
    iter_rows,
    load,
    copy_table_rows,
)
from etlhelper.connect import (
    connect,
    get_connection_string,
    get_sqlalchemy_connection_string,
)
from etlhelper.utils import (
    table_info,
)
from etlhelper import (
    row_factories,
)

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "0.0.0"

warnings.warn(
    (
        "ETLHelper version 1.0.0 is coming soon and will contain many breaking changes. "
        "Users should pin their versions '(etlhelper<1)' and check GitHub for release details."
    ),
    DeprecationWarning,
    stacklevel=2,
)

# Create etlhelper logger and clear the logger handlers
# This prevents a new logger from being created when running 'logging.getLogger("etlhelper")'
# with default handlers
logging.getLogger("etlhelper").handlers.clear()


def log_to_console(level=logging.INFO, output=sys.stderr) -> None:
    """
    Log ETLHelper messages to the given output.

    :param level: logger level
    :param output: the output location of the logger messages
    """
    logger = logging.getLogger('etlhelper')
    # Clear all existing handlers to prevent duplicate output
    logger.handlers.clear()

    # Prepare log handler.  See this StackOverflow answer for details:
    # https://stackoverflow.com/a/27835318/3508733
    class CleanDebugMessageFormatter(logging.Formatter):
        default_fmt = logging.Formatter('%(asctime)s %(funcName)s: %(message)s')
        debug_fmt = logging.Formatter('%(message)s')

        def format(self, record):
            if record.levelno < logging.INFO:
                return self.debug_fmt.format(record)
            else:
                return self.default_fmt.format(record)

    handler = logging.StreamHandler(output)
    handler.setFormatter(CleanDebugMessageFormatter())

    # Configure logger
    logger.addHandler(handler)
    logger.setLevel(level=level)
