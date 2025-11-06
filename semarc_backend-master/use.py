import time
from datetime import timedelta
# from openai import OpenAI
# from config import API_KEY, proxies, API_URL_REDIRECT, LLM_MODEL, USE_PROXY, AVAIL_LLM_MODELS
from uml_to_code_generation import tools as tl
from crazy_utils_no_ui import request_gpt_model_multi_threads_with_no_ui_and_high_efficiency, \
    request_gpt_model_in_new_thread_with_no_ui, generate_manifest_and_project_folder


def call_llm(prompt: str) -> str:
    llm_kwargs = tl.get_default_kwargs()
    return request_gpt_model_in_new_thread_with_no_ui(
        inputs = prompt, 
        llm_kwargs = llm_kwargs,
        history = [],
        sys_prompt = "你是一个资深软件分析工程师。",
        inputs_show_user = "*")



if __name__ == "__main__":
    start_time = time.time()
    user_question = "用Python实现二分查找算法"
    answer = call_llm(user_question)
    print("🟢 用户问题:", user_question)
    print("🔵 AI回答:", answer)
    print(f"\n分析完成! 总耗时: {timedelta(seconds=time.time() - start_time)} [时:分:秒]")