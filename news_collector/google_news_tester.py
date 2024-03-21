import googlefinance

# API 키 설정
api_key = "YOUR_API_KEY"

# 뉴스 기사 가져오기
def get_news(query, start_date, end_date):
  """
  Google Finance API를 이용하여 뉴스 기사를 가져옵니다.

  Args:
    query: 뉴스 검색어
    start_date: 검색 시작 날짜 (YYYY-MM-DD 형식)
    end_date: 검색 종료 날짜 (YYYY-MM-DD 형식)

  Returns:
    뉴스 기사 목록
  """
  params = {
      "q": query,
      "start": start_date,
      "end": end_date,
      "sort": "date",
      "output": "json"
  }
  url = googlefinance.get_url("news", params, api_key)
  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    return data["articles"]
  else:
    raise Exception("API 요청 실패: {}".format(response.status_code))

# 예시
query = "tesla"
start_date = "2023-11-01"
end_date = "2023-12-31"

news_articles = get_news(query, start_date, end_date)

# 뉴스 기사 출력
for article in news_articles:
  print("제목:", article["title"])
  print("출처:", article["source"])
  print("링크:", article["link"])
  print("발행일:", article["published_date"])
  print("------------------------")
