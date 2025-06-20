"""
Google Gemini 2.5-flash 客戶端
代表立場：狗比較聰明
"""

import google.generativeai as genai
import os

class GeminiClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.stance = "狗比較聰明"
        
    def get_system_prompt(self):
        """獲取系統提示詞"""
        return f"你是一個參與群體討論的 AI，你的立場是「{self.stance}」。請堅持並論證狗比貓更加聰明的觀點。請使用繁體中文，發言字數限制為 150 字以內。"
    
    def get_summary_system_prompt(self):
        """獲取總結階段的系統提示詞"""
        return "你是一個客觀的辯論總結者。請根據提供的完整辯論內容，客觀分析各方論點並總結辯論結果，最後再給出你覺得這場辯論是哪個立場勝利的結論。請使用繁體中文，限 300 字以內。"
        
    def get_response(self, messages):
        """獲取 AI 回應"""
        try:
            # 將 OpenAI 格式的 messages 轉換為 Gemini 格式
            prompt_parts = []
            for msg in messages:
                if msg['role'] == 'system':
                    prompt_parts.append(f"System: {msg['content']}")
                elif msg['role'] == 'user':
                    prompt_parts.append(f"User: {msg['content']}")
                elif msg['role'] == 'assistant':
                    prompt_parts.append(f"Assistant: {msg['content']}")
            
            full_prompt = "\n".join(prompt_parts)
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=200,
                    temperature=0.7
                )
            )
            return response.text.strip()
        except Exception as e:
            return f"Gemini API 呼叫失敗: {str(e)}"