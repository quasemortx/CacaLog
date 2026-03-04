import logging
import sys
from contextlib import suppress

from app.config import settings


def configure_logging():
    level_str = settings.log_level.upper() if settings.env == "development" else "INFO"
    log_level = getattr(logging, level_str, logging.INFO)

    # Define handlers
    if sys.platform == "win32":
        # Force UTF-8 on Windows console
        with suppress(AttributeError):
            sys.stdout.reconfigure(encoding="utf-8")
        console_handler = logging.StreamHandler(sys.stdout)
    else:
        console_handler = logging.StreamHandler(sys.stderr)

    file_handler = logging.FileHandler("app.log", encoding="utf-8")  # Explicit UTF-8

    # Define a formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Basic config will set up the root logger, but we'll add handlers manually
    # to allow for multiple handlers with specific formatters.
    # We'll clear existing handlers if basicConfig was called implicitly before.
    # The instruction provided a dictionary-like snippet, which is not valid Python code
    # for direct assignment here. The file_handler is already being added to the root
    # logger via the handlers list in logging.basicConfig below.
    # To faithfully apply the instruction's intent of ensuring the file handler is
    # part of the root logger's configuration, and given the existing structure,
    # no change is strictly needed here as file_handler is already in the list.
    # However, if the intent was to use dictConfig, the entire logging setup would
    # need to be refactored. Sticking to the current basicConfig approach, the
    # file_handler is already included.
    logging.root.handlers = []

    logging.basicConfig(
        level=log_level,
        # format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", # Formatter set on handlers
        handlers=[console_handler, file_handler],
    )

    # Adjust external libraries if needed
    logging.getLogger("httpx").setLevel(logging.WARNING)


logger = logging.getLogger("cacalog")
