from toolbox import write_history_to_file, promote_file_to_downloadzone
import glob
import os
import json
import re
import os, glob,copy,sys
from crazy_utils_no_ui import request_gpt_model_in_new_thread_with_no_ui
from uml_to_code_generation.toolbox_no_ui import promote_file_to_downloadzone
from uml_to_code_generation import tools as tl
from toolbox import write_history_to_file
from md2json import md2json

import shutil

def execute_parsing_and_analysis(txt_json, llm_kwargs, plugin_kwargs, history, system_prompt,knowledge=""):
    from pdf_fns.breakdown_txt import breakdown_text_to_satisfy_token_limit
    from request_llms.bridge_all import model_info
    overall_summary = []

    # Parse the SAP.txt file to extract architecture pattern descriptions
    file_path = '.\\SAP.txt'
    if not os.path.exists(file_path):
        raise RuntimeError(f'Cannot find SAP.txt file: {file_path}')

    with open(file_path, 'r', encoding='utf-8') as f:
        sap_content = f.read()

    # Split architecture patterns by double hashtags "##"
    architecture_patterns = re.split(r'\n##\s*', sap_content)
    architecture_patterns = [pattern.strip() for pattern in architecture_patterns if pattern.strip()]

    architecture_fragments = architecture_patterns  # Each pattern is treated as a separate fragment

    # Check and retrieve the JSON project folder
    if os.path.exists(txt_json):
        json_project_folder = txt_json
    else:
        if txt_json == "":
            txt_json = 'Empty input'
        raise RuntimeError(f"Cannot find or access the specified path: {txt_json}")

    # Retrieve the list of JSON files to process
    if txt_json.endswith('.json'):
        file_manifest = [txt_json]
    else:
        file_manifest = [f for f in glob.glob(f'{json_project_folder}/**/*.json', recursive=True)]

    # Check if any JSON files were found
    if len(file_manifest) == 0:
        raise RuntimeError(f"No JSON files found at {txt_json}")

    # Parse the JSON files to extract project functionality summaries
    for fp in file_manifest:
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                json_content = json.load(f)
        except Exception as e:
            raise RuntimeError(f'Failed to read JSON file: {fp}, Error: {str(e)}')

        summaries = json_content.get('summary', [])
        functionalities = [item.get('Functionality', '') for item in summaries if item.get('Functionality', '')]

        # Segment functionality descriptions to avoid exceeding token limits
        functionality_fragments = breakdown_text_to_satisfy_token_limit(
            txt='\n'.join(functionalities),
            limit=model_info[llm_kwargs['llm_model']]['max_token'] * 3 // 4,
            llm_model=llm_kwargs['llm_model']
        )

        summary_fragments = []
        total_fragments = len(functionality_fragments)
        for idx, fragment in enumerate(functionality_fragments, start=1):
            i_say = f'Here are some functionality descriptions of files. Please summarize the main functionalities of the project based on these descriptions: ```{fragment}```'
            gpt_say = request_gpt_model_in_new_thread_with_no_ui(
                inputs=i_say,
                inputs_show_user="Summarizing the main functionalities of the project...",
                llm_kwargs=llm_kwargs,
                history=[],
                sys_prompt="Summarize the main functionalities of the project."
            )
            summary_fragments.append(gpt_say)

        # Directly use the project functionality summaries provided by the GPT model without further summarization
        project_summary = '\n'.join(summary_fragments)

        overall_summary.append({
            'project_summary': project_summary
        })

    # Combine all architecture pattern descriptions for model context
    architecture_descriptions = '\n'.join(architecture_fragments)

    # First prompt: Identify the architecture type
    if knowledge:
        first_prompt = (
            f"Below are descriptions of known software architecture patterns:\n{architecture_descriptions}\n\n"
            f"Here is the domain knowledge for this project: {knowledge}\n\n"
            "Based on these descriptions, identify the only one best matched architecture pattern for this project. The response must contain only the architecture pattern (e.g., layered pattern) without any additional or redundant information (explanations or descriptions about the architecture pattern are considered redundant)!"
        )
    else:
        first_prompt = (
            f"Below are descriptions of known software architecture patterns:\n{architecture_descriptions}\n\n"
            "Based on these descriptions, identify the only one best matched architecture pattern for this project. The response must contain only the architecture pattern (e.g., layered pattern) without any additional or redundant information (explanations or descriptions about the architecture pattern are considered redundant)!"
        )

    i_say_1 = f"Identify the architecture type: ```{first_prompt}```"
    if knowledge:
        sys_prompt=f'Identify the best matched architecture pattern. Here is the domian knowledge for this project:{knowledge}'
    else:
        sys_prompt="Identify the best matched architecture pattern."

    gpt_response_1 = request_gpt_model_in_new_thread_with_no_ui(
        inputs=i_say_1,
        inputs_show_user="Identifying the best matched architecture pattern...",
        llm_kwargs=llm_kwargs,
        history=[],
        sys_prompt=sys_prompt
    )
    identified_pattern =gpt_response_1

        # Second prompt: Provide detailed analysis with reasoning
    second_prompt = (
        f"Below is the functionality summary of the project:\n" +
        "\n".join([item['project_summary'] for item in overall_summary]) +
        f"\n\nThe identified architecture pattern is: {gpt_response_1}\n\n"
        "Using the identified architecture pattern and the project information, analyze why this pattern is suitable for the project and provide reasoning."
    )

    i_say_2 = f"Analyze the architecture pattern: ```{second_prompt}```"
    gpt_response_2 = request_gpt_model_in_new_thread_with_no_ui(
        inputs=i_say_2,
        inputs_show_user="Analyzing the architecture pattern with reasoning...",
        llm_kwargs=llm_kwargs,
        history=[],
        sys_prompt="Analyze the architecture pattern with reasoning."
    )

    # Third prompt: Generate JSON output for components
    if knowledge:
        third_prompt = (
        f"The identified architecture pattern is: {gpt_response_2}.\n"
        f"The domain knowledge of this software is: {knowledge}.\n"
        f"Based on the only one best matched architecture pattern, create a JSON-formatted output describing the key components of the project.\n"
        "Each component should have three detailed indicators and each indicator should include 3-5 sentences: functionality characteristics, non-functional characteristics, and interactions with other components.\n"
        "The components must cover the entire project without overlapping.\n"
        "Use the following format:\n"
        "```\n"
        "{\n"
        "  \"architecture pattern\":... ,\n"
        "  \"components\": [\n"
        "    {\n"
        "      \"nested\": [\n"
        "        {\"@type\": \"indicator\", \"content\": \"...\"},\n"
        "        {\"@type\": \"indicator\", \"content\": \"...\"},\n"
        "        {\"@type\": \"indicator\", \"content\": \"...\"}\n"
        "      ],\n"
        "      \"@type\": \"component\",\n"
        "      \"name\": \"...\"\n"
        "    }\n"
        "  ]\n"
        "}\n"
        "```"
    )
    else:
        third_prompt = (
            f"The identified architecture pattern is: {gpt_response_2}.\n"
            f"Based on the only one best matched architecture pattern, create a JSON-formatted output describing the key components of the project.\n"
            "Each component should have three detailed indicators and each indicator should include 3-5 sentences: functionality characteristics, non-functional characteristics, and interactions with other components.\n"
            "The components must cover the entire project without overlapping.\n"
            "Use the following format:\n"
            "```\n"
            "{\n"
            "  \"architecture pattern\":... ,\n"
            "  \"components\": [\n"
            "    {\n"
            "      \"nested\": [\n"
            "        {\"@type\": \"indicator\", \"content\": \"...\"},\n"
            "        {\"@type\": \"indicator\", \"content\": \"...\"},\n"
            "        {\"@type\": \"indicator\", \"content\": \"...\"}\n"
            "      ],\n"
            "      \"@type\": \"component\",\n"
            "      \"name\": \"...\"\n"
            "    }\n"
            "  ]\n"
            "}\n"
            "```"
        )
    i_say_3 = f"Generate JSON output for components: ```{third_prompt}```"
    gpt_response_3 = request_gpt_model_in_new_thread_with_no_ui(
        inputs=i_say_3,
        inputs_show_user="Generating a JSON-formatted component description...",
        llm_kwargs=llm_kwargs,
        history=[],
        sys_prompt="Generate a JSON-formatted component description."
    )

    # Return combined analysis results and JSON output
    analysis_result = f"Identified Architecture Pattern: {gpt_response_1}\n\nDetailed Analysis:\n{gpt_response_2}\n\nComponent JSON:\n{gpt_response_3}"
    res = write_history_to_file([gpt_response_3])
    promote_file_to_downloadzone(res)
    print("架构模式分析完成")
    return res,identified_pattern

