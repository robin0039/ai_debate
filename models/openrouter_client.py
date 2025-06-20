"""
OpenRouter DeepSeek 客戶端
代表立場：貓跟狗都很笨
"""

import requests
import json
import os
import sys

class OpenRouterClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        self.stance = "貓跟狗都很笨"
        self.model = "deepseek/deepseek-chat"
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
    def get_system_prompt(self):
        """獲取系統提示詞"""
        return f"你是一個參與群體討論的 AI，你的立場是「{self.stance}」。請堅持並論證貓和狗其實都不算太聰明的觀點。請使用繁體中文，發言字數限制為 150 字以內。"
    
    def get_summary_system_prompt(self):
        """獲取總結階段的系統提示詞"""
        return "你是一個客觀的辯論總結者。請根據提供的完整辯論內容，客觀分析各方論點並總結辯論結果，最後再給出你覺得這場辯論是哪個立場勝利的結論。請使用繁體中文，限 300 字以內。"
        
    def get_response(self, messages, stream=False):
        """獲取 AI 回應"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "HTTP-Referer": "https://github.com/ai-debate-demo",
                "X-Title": "AI Debate Demo",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 200,
                "temperature": 0.7,
                "stream": stream
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=data,
                timeout=30,
                stream=stream
            )
            
            if response.status_code == 200:
                if stream:
                    # 處理 streaming 回應 (SSE)
                    full_response = ""
                    for line in response.iter_lines():
                        if line:
                            line = line.decode('utf-8')
                            if line.startswith('data: '):
                                data_str = line[6:]  # 移除 'data: ' 前綴
                                if data_str == '[DONE]':
                                    break
                                try:
                                    data_json = json.loads(data_str)
                                    if 'choices' in data_json and len(data_json['choices']) > 0:
                                        delta = data_json['choices'][0].get('delta', {})
                                        if 'content' in delta and delta['content']:
                                            content = delta['content']
                                            print(content, end='', flush=True)
                                            full_response += content
                                except json.JSONDecodeError:
                                    continue
                    return full_response
                else:
                    result = response.json()
                    return result['choices'][0]['message']['content'].strip()
            else:
                error_msg = f"OpenRouter API 呼叫失敗: HTTP {response.status_code}"
                if stream:
                    print(error_msg, end='', flush=True)
                return error_msg
                
        except Exception as e:
            error_msg = f"OpenRouter API 呼叫失敗: {str(e)}"
            if stream:
                print(error_msg, end='', flush=True)
            return error_msg