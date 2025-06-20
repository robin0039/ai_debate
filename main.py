#!/usr/bin/env python3
"""
AI 辯論 Demo 主程式
讓三個 AI 模型就「貓比較聰明還是狗比較聰明？」進行辯論
"""

import os
import sys
from dotenv import load_dotenv
from models.openai_client import OpenAIClient
from models.gemini_client import GeminiClient
from models.openrouter_client import OpenRouterClient
from debate_session import DebateSession

def check_env_keys():
    """檢查環境變數設定"""
    required_keys = ['OPENAI_API_KEY', 'GOOGLE_API_KEY', 'OPENROUTER_API_KEY']
    missing_keys = []
    
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)
    
    if missing_keys:
        print("❌ 缺少必要的 API 金鑰環境變數：")
        for key in missing_keys:
            print(f"   - {key}")
        print("\n請設定環境變數或建立 .env 檔案，參考 .env.example")
        return False
    
    return True

def main():
    """主程式進入點"""
    # 載入環境變數
    load_dotenv()
    
    # 檢查 API 金鑰
    if not check_env_keys():
        sys.exit(1)
    
    try:
        # 初始化 AI 客戶端
        print("🔧 初始化 AI 客戶端...")
        openai_client = OpenAIClient()
        gemini_client = GeminiClient()
        openrouter_client = OpenRouterClient()
        
        # 建立辯論會議
        debate_session = DebateSession(
            openai_client=openai_client,
            gemini_client=gemini_client, 
            openrouter_client=openrouter_client
        )
        
        # 開始辯論
        debate_session.start_debate()
        
        print("\n🎉 辯論結束！感謝各位 AI 的精彩表現！")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 使用者中斷辯論")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 發生錯誤：{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()