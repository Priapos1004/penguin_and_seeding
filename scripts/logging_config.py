"""Setup for logging."""
import logging
import sys
from logging import Filter, Handler, Logger


def setup_logging(focus_on: bool):
    """
    Configure root logging.

    If focus_on is True, only logs from pynguin.generator and pynguin.custom_seeding
    will be emitted. Otherwise, all INFO+ logs are shown.
    """
    # 1) get root logger & clear any existing handlers
    root: Logger = logging.getLogger()
    root.setLevel(logging.INFO)
    for h in list(root.handlers):
        root.removeHandler(h)

    # 2) build your console handler & formatter
    handler: Handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    fmt = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    handler.setFormatter(logging.Formatter(fmt))

    # 3) if focus_on, only allow those two modules
    if focus_on:
        allowed_modules = ["pynguin.custom_seeding"]
        allowed_messages = [
            "Parsed testcases:",
            "Used search time:",
            "Seeding took",
        ]
        class FocusFilter(Filter):
            def filter(self, record):
                # Allow logs from allowed modules
                allowed_pynguin_modules_condition = any(record.name.startswith(mod) for mod in allowed_modules)
                # Allow any other module that does not start with "pynguin"
                non_pynguin_modules = not record.name.startswith("pynguin")
                # Allow logs with specific messages
                allowed_message_condition = any(msg in record.getMessage() for msg in allowed_messages)
                return (
                    allowed_pynguin_modules_condition or
                    non_pynguin_modules or
                    allowed_message_condition
                )
        handler.addFilter(FocusFilter())

    # 4) attach it
    root.addHandler(handler)
