import json
import os
import re
from crazy_utils_no_ui import request_gpt_model_in_new_thread_with_no_ui
from pdf_fns.breakdown_txt import breakdown_text_to_satisfy_token_limit
from uml_to_code_generation import tools as tl
from request_llms.bridge_all import model_info
from md2json import md2json_commit_log
from toolbox import write_history_to_file

def analyze_commit_log(commit_log_path, llm_kwargs, output_json_path):
    # 读取 commit log 文件
    with open(commit_log_path, 'r', encoding='utf-8') as f:
        commit_log = f.read()

    print(f"Commit log length: {len(commit_log)}")  # 调试信息

    # 定义 prompt
    initial_prompt = """
    我正在分析同一个软件两个版本之间的变更，下面我将给你两个版本之间的commit log和commit的规范命名规则，你需要根据规范命名规则为这些commit重新分类，并必须按json格式将我每次上传的commit log信息完整输出，不要省略任何一条。规范命名的分类如下：八类变更：style, docs, test, build, cicd, fix, feat, and refactor.

    ### 1. **style**

    **代码风格调整**

    - 与功能无关的格式修改，例如：空格、缩进、换行、分号等
    - 示例：将双引号改为单引号、调整函数间的空行

    ---

    ### 2. **docs**

    **文档变更**

    - 仅修改文档或注释，不影响代码逻辑
    - 示例：更新 README、添加代码注释、修改 API 文档

    ---

    ### 3. **test**

    **测试相关变更**

    - 添加、修改或删除测试代码，不涉及生产代码逻辑
    - 示例：新增单元测试、修复测试用例、补充集成测试

    ---

    ### 4. **build**

    **构建系统或依赖变更**

    - 影响项目构建工具或外部依赖的修改
    - 示例：升级 Webpack 配置、更新 npm 依赖、调整 Maven 脚本

    ---

    ### 5. **ci/cd**

    **持续集成/持续部署配置变更**

    - 修改 CI/CD 流程配置文件
    - 示例：调整 GitHub Actions、更新 Jenkinsfile、修改 Travis CI 配置

    ---

    ### 6. **fix**

    **问题修复**

    - 修复代码中的缺陷或错误
    - 示例：解决内存泄漏、修复边界条件导致的崩溃

    ---

    ### 7. **feat**

    **新增功能**

    - 添加新特性或功能
    - 示例：实现用户登录功能、新增 API 接口

    ---

    ### 8. **refactor**

    **代码重构**

    - 既不修复错误也不增加功能的代码结构优化
    - 示例：拆分臃肿的函数、优化算法复杂度、重命名变量。

    输出的json格式如下：
    {
        "summary": [
            {
                "type": (变更类型，style, docs, test, build, cicd, fix, feat, and refactor之一),
                "ID": （commit ID）,
                "files": [],
                "content": (变更内容)
            },
            ...
        ]
    }
    了解了这部分内容以后我再给你commit log
    """

    # 分段处理 commit log，避免超过 token 限制
    commit_logs = commit_log.split('\n\ncommit ')
    commit_logs = ['commit ' + log for log in commit_logs if log.strip()]

    print(f"Total commits: {len(commit_logs)}")  # 调试信息

    overall_summary = []
    history = []

    for i in range(0, len(commit_logs), 20):
        fragment = '\n\n'.join(commit_logs[i:i+50])
        print(f"Processing fragment {i//20 + 1}/{(len(commit_logs) + 19) // 20}")  # 调试信息
        print(fragment[:500])  # 打印前500个字符，避免输出过长

        i_say = f"{initial_prompt}\n\n{fragment}"
        i_say_show_user = f'正在处理第 {i//20 + 1}/{(len(commit_logs) + 19) // 20} 个片段。'

        gpt_say = request_gpt_model_in_new_thread_with_no_ui(
            inputs=i_say,
            inputs_show_user=i_say_show_user,
            llm_kwargs=llm_kwargs,
            history=history,
            sys_prompt="请根据规范命名规则为这些commit重新分类，并按json格式输出，你必须给我输入中所有commit log的格式化输出，不要省略任何一条。"
        )

        history.extend([i_say_show_user, gpt_say])
        overall_summary.append(gpt_say)

    res = write_history_to_file(history)
    md2json_commit_log(res, output_json_path)

    return output_json_path

def analyze_commit_log2(commit_log_path, output_json_path):
    #不使用大模型直接格式化输出commit log
    # 定义变更类型的关键词映射
    type_keywords = {
        "style": ["style", "format", "whitespace", "indentation"],
        "docs": ["docs", "documentation", "readme", "comment"],
        "test": ["test", "unit test", "integration test"],
        "build": ["build", "dependency", "webpack", "maven"],
        "cicd": ["ci", "cd", "github actions", "jenkins", "travis"],
        "fix": ["fix", "bug", "error", "issue", "crash"],
        "feat": ["feat", "feature", "add", "implement"],
        "refactor": ["refactor", "optimize", "rename", "restructure"]
    }

    # 读取 commit log 文件
    with open(commit_log_path, 'r', encoding='utf-8') as f:
        commit_log = f.read()

    # 分割每个 commit
    commits = commit_log.strip().split("\n\ncommit ")
    commits = ["commit " + c if not c.startswith("commit ") else c for c in commits]

    summary = []

    for commit in commits:
        lines = commit.strip().split("\n")
        if len(lines) < 2:
            continue

        # 提取 commit ID 和 message
        commit_id = lines[0].split()[1]
        commit_message = lines[1]

        # 提取变更文件列表
        files = []
        for line in lines[2:]:
            if re.match(r"^\d+\s+\d+\s+.+", line):
                files.append(line.split()[-1])

        # 根据 commit message 判断变更类型
        commit_type = "unknown"
        for t, keywords in type_keywords.items():
            if any(keyword in commit_message.lower() for keyword in keywords):
                commit_type = t
                break

        # 构造单条 commit 的 JSON 数据
        summary.append({
            "type": commit_type,
            "ID": commit_id,
            "files": files,
            "content": commit_message
        })

    # 写入 JSON 文件
    output_data = {"summary": summary}
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"Formatted commit log JSON has been written to {output_json_path}")
    return output_json_path

if __name__ == "__main__":
    llm_kwargs = tl.get_default_kwargs()
    commit_log_path = "/results/libuv_new\\libuv_log.txt"
    output_json_path = "/results/libuv_new\\libuv_log2.json"
    analyze_commit_log2(commit_log_path, llm_kwargs, output_json_path)