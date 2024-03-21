from dbutil.MongoDBManager import MongoDBManager
from dbutil.ExcelUploader import ExcelUploader
from common.ConfigManager import ConfigManager
from common.Logger import Logger
from crypto.CryptoUtil import CryptoUtil
from datetime import datetime

compare_pass = True

환경관리자 = ConfigManager()
로깅디렉토리 = 환경관리자.get('log_dir')
시스템명 = 환경관리자.get('system_name')
암호키디렉토리 = 환경관리자.get('key_file_path')
암호키파일명 = 환경관리자.get('key_file_name')
로그출력 = Logger(로깅디렉토리)
암복호유틸 = CryptoUtil(암호키디렉토리, 암호키파일명)

데이터베이스주소 = 암복호유틸.decrypt(환경관리자.get('database_server_uri'))
데이터베이스명 = 암복호유틸.decrypt(환경관리자.get('database_name'))
데이터베이스사용자 = 암복호유틸.decrypt(환경관리자.get('database_user'))
데이터베이스비밀번호 = 암복호유틸.decrypt(환경관리자.get('database_passwd'))

# MongoDB 연결 관리자 인스턴스 생성
db_mgr = MongoDBManager(데이터베이스주소, 데이터베이스명, 데이터베이스사용자, 데이터베이스비밀번호)
collection_name = '검색키워드'
# 연결 시도
connected, msg = db_mgr.connect()
if not connected:
    print(f"Database connection failed: {msg}")
    exit()

# ExcelUploader 인스턴스 생성
file_name = "/work/python/private/search_keyword_list.xlsx"

uploader = ExcelUploader(file_name, collection_name)

# 파일 업로드 실행 (compare 및 upload 메소드를 호출)
del_success, msg = db_mgr.delete_all(collection_name)
if del_success :
    upload_result = uploader.upload(db_mgr, ['검색키워드','업종','관련키워드1','관련키워드2','검색시작일자','검색종료일자','등록일자','등록자명'])
    if upload_result[0] :
        로그출력.info(시스템명, upload_result[1])
    else :
        로그출력.error(시스템명, f"Excel Upload Error : {upload_result[1]}")
else :
    로그출력.error(시스템명, f"{collection_name} Collection Data all delete error.. : {msg}")

# 오늘 날짜를 YYYYMMDD 형식으로 변환
today = datetime.now().strftime('%Y%m%d')

# 쿼리 실행
# 검색시작일자가 오늘보다 같거나 작고 검색종료일자가 오늘보다 같거나 큰 문서 조회
query = {
    "검색시작일자": {"$lte": int(today)},
    "검색종료일자": {"$gte": int(today)}
}
로그출력.debug(시스템명, f"검색키워드 조회 : {query}")
result = db_mgr.select('검색키워드', query)

if result[0] :
    # 조회 결과 출력
    for doc in result[1]:
        로그출력.debug(시스템명, f"document : {doc['검색키워드']}, {doc['업종']}, {doc['관련키워드1']}, {doc['관련키워드2']}, {doc['검색시작일자']}")
else :
    로그출력.error(시스템명, f"Error : {result[1]}")

