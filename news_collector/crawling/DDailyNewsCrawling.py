import requests
from bs4 import BeautifulSoup

class DDailyNewsCrawling:
    def __init__(self):
        self.media_info = [
                                ["디지털데일리", "뉴스", "https://ddaily.co.kr/news"]
                          ]

    def runCrawling(self):
        results = []
        success = True
        start_page = 1
        end_page = 1
        for media_name, category, base_url in self.media_info:
            print(f"**{media_name} - {category}**")
            
            for page in range(start_page, end_page + 1):
                url = f"{base_url}?page={page}"
                response = requests.get(url)
                soup = BeautifulSoup(response.content, "html.parser")
                news_list = soup.find("div", class_="arl_013")

                if not news_list:
                    continue

                for news in news_list.find_all("p", class_="title"):
                    title = news.find("a").text.strip()
                    link = news.find("a")["href"]
                    news_page_response = requests.get(f"https://ddaily.co.kr{link}")
                    news_page_soup = BeautifulSoup(news_page_response.content, "html.parser")

                    published_time = news_page_soup.find("span", class_="date").text.strip()
                    author = news_page_soup.find("span", class_="writer").text.strip()
                    content_raw = news_page_soup.find("div", class_="article_content").text.strip()
                    start_index = content_raw.find(f"{author}]") + len(f"{author}]")
                    content = content_raw[start_index:].strip()
                    modify_time = 'None'

                    result = {
                        "미디어명": media_name,
                        "카테고리": category,
                        "제목": title,
                        "링크": f"https://ddaily.co.kr{link}",
                        "발행시간": published_time,
                        "수정시간": modify_time,
                        "기자": author,
                        "내용": content
                    }
                    results.append(result)
        
        return success, results

if __name__ == "__main__":
    # 사용 예시
    start_page = 1
    end_page = 1

    crawler = DDailyNewsCrawling()
    success, results = crawler.runCrawling()

    if success:
        for result in results:
            for key, value in result.items():
                print(f"{key}: {value}")
            print("-----------------")
    else:
        print("크롤링 실패")
