"""
OpenAI GPT-4o-mini 客戶端
代表立場：貓比較聰明
"""

import openai
import os
import sys

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
        return "你是一個客觀的辯論總結者。請根據提供的完整辯論內容，客觀分析各方論點並總結辯論結果，最後再給出你覺得這場辯論是哪個立場勝利的結論。請使用繁體中文，言簡意賅地進行總結。"
        
    def get_response(self, messages, stream=False):
        """獲取 AI 回應"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=2000,
                temperature=0.7,
                stream=stream
            )
            
            if stream:
                # 處理 streaming 回應
                full_response = ""
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        print(content, end='', flush=True)
                        full_response += content
                return full_response
            else:
                return response.choices[0].message.content.strip()
                
        except Exception as e:
            error_msg = f"OpenAI API 呼叫失敗: {str(e)}"
            if stream:
                print(error_msg, end='', flush=True)
            return error_msg