import logging
import os

log_level_env = os.getenv("LOG_LEVEL", "DEBUG")
log_level = getattr(logging, log_level_env.upper()) if log_level_env else logging.INFO
logging.basicConfig(
    level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("LoggerConfig")

logger.info(f"Setting log level to {log_level_env}...")


class CustomLogger:
    def __init__(self, name: str = __name__):
        name = name.replace("__", "")
        self.logger = logging.getLogger(name)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def exception(self, message):
        self.logger.exception(message)


# Example usage:
if __name__ == "__main__":
    logger = CustomLogger("MyLogger")

    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.debug("This is an debug message.")
    logger.critical("This is a critical message.")
