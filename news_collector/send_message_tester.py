import os
from common.ConfigManager import ConfigManager
from common.Logger import Logger
from crypto.CryptoUtil import CryptoUtil
from common.TelegramMessage import TelegramMessage


환경관리자 = ConfigManager()
로깅디렉토리 = 환경관리자.get('log_dir')
시스템명 = 환경관리자.get('system_name')
로그출력 = Logger(로깅디렉토리)

암호키디렉토리 = 환경관리자.get('key_file_path')
암호키파일명 = 환경관리자.get('key_file_name')
로그출력.debug(시스템명, 암호키디렉토리)
로그출력.debug(시스템명, 암호키파일명)
암복호유틸 = CryptoUtil(암호키디렉토리, 암호키파일명)

telegram_bot_token = 환경관리자.get('telegram_bot_token')
chat_ids = 환경관리자.get('telegram_chat_list')
decrypted_bot_token = 암복호유틸.decrypt(telegram_bot_token)
로그출력.debug(시스템명, decrypted_bot_token)

# bot_token을 설정합니다.
telegram_bot = TelegramMessage(decrypted_bot_token)

# chat_id 리스트와 메시지를 설정합니다.
chat_ids = chat_ids
message = "뉴스 감정 분석 결과: ['분야: 정부정책', '주체: 이복현 금융감독원장', '주제: 제도개선 방안', '내용: 이복현 금융감독원장은 홍콩 ELS 손실과 관련해 고객 손실 발생 시 직원들의 성과 평가와 연결하는 등의 제도개선 방안을 검토하겠다고 말했다. 이를 위해 당국, 업계, 협회, 전문가들로 구성된 TF를 3월 중 구성하여 연내 성과를 도출하겠다고 발표했다. 고위험 상품 판매를 부추기는 성과·인사평가 체계와 영업 관행을 개선하려는 의도가 있다.', '감성평가: 긍정적', '긍정/부정 사유: 금융상품 판매로 인한 고객의 손실을 줄이기 위한 제도 개선 방안을 마련하고, 이를 실행하기 위한 구체적인 계획을 발표함으로써, 소비자 보호 강화와 금융업계의 투명성 증진을 도모하려는 긍정적인 노력을 보여주고 있기 때문입니다.']"

# 메시지 전송
telegram_bot.send_message(chat_ids, message)