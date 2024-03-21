import os
from common.ConfigManager import ConfigManager
from common.Logger import Logger
from crypto.CryptoUtil import CryptoUtil


# 환경 변수 'file_nm'의 값을 가져옵니다.
# export ENV_FILE_NM=/work/python/news_collector/common/environment.ini

환경관리자 = ConfigManager()
로깅디렉토리 = 환경관리자.get('log_dir')
시스템명 = 환경관리자.get('system_name')
로그출력 = Logger(로깅디렉토리)
로그출력.debug(시스템명, f"시스템명 :{시스템명}")
# 로그출력.debug(시스템명, "로그출력 테스트")
# 로그출력.debug(시스템명, f"로깅디렉토리 : {로깅디렉토리}")



# 암호키디렉토리 = 환경관리자.get('key_file_path')
# 로그출력.debug(시스템명, f"암호키디렉토리 :{암호키디렉토리}")

# 암호키파일명 = 환경관리자.get('key_file_name')
# 로그출력.debug(시스템명, f"암호키파일명   :{암호키파일명}")

# 암복호유틸 = CryptoUtil(암호키디렉토리, 암호키파일명)

# 데이터베이스주소 = 암복호유틸.decrypt(환경관리자.get('database_server_uri'))
# 로그출력.debug(시스템명, f"데이터베이스주소 : {데이터베이스주소}")

# 데이터베이스명 = 암복호유틸.decrypt(환경관리자.get('database_name'))
# 로그출력.debug(시스템명, f"데이터베이스명 : {데이터베이스명}")

# 데이터베이스사용자 = 암복호유틸.decrypt(환경관리자.get('database_user'))
# 로그출력.debug(시스템명, f"데이터베이스사용자 : {데이터베이스사용자}")

# 데이터베이스비밀번호 = 암복호유틸.decrypt(환경관리자.get('database_passwd'))
# 로그출력.debug(시스템명, f"데이터베이스비밀번호 : {데이터베이스비밀번호}")
