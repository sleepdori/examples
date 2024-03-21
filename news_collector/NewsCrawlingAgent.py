import threading
import time
import importlib
from common.ConfigManager import ConfigManager
from common.Logger import Logger
from dbutil.MongoDBManager import MongoDBManager
from datetime import datetime
from crypto.CryptoUtil import CryptoUtil
from analysis.OpenAICall import OpenAICall
from common.TelegramMessage import TelegramMessage
import pandas as pd

환경관리자 = ConfigManager()
로깅디렉토리 = 환경관리자.get('log_dir')
시스템명 = 환경관리자.get('system_name')
로그출력 = Logger(로깅디렉토리)
news_portal_list = (환경관리자.get('news_portal_list')).split(',')
로그출력.debug(시스템명, f"{news_portal_list[0]}, {news_portal_list[1]}")

class CrawlingThread(threading.Thread):

    def __init__(self, portal_name, class_name, logger, system_name):
        threading.Thread.__init__(self)
        self.portal_name = portal_name
        # module_name, class_name = class_name.split(':')
        self.class_nm = class_name.replace("'", '')
        print(f"#####################################{self.class_nm}")
        module = importlib.import_module(f'crawling.{self.class_nm}')
        class_ = getattr(module, self.class_nm)
        self.crawler = class_()
        self.logger = logger
        self.system_name = system_name
        self.is_running = True
        self.환경관리자 = ConfigManager()
        self.암호키디렉토리 = self.환경관리자.get('key_file_path')
        self.암호키파일명 = self.환경관리자.get('key_file_name')
        self.암복호유틸 = CryptoUtil(self.암호키디렉토리, self.암호키파일명)
        self.데이터베이스주소 = self.암복호유틸.decrypt(self.환경관리자.get('database_server_uri'))
        self.데이터베이스명 = self.암복호유틸.decrypt(self.환경관리자.get('database_name'))
        self.데이터베이스사용자 = self.암복호유틸.decrypt(self.환경관리자.get('database_user'))
        self.데이터베이스비밀번호 = self.암복호유틸.decrypt(self.환경관리자.get('database_passwd'))
        self.api_key = self.환경관리자.get('api_key')
        self.decrypted_api_key = self.암복호유틸.decrypt(self.api_key)
        self.my_model =  self.환경관리자.get('my_model')
        self.my_prompt = self.환경관리자.get('my_prompt').replace('||', '\n')
        self.telegram_bot_token = self.환경관리자.get('telegram_bot_token')
        self.chat_ids = self.환경관리자.get('telegram_chat_list')
        self.decrypted_bot_token = self.암복호유틸.decrypt(self.telegram_bot_token)

        self.openai_call = OpenAICall(self.system_name, self.decrypted_api_key, self.my_model, self.my_prompt)

        # MongoDB 연결 관리자 인스턴스 생성
        self.db_mgr = MongoDBManager(self.데이터베이스주소, self.데이터베이스명, self.데이터베이스사용자, self.데이터베이스비밀번호)

    def check_keywords_in_news(self, keywords, news_content):
        included_keywords = {
            '검색키워드': []
        }

        for keyword in keywords:
            search_keyword = keyword.get('검색키워드', None)
            if search_keyword and search_keyword in news_content:
                included_keywords['검색키워드'].append(search_keyword)

            # Check for related keywords, ensuring each is listed only once
            # for key in ['관련키워드1', '관련키워드2', '관련키워드3']:
            #     related_keyword = keyword.get(key, None)
            #     if pd.isna(related_keyword):
            #         continue                
            #     if related_keyword and related_keyword in news_content and related_keyword not in included_keywords['관련키워드']:
            #         included_keywords['관련키워드'].append(related_keyword)
            #         included_keywords['관련키워드유무'] = True

        return included_keywords


    def run(self):
        while self.is_running:
            # 오늘 날짜를 YYYYMMDD 형식으로 변환
            today = datetime.now().strftime('%Y%m%d')

            # 쿼리 실행
            # 검색시작일자가 오늘보다 같거나 작고 검색종료일자가 오늘보다 같거나 큰 문서 조회
            query = {
                "검색시작일자": {"$lte": int(today)},
                "검색종료일자": {"$gte": int(today)}
            }
            self.logger.debug(self.system_name, f"검색키워드 조회 : {query}")
            key_success, keywords = self.db_mgr.select('검색키워드', query)
            if key_success :
                self.logger.debug(self.system_name, "검색 키워드를 조회했습니다.")
            success, news = self.crawler.runCrawling()

            if success :
                self.logger.debug(self.system_name, f"{self.portal_name}의 뉴스를 조회 했습니다. 키워드를 검색합니다.")
                for news_content in news :
                    self.logger.debug(self.system_name, f"{news_content['제목']} 뉴스에 키워드가 포함되어 있는지 확인합니다.")
                    key_serching_rslt = self.check_keywords_in_news(keywords, news_content['내용'])
                    self.logger.debug(self.system_name, f"{news_content['제목']}  뉴스에 키워드 검사가 완료 되었습니다. 검출유무를 확인합니다.")
                    if len(key_serching_rslt['검색키워드']) > 0 :
                        str = f"{key_serching_rslt['검색키워드']}"
                        key_serch_result = f"[{str}] 키워드와 관련된 뉴스"
                        query = {
                            "링크": {"$eq": news_content['링크']}
                        }
                        self.logger.debug(self.system_name, f"{news_content['제목']} 뉴스가 이미 발행된 뉴스 여부를 확인합니다.")
                        check_success, check_news = self.db_mgr.select('포털뉴스', query)
                        if check_success :
                            
                            if len(check_news) == 0 : 
                                self.logger.debug(self.system_name, f"{news_content['제목']} 뉴스는 새로운 뉴스 입니다.{check_news}")
                                self.logger.debug(self.system_name, f"{news_content['제목']}  뉴스에 {key_serch_result}를 발견했습니다. 해당 뉴스에 감성분석을 진행합니다.")
                                analyze_success, analyze_result = self.openai_call.analyze_news((news_content['내용']).replace('""', "'"))
                                if analyze_success :
                                    analyze = {
                                                "분야": analyze_result[0],
                                                "주체": analyze_result[1],
                                                "주제": analyze_result[2],
                                                "내용": analyze_result[3],
                                                "감성평가": analyze_result[4],
                                                "긍정부정사유": analyze_result[5]
                                            }
                                    self.logger.debug(self.system_name, f"{news_content['제목']}  뉴스에 감성분석을 진행 완료했습니다. 결과 : {analyze}")
                                    news_content['분석결과'] : analyze
                                    message_str = f"{news_content['제목']}  *|* {key_serch_result} 키워드에 관련된 뉴스 입니다. *|* *|* {analyze_result[0]} *|* {analyze_result[1]} *|* {analyze_result[2]} *|* {analyze_result[4]} *|* *|* {analyze_result[5]} *|* *|* {analyze_result[3]} *|* *|* 원본뉴스 : {news_content['링크']}"
                                    # bot_token을 설정합니다.
                                    telegram_bot = TelegramMessage(self.decrypted_bot_token)
                                    self.logger.debug(self.system_name, f"{news_content['제목']}  뉴스에 메신저로 전송합니다.")
                                    telegram_bot.send_message(self.chat_ids, message_str.replace('*|*', "\n"))
                                    self.logger.debug(self.system_name, f"{news_content['제목']}  뉴스에 메신저로 전송했습니다.")
                                else :
                                    self.logger.error(self.system_name, f"{key_serch_result}를 분석 시도 중 에러가 발생했습니다! 뉴스 : {news_content}")

                        else :
                            self.logger.error(self.system_name, f"{key_serch_result}를 이미 발행된 뉴스 인지 확인 중 에러 발생: {check_news}")

                    self.logger.debug(self.system_name, f"{news_content['제목']}  뉴스를 Database에 저장합니다.")
                    self.logger.debug(self.system_name, f"{news_content['제목']}  뉴스의 링크 정보 : {news_content['링크']}")
                    upsert_success, upsert_message = self.db_mgr.upsert("포털뉴스", '링크', news_content)
                    # upsert_success, upsert_message = self.db_mgr.insert("포털뉴스", news_content)
                    if upsert_success : 
                        self.logger.debug(self.system_name, f"{news_content['제목']} Database에 저장 했습니다. {upsert_message}")
                    else :
                        self.logger.error(self.system_name, f"{news_content['제목']} Database에 저장에 실패 했습니다. {upsert_message}")
            else :
                self.logger.error(self.system_name, f"{self.portal_name} Crawling: Success={success}, Results={news}")

            self.logger.debug(self.system_name, f"{self.portal_name}의 뉴스 조회를 완료 했습니다. 5분후에 재 조회 합니다.")
            time.sleep(5 * 60)  # 5분 대기

    def stop(self):
        self.is_running = False


def monitor_threads():
    while True:
        for portal_name, thread in list(crawling_threads.items()):
            if not thread.is_alive():
                print(f"{portal_name} 스레드가 비정상적으로 종료되었습니다. 스레드를 재시작합니다.")
                thread.stop()  # 현재 실행 중인 스레드 중지
                portal_name, class_name = thread.portal_name, thread.class_name
                new_thread = CrawlingThread(portal_name, class_name)  # 새 스레드 객체 생성
                new_thread.start()  # 새 스레드 시작
                crawling_threads[portal_name] = new_thread  # 스레드 딕셔너리 업데이트
        time.sleep(60 * 60)  # 60분 대기

# 스레드를 관리하기 위한 딕셔너리
crawling_threads = {}

# 각 뉴스 포털에 대한 크롤링 스레드 생성 및 시작
for portal in news_portal_list:
    portal_name, class_name = portal.split(':')
    thread = CrawlingThread(portal_name, class_name, 로그출력, 시스템명)
    thread.start()
    crawling_threads[portal_name] = thread

# 스레드 모니터링 스레드 시작
monitor_thread = threading.Thread(target=monitor_threads)
monitor_thread.start()
