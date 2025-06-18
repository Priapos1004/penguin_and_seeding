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
        allowed = ["pynguin.custom_seeding"]
        class FocusFilter(Filter):
            def filter(self, record):
                # record.name is the logger name
                return any(record.name.startswith(mod) or not record.name.startswith("pynguin") for mod in allowed)
        handler.addFilter(FocusFilter())

    # 4) attach it
    root.addHandler(handler)
