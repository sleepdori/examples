import os
from threading import Lock
from common.Logger import Logger
from crypto.CryptoUtil import CryptoUtil

class ConfigManager:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ConfigManager, cls).__new__(cls)
                cls._instance._load_config()
            return cls._instance

    def _load_config(self):
        env_file = os.getenv('ENV_FILE_NM')
        if not env_file:
            raise ValueError('환경 변수 ENV_FILE_NM이 설정되지 않았습니다.')
        self.configs = {}
        with open(env_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    self.configs[key.strip()] = value.strip()

            self.print_config()  # 환경 파일을 읽은 후에 설정을 출력합니다.

    def get(self, key):
        return self.configs.get(key)

    def print_config(self):
        로깅디렉토리 = self.get('log_dir')
        시스템명 = self.get('system_name')
        로그출력 = Logger(로깅디렉토리)
        
        for key, value in self.configs.items():
            if not key.startswith('database'):
                if key == "my_prompt" :
                    value = value.replace('\\n', '\n')
                로그출력.debug(시스템명, f"{key} = {value}")
# 사용 예
# config_manager = ConfigManager()
# print(config_manager.get_value('some_key'))
