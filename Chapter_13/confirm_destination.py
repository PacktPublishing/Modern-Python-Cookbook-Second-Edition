"""
Confirm how logging is configured.

It's not always obvious. A "spike" like this can help understand
the current logging configuration
"""
import logging

def main():
    logger = logging.getLogger("main")
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
    logging.shutdown()
