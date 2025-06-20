"""
OpenAI GPT-4o-mini 客戶端
代表立場：貓比較聰明
"""

import openai
import os

class OpenAIClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = openai.OpenAI(api_key=self.api_key)
        self.stance = "貓比較聰明"
        self.model = "gpt-4o-mini"
        
    def get_system_prompt(self):
        """獲取系統提示詞"""
        return f"你是一個參與群體討論的 AI，你的立場是「{self.stance}」。請堅持並論證貓比狗更加聰明的觀點。請使用繁體中文，發言字數限制為 150 字以內。"
    
    def get_summary_system_prompt(self):
        """獲取總結階段的系統提示詞"""
        return "你是一個客觀的辯論總結者。請根據提供的完整辯論內容，客觀分析各方論點並總結辯論結果。請使用繁體中文，限 300 字以內。"
        
    def get_response(self, messages):
        """獲取 AI 回應"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"OpenAI API 呼叫失敗: {str(e)}"