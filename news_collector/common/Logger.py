import logging
import logging.handlers
from datetime import datetime

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Logger(metaclass=SingletonMeta):
    def __init__(self, log_file_path, log_format='%(asctime)s [%(levelname)s] %(filename)s: %(message)s', date_format='%Y-%m-%d %H:%M:%S'):
        if not hasattr(self, 'initialized'):  # 클래스가 초기화되지 않았다면 초기화를 진행합니다.
            self.log_file_path = log_file_path
            self.log_format = log_format
            self.date_format = date_format
            self.loggers = {}
            self.initialized = True

    def get_logger(self, category):
        if category not in self.loggers:
            logger = logging.getLogger(category)
            logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter(self.log_format, self.date_format)

            file_handler = logging.FileHandler(
                f"{self.log_file_path}/{category}_{datetime.now().strftime('%Y%m%d')}.log")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            error_file_handler = logging.FileHandler(
                f"{self.log_file_path}/error_{datetime.now().strftime('%Y%m%d')}.log")
            error_file_handler.setLevel(logging.ERROR)
            error_file_handler.setFormatter(formatter)
            logger.addHandler(error_file_handler)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            self.loggers[category] = logger
        return self.loggers[category]

    def debug(self, category, message):
        logger = self.get_logger(category)
        logger.debug(message)

    def info(self, category, message):
        logger = self.get_logger(category)
        logger.info(message)

    def warning(self, category, message):
        logger = self.get_logger(category)
        logger.warning(message)

    def error(self, category, message, exception=None):
        logger = self.get_logger(category)
        if exception:
            logger.error(f"{message}, Exception: {exception}", exc_info=True)
        else:
            logger.error(message)

    def critical(self, category, message):
        logger = self.get_logger(category)
        logger.critical(message)

# 사용 예시
if __name__ == "__main__":
    logger_instance1 = Logger("path/to/log/files")
    logger_instance2 = Logger("path/to/log/files")
    print(logger_instance1 is logger_instance2)  # True를 출력, 두 인스턴스가 동일함을 확인
    
    # 로깅 예시는 이전과 동일하게 사용
    # ...
