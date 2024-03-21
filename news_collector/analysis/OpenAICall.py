import time
from openai import OpenAI
import re
from common.Logger import Logger

class OpenAICall:
    def __init__(self, system_nm, api_key, my_model, my_prompt):
        self.client = OpenAI(api_key=api_key)
        self.my_prompt = my_prompt
        self.my_model = my_model
        self.logger = Logger(system_nm)
    def analyze_news(self, news_text, target_char='"', replacement_char='\"'):
        # 코드 실행 전 시간
        start_time = time.time()
        # 입력된 문자열에서 target_char를 replacement_char로 치환
        modified_text = news_text.replace(target_char, replacement_char)
        try:
            response = self.client.chat.completions.create(
                model=self.my_model,
                messages=[
                    {"role": "system", "content": self.my_prompt},
                    {"role": "user", "content": news_text}
                ]
            )
            content = response.choices[0].message.content
            # 결과 내용에서 요구한 섹션 추출
            return_content = self._extract_sections(content)
        
            return True, return_content
        except Exception as e:
            self.logger.error('openai', "analyze_news method call error...", e)
            return False, str(e)
        finally :
            # 코드 실행 후 시간
            end_time = time.time()
            self.logger.info('openai', "OpenAI Model Call 소요 시간 : %d 초 "%(end_time-start_time) )

    def _extract_sections(self, content):
        sections = []
        for i in range(1, 7):
            # 섹션 번호를 기준으로 내용을 매칭하기 위한 정규 표현식 수정
            pattern = rf"{i}\.\s*([^\n]+)"
            matches = re.findall(pattern, content)
            
            # 매칭된 내용이 있다면 해당 내용을, 없다면 빈 문자열을 추가
            section_content = " ".join(matches).strip() if matches else ""
            sections.append(section_content)
        return sections

