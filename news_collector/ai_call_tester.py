import os
from common.ConfigManager import ConfigManager
from common.Logger import Logger
from crypto.CryptoUtil import CryptoUtil
from analysis.OpenAICall import OpenAICall

환경관리자 = ConfigManager()
로깅디렉토리 = 환경관리자.get('log_dir')
시스템명 = 환경관리자.get('system_name')
로그출력 = Logger(로깅디렉토리)

암호키디렉토리 = 환경관리자.get('key_file_path')
암호키파일명 = 환경관리자.get('key_file_name')

암복호유틸 = CryptoUtil(암호키디렉토리, 암호키파일명)

api_key = 환경관리자.get('api_key')
decrypted_api_key = 암복호유틸.decrypt(api_key)
로그출력.debug(시스템명, decrypted_api_key)

my_model =  환경관리자.get('my_model')
로그출력.debug(시스템명, my_model)
로그출력.debug(시스템명, 환경관리자.get('my_prompt').replace('||', '\n'))
my_prompt = 환경관리자.get('my_prompt').replace('||', '\n')

news_text = "이복현 금융감독원장은 13일 서울 여의도 한국경제인협회 컨퍼런스센터에서 기자들과 만나 홍콩 ELS 손실 관련 제도개선 방안에 대한 언론 보도를 언급한 뒤 “(ELS 등으로 고객 손실 발생 시) 직원들의 성과 평가와 연결하는 방안을 비롯해 미래 지향적인 방안을 검토할 것”이라며 “3월 중에라도 당국, 업계, 협회, 전문가들 모두 TF 구성해서 가시적 성과가 연내 도출되도록 하겠다”고 말했다. 앞서 언론과 학계에서는 고객에게 손실이 발생했을 때 직원 성과급을 제한하고, 고위험 상품 판매를 부추기는 성과·인사평가체계와 영업 관행을 고쳐야 한다는 지적도 제기됐다."


openai_call = OpenAICall(시스템명, decrypted_api_key, my_model, my_prompt)
success, result = openai_call.analyze_news(news_text)

if success:
    print("뉴스 감정 분석 결과:", result)
else:
    print("분석 실패:", result)