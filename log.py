import logging
import httpx

log_fmt = "%(asctime)s %(levelname)s (%(filename)s:%(funcName)s:%(lineno)d) %(message)s"
# logging.basicConfig(level=logging.DEBUG, filename="myapp.log", format=log_fmt)
logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)
print_handler = logging.StreamHandler()
print_handler.setLevel(logging.DEBUG)
logger.addHandler(print_handler)

# message
#    |
#   logger("myapp")
#            |
#            -----> print_handler


def google():
    logger.info("We are checking google")
    httpx.get("https://www.google.com")
    logger.info("Done checking google")
  


logger.error("This is an error")
logger.warning("This is a warning")
logger.info("This is some info")
logger.debug("This is for debug mode only")

google()
