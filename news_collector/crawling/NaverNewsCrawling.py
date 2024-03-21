import requests
from bs4 import BeautifulSoup

class NaverNewsCrawling:
    def __init__(self):
        self.media_info = [
                             ["네이버", "경제", "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101"]
                          ]

    def runCrawling(self):
        results = []
        success = True

        for media_name, category, base_url in self.media_info:
            try:
                response = requests.get(base_url)
                soup = BeautifulSoup(response.content, "html.parser")
                news_list = soup.find("body", class_="n_news_mnews fs1 as_mp_layout as_section_home")
                
                if not news_list:  # 검증 추가: news_list가 None인 경우 처리
                    continue
                
                news_count = 1
                for news in news_list.find_all("div", class_="sa_text"):
                    # 뉴스 제목 추출
                    title = news.find("strong").text.strip()
                    
                    # 뉴스 링크 추출
                    link = news.find("a")["href"]
                    
                    # 뉴스 페이지 요청 및 응답
                    news_page_response = requests.get(link)
                    
                    # 뉴스 페이지 HTML 파싱
                    news_page_soup = BeautifulSoup(news_page_response.content, "html.parser")

                    # # 뉴스 발행시간 추출
                    tag = news_page_soup.find("span", class_="media_end_head_info_datestamp_time _ARTICLE_DATE_TIME")
                    if tag != None :
                        published_time = tag.text.strip()[5:]
                    else :
                        published_time = 'None'
                        
                    tag = news_page_soup.find("span", class_="media_end_head_info_datestamp_time _ARTICLE_MODIFY_DATE_TIME")
                    if tag != None :
                        modify_time = tag.text.strip()[5:]
                    else :
                        modify_time = 'None'
            
                    # # 뉴스 기자 이름 추출
                    tag = news_page_soup.find("em", class_="media_end_head_journalist_name")
                    if tag != None :
                        author = tag.text.strip()
                    else :
                        modify_time = 'None author'

                    # # 뉴스 내용 추출
                    tag = news_page_soup.find("article", class_="go_trans _article_content")
                    if tag != None :
                        content = tag.text.strip()
                    else :
                        modify_time = 'None content'

                    results.append({
                        "미디어명": media_name,
                        "카테고리": category,
                        "제목": title,
                        "링크": link,
                        "발행시간": published_time,
                        "수정시간": modify_time,
                        "기자": author,
                        "내용": content
                    })
                    news_count += 1
            except Exception as e:
                success = False
                return success, [f"Error occurred: {str(e)}"]

        return success, results

if __name__ == "__main__":
    # 사용 예시
    media_info = [
        ["네이버", "경제", "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101"]
    ]
    crawler = NaverNewsCrawling(media_info)
    success, results = crawler.runCrawling()

    if success:
        for result in results:
            for key, value in result.items():
                print(f"{key}: {value}")
            print("-----------------")
    else:
        print(results[0])  # 오류 메시지 출력
