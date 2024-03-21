from crawling.NaverNewsCrawling import NaverNewsCrawling

if __name__ == "__main__":

    crawler = NaverNewsCrawling()
    success, results = crawler.runCrawling()

    if success:
        print(results)
        # for result in results:
        #     for key, value in result.items():
        #         print(f"{key}: {value}")
        #     print("-----------------")
    else:
        print(results[0])  # 오류 메시지 출력