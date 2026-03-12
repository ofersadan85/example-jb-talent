import logging
import sys

import httpx

# logging.basicConfig(level=logging.DEBUG, filename="myapp.log", format=log_fmt)
logger = logging.getLogger("myapp")


def setup_logging():
    logger.setLevel(logging.ERROR)

    if not logger.handlers:
        print_handler = logging.StreamHandler(sys.stdout)
        print_handler.setLevel(logging.INFO)
        print_fmt = logging.Formatter("%(levelname)s %(message)s")
        print_handler.setFormatter(print_fmt)

        file_handler = logging.FileHandler("myapp.log")
        file_handler.setLevel(logging.DEBUG)
        file_fmt = logging.Formatter(
            "%(asctime)s %(levelname)s (%(filename)s:%(funcName)s:%(lineno)d) %(message)s"
        )
        file_handler.setFormatter(file_fmt)

        logger.addHandler(print_handler)
        logger.addHandler(file_handler)


# message
#    |
#   logger("myapp")
#            |
#            -----> print_handler
#            |
#            -----> file_handler


def google():
    print("Normal print")
    logger.info("We are checking google")
    httpx.get("https://www.google.com")
    logger.info("Done checking google")


if __name__ == "__main__":
    setup_logging()
    google()
    logger.info("Test")
