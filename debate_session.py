"""
辯論會議控制器
管理三個 AI 模型的辯論流程：3 輪辯論 + 1 輪總結
"""

import time

class DebateSession:
    def __init__(self, openai_client, gemini_client, openrouter_client):
        self.openai_client = openai_client    # 貓派代表
        self.gemini_client = gemini_client    # 狗派代表  
        self.openrouter_client = openrouter_client  # 懷疑派代表
        self.debate_history = []
        self.round_count = 0
        self.participants = [
            ("🐱 貓派", self.openai_client),
            ("🐶 狗派", self.gemini_client), 
            ("🤷 懷疑派", self.openrouter_client)
        ]
        
    def start_debate(self):
        """開始辯論流程"""
        print("🧠 AI 辯論 Demo：《貓比較聰明還是狗比較聰明？》")
        print("=" * 60)
        print("📋 參與者：")
        print("🐱 貓派 (GPT-4o-mini)：堅持貓比較聰明")
        print("🐶 狗派 (Gemini 2.5-flash)：主張狗比較聰明")
        print("🤷 懷疑派 (DeepSeek)：認為貓跟狗都很笨")
        print("=" * 60)
        
        # 進行 3 輪辯論
        for round_num in range(1, 4):
            print(f"\n🔥 第 {round_num} 輪辯論")
            print("-" * 40)
            self.conduct_round(round_num)
            time.sleep(1)
        
        # 總結階段
        print(f"\n📊 辯論總結")
        print("-" * 40)
        self.generate_summary()
        
    def conduct_round(self, round_num):
        """進行單輪辯論"""
        self.round_count = round_num
        
        for name, client in self.participants:
            print(f"\n{name} 發言：")
            
            # 建構訊息
            messages = self._build_messages(client, round_num)
            
            # 獲取回應
            response = client.get_response(messages)
            
            # 儲存到歷史記錄
            self.debate_history.append(f"{name}：{response}")
            
            # 顯示回應
            print(f"💬 {response}")
            print()
            time.sleep(1)
    
    def _build_messages(self, client, round_num):
        """建構 API 訊息格式"""
        messages = []
        
        # 系統提示詞
        messages.append({
            "role": "system",
            "content": client.get_system_prompt()
        })
        
        # 第一輪：直接提問
        if round_num == 1:
            messages.append({
                "role": "user", 
                "content": "主題：「貓比較聰明還是狗比較聰明？」請發表你的看法。"
            })
        else:
            # 第二輪以後：加入歷史對話
            messages.append({
                "role": "user",
                "content": "主題：「貓比較聰明還是狗比較聰明？」請發表你的看法。"
            })
            
            # 加入歷史對話作為 assistant 回應
            if self.debate_history:
                history_text = "\n".join(self.debate_history)
                messages.append({
                    "role": "assistant",
                    "content": history_text
                })
                
                messages.append({
                    "role": "user",
                    "content": "基於以上討論，請繼續發表你的觀點並回應其他人的論點。"
                })
        
        return messages
    
    def generate_summary(self):
        """生成辯論總結"""
        full_debate = "\n".join(self.debate_history)
        
        for name, client in self.participants:
            print(f"\n{name} 總結：")
            
            # 建構總結訊息
            messages = [
                {
                    "role": "system",
                    "content": client.get_summary_system_prompt()
                },
                {
                    "role": "user", 
                    "content": f"以下是完整的辯論內容：\n{full_debate}\n\n請客觀總結這場辯論的結果。"
                }
            ]
            
            # 獲取總結
            summary = client.get_response(messages)
            print(f"📝 {summary}")
            print()
            time.sleep(1)