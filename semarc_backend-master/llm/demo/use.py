import os
from openai import OpenAI
from llm.demo.config import QwenConfig


def load_prompt_template(user_input: str) -> str:
    """读取prompt.txt模板并替换用户输入"""
    with open("prompt.txt", "r", encoding="utf-8") as f:
        template = f.read()
    return template.format(user_input=user_input)


def call_qwen(prompt: str) -> str:
    """调用千问API"""
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
    # 示例：用户提问
    user_question = "用Python实现二分查找算法"

    # 组合专业提示词（从prompt.txt加载）
    full_prompt = load_prompt_template(user_question)

    # 调用API获取回答
    answer = call_qwen(full_prompt)

    print("🟢 用户问题:", user_question)
    print("🔵 AI回答:", answer)