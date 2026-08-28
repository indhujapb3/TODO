import logging
import sys


def setup_logging():
    # -----------------------------
    # Application logging
    # -----------------------------

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # -----------------------------
    # SQLAlchemy SQL logging
    # -----------------------------

    sqlalchemy_logger = logging.getLogger(
        "sqlalchemy.engine"
    )

    sqlalchemy_logger.setLevel(logging.INFO)