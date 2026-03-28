import datetime
import logging
import os
from pathlib import Path


def configure_logging() -> logging.Logger:
    default_log_dir = Path(__file__).resolve().parent.parent.parent / "logs"
    log_dir = Path(os.environ.get("LOG_DIR", default_log_dir))
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = (
        log_dir / f"{datetime.datetime.now(tz=datetime.UTC).date()}_mamahealth.log"
    )
    log_format = "%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s"
    log_datefmt = "%Y-%m-%d %H:%M:%S"

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    formatter = logging.Formatter(log_format, datefmt=log_datefmt)

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

    return logging.getLogger(__name__)
