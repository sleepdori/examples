import requests

class TelegramMessage:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.base_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    def send_message(self, ids, msg):
        chat_ids = ids.split(',')
        for chat_id in chat_ids:
            payload = {"chat_id": chat_id.strip(), "text": msg}
            try:
                response = requests.post(self.base_url, data=payload)
                if response.status_code == 200:
                    print(f"메시지가 chat_id {chat_id}로 성공적으로 전송되었습니다.")
                else:
                    print(f"chat_id {chat_id}로 메시지 전송에 실패했습니다. 오류 내용: {response.text}")
            except Exception as e:
                print(f"chat_id {chat_id}로 메시지 전송 중 에러 발생. 에러 내용: {e}")

# # 사용 예
# # bot_token을 설정합니다. 보안상의 이유로 실제 토큰은 여기에 직접 입력하지 않는 것이 좋습니다.
# bot_token = "5792458935:AAFxuKzNcrCcyxZPMoUAm18dg5AfKpl30Lw"
# telegram_bot = TelegramMessage(bot_token)

# # chat_id 리스트와 메시지를 설정합니다.
# chat_ids = "63646483,50244930"
# message = "이것은 테스트 메시지입니다."

# # 메시지 전송
# telegram_bot.send_message(chat_ids, message)
