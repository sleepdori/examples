from dbutil.MongoDBManager import MongoDBManager
from dbutil.ExcelUploader import ExcelUploader
from common.ConfigManager import ConfigManager
from common.Logger import Logger
from crypto.CryptoUtil import CryptoUtil
from datetime import datetime
import pandas as pd

compare_pass = False

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

# 연결 시도
connected, msg = db_mgr.connect()
if not connected:
    print(f"Database connection failed: {msg}")
    exit()

def check_keywords_in_news(keywords, news_content):
    included_keywords = {
        '검색키워드': [],
        '관련키워드': [],
        '검색키워드유무' : False,
        '관련키워드유무' : False
    }

    for keyword in keywords:
        search_keyword = keyword.get('검색키워드', None)
        print(f"################## 1 ,{search_keyword}")
        if search_keyword and search_keyword in news_content:
            included_keywords['검색키워드'].append(search_keyword)
            included_keywords['검색키워드유무'] = True

        # Check for related keywords, ensuring each is listed only once
        for key in ['관련키워드1', '관련키워드2', '관련키워드3']:
            related_keyword = keyword.get(key, None)
            if pd.isna(related_keyword):
                continue
            if related_keyword and related_keyword in news_content and related_keyword not in included_keywords['관련키워드']:
                included_keywords['관련키워드'].append(related_keyword)
                included_keywords['관련키워드유무'] = True

    return included_keywords
    
# 오늘 날짜를 YYYYMMDD 형식으로 변환
today = datetime.now().strftime('%Y%m%d')


# 쿼리 실행
# 검색시작일자가 오늘보다 같거나 작고 검색종료일자가 오늘보다 같거나 큰 문서 조회
query = {
    "검색시작일자": {"$lte": int(today)},
    "검색종료일자": {"$gte": int(today)}
}
로그출력.debug(시스템명, f"검색키워드 조회 : {query}")
key_success, keywords = db_mgr.select('검색키워드', query)

query = {
    "링크": {"$eq": 'https://n.news.naver.com/mnews/article/029/0002861096'}
}
news_success, news = db_mgr.select('포털뉴스', query)
if key_success :
    # 조회 결과 출력
    print(news)
    for doc in keywords:
        로그출력.debug(시스템명, f"document : {doc['검색키워드']}, {doc['관련키워드1']}, {doc['관련키워드2']}, {doc['관련키워드3']}, {doc['검색시작일자']}")
    for news_content in news :
        keywords_result = check_keywords_in_news(keywords, news_content['내용'])
        print(keywords_result)
else :
    로그출력.error(시스템명, f"Error : {result[1]}")




