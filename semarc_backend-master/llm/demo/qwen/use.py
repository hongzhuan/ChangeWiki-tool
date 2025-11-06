import time
from datetime import timedelta

from openai import OpenAI
from llm.demo.qwen.config import QwenConfig


def call_qwen(prompt: str) -> str:
    try:
        client = OpenAI(
            api_key=QwenConfig.API_KEY,
            base_url=QwenConfig.BASE_URL
        )

        completion = client.chat.completions.create(
            model=QwenConfig.MODEL,
            messages=[
                {"role": "system", "content": "你是一个资深软件分析工程师。"},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content

    except Exception as e:
        return f"千问API调用失败: {str(e)}"


if __name__ == "__main__":
    start_time = time.time()

    user_question = "用Python实现二分查找算法"
    answer = call_qwen(user_question)
    print("🟢 用户问题:", user_question)
    print("🔵 AI回答:", answer)

    elapsed = time.time() - start_time
    print(f"\n分析完成! 总耗时: {timedelta(seconds=elapsed)} [时:分:秒]")