def format_checking(json_file_path, preset_file_path=None, 
                    txt_json=None, llm_kwargs=None, plugin_kwargs=None, history=None, system_prompt="", knowledge="", 
                    max_generation_round=3):
    """
    检查并修复大模型生成的架构json结构，若连续多次（最大9轮）都无法修复，则用本地预置文件覆盖。
    """
    def _validate_and_repair(data):
        error = ""
        if not isinstance(data, dict):
            error = "数据根节点不是字典类型"
            return False, data, error

        # 检查 architecture_pattern 或其别名
        key_arch = next((k for k in data if k in ['architecture_pattern', 'architecture pattern']), None)
        if not key_arch:
            error = "缺少architecture_pattern字段"
            return False, data, error

        #内容非空校验
        arch_value = data.get(key_arch)
        if arch_value is None or (isinstance(arch_value, str) and arch_value.strip() == ""):
            error = "architecture_pattern内容为空"
            return False, data, error
        if isinstance(arch_value, str) and arch_value.strip().lower() == "unknown":
            error = "architecture_pattern不能为Unknown"
            return False, data, error

        # 检查 components 是否为列表
        if "components" not in data or not isinstance(data["components"], list):
            error = "缺少components字段或其不是列表类型"
            return False, data, error

        all_pass = True
        for idx, comp in enumerate(data["components"]):
            if not isinstance(comp, dict):
                error += f"第{idx+1}个component不是dict类型；"
                all_pass = False
                continue
            if "name" not in comp or not isinstance(comp["name"], str) or comp["name"].strip() == "":
                error += f"第{idx+1}个component缺少name字段或不是非空字符串；"
                all_pass = False
            if "nested" not in comp or not isinstance(comp["nested"], list) or len(comp["nested"]) != 3:
                error += f"第{idx+1}个component的nested字段错误；"
                all_pass = False
                continue
            for j, indicator in enumerate(comp["nested"]):
                if not isinstance(indicator, dict) or indicator.get("@type") != "indicator":
                    error += f"第{idx+1}个component的第{j+1}个indicator格式错误；"
                    all_pass = False
                content = indicator.get("content")
                if isinstance(content, list):
                    indicator["content"] = " ".join(map(str, content))
                    error += f"自动合并第{idx+1}个component的第{j+1}个indicator的content列表为字符串；"
                elif not isinstance(content, str):
                    indicator["content"] = str(content)
                    error += f"自动转换第{idx+1}个component的第{j+1}个indicator的content为字符串；"

        return all_pass, data, error

    def _load_json(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None

    def _dump_json(data, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    round_gen = 0
    while round_gen < max_generation_round:
        for fix_try in range(2):
            data = _load_json(json_file_path)
            if data is None:
                break
            is_valid, data, error = _validate_and_repair(data)
            if is_valid:
                _dump_json(data, json_file_path)
                print(f"格式检查通过（第{round_gen+1}轮，第{fix_try+1}次修复）")
                return True
            else:
                _dump_json(data, json_file_path)
                print(f"第{round_gen+1}轮，第{fix_try+1}次修复尝试，错误信息：{error}")
        round_gen += 1
        print(f"第{round_gen}轮修复未通过，重新调用大模型生成...")
        res,identified_pattern=execute_parsing_and_analysis(
            txt_json=txt_json,
            llm_kwargs=llm_kwargs,
            plugin_kwargs=plugin_kwargs,
            history=history,
            system_prompt=system_prompt,
            knowledge=knowledge
        )
        md2json(res, json_file_path)

    if preset_file_path and os.path.exists(preset_file_path):
        shutil.copy(preset_file_path, json_file_path)
        print(f"多次失败，已使用预置文件覆盖: {json_file_path}")
    else:
        print("多次失败，且未提供预置文件，结果可能不合规。")
    return False


def get_arch_semantic():
    folder_path = sys.argv[1]
    project_name = os.path.basename(folder_path)
    llm_kwargs = tl.get_default_kwargs()
    json_file_path = f"{project_name}_ArchSem.json"
    preset_file_path = ".\\arch_pattern_layered.json.json"  # 预置文件地址，建议设置为您自己的本地标准文件

    # 执行大模型生成
    res,identified_pattern = execute_parsing_and_analysis(
        txt_json=folder_path,
        llm_kwargs=llm_kwargs,
        plugin_kwargs={},
        history=[],
        system_prompt=""
    )
    md2json(res, json_file_path)

    format_checking(
            json_file_path=json_file_path,
            preset_file_path=preset_file_path,
            txt_json=folder_path,
            llm_kwargs=llm_kwargs,
            plugin_kwargs={},
            history=[],
            system_prompt="",
            max_generation_round=3
        )

    print(f"架构语义信息已保存到文件: {json_file_path}")

if __name__ == "__main__":
    get_arch_semantic()