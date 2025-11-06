import time
from datetime import timedelta

from openai import OpenAI

API_KEY = "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"
MODEL = "deepseek/deepseek-r1-0528-qwen3-8b:free" # 11s
# MODEL = "deepseek/deepseek-chat:free" # 10s
# MODEL = "deepseek/deepseek-r1-0528:free" # 33s
# MODEL = "qwen/qwen-2.5-coder-32b-instruct:free" # 13s
MODEL = "qwen/qwen2.5-vl-72b-instruct:free" # 21s
# MODEL = "deepseek/deepseek-chat-v3-0324:free" # 40+s
SYSTEM_PROMPT = "你是一个资深软件代码分析工程师。"

# 初始化客户端
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=API_KEY)

def call_llm(prompt: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    start_time = time.time()

    user_question = "用Python实现二分查找算法"
    answer = call_llm(user_question)
    print("🟢 用户问题:", user_question)
    print("🔵 AI回答:", answer)

    elapsed = time.time() - start_time
    print(f"\n分析完成! 总耗时: {timedelta(seconds=elapsed)} [时:分:秒]")