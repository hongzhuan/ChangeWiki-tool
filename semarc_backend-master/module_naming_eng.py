from toolbox import update_ui
from toolbox import CatchException, report_exception
from toolbox import write_history_to_file, promote_file_to_downloadzone
from crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
import glob,os,sys
from clusters_func import merge_functionality_with_clusters
from uml_to_code_generation import tools as tl
import json
from pdf_fns.breakdown_txt import breakdown_text_to_satisfy_token_limit
from request_llms.bridge_all import model_info
from crazy_utils_no_ui import request_gpt_model_multi_threads_with_no_ui_and_high_efficiency, \
    request_gpt_model_in_new_thread_with_no_ui, generate_manifest_and_project_folder
from md2json import md2json_name

import shutil

def analysis_json(json_file, llm_kwargs, plugin_kwargs, history, system_prompt, module_name_path, knowledge=""): #将LLM的回答结果直接写入json文件
    max_token = model_info[llm_kwargs['llm_model']]['max_token']
    TOKEN_LIMIT_PER_FRAGMENT = max_token * 3 // 4
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            json_content = json.load(f)
    except Exception as e:
        raise RuntimeError(f'Unable to read JSON file: {json_file}, error: {str(e)}')

    result_modules = []

    # 处理JSON文件中的每个模块（group）
    modules = json_content.get('structure', [])
    overall_summary = []
    for module in modules:
        module_no = module.get('name', 'Unknown Module')
        nested_items = module.get('nested', [])
        module_type = module.get('@type', '')

        # 收集模块中所有文件的功能描述
        functionalities = []

        def extract_functionalities(items, functionalities_list):
            for item in items:
                if item.get('@type') == 'item':
                    functionality = item.get('Functionality', '')
                    if functionality:
                        functionalities_list.append(functionality)
                elif item.get('@type') == 'group':
                    # 递归处理嵌套的group
                    extract_functionalities(item.get('nested', []), functionalities_list)

        extract_functionalities(nested_items, functionalities)

        # 分段处理功能描述，避免超过token限制
        functionality_fragments = breakdown_text_to_satisfy_token_limit(
            txt='\n'.join(functionalities),
            limit=TOKEN_LIMIT_PER_FRAGMENT,
            llm_model=llm_kwargs['llm_model']
        )

        module_summaries = []
        for i, fragment in enumerate(functionality_fragments):
            # i_say = f'以下是一些文件的功能描述，请根据这些描述总结该模块的主要功能：```{fragment}```'
            i_say = f'The following are some functionality descriptions of files. Please summarize the main functionality of this module based on these descriptions: ```{fragment}```'
            # i_say_show_user = f'正在总结模块 {module_name} 的第 {i+1}/{len(functionality_fragments)} 个片段。'
            i_say_show_user = f'Summarizing fragment {i+1}/{len(functionality_fragments)} of module {module_no}.'

            gpt_say = request_gpt_model_in_new_thread_with_no_ui(
                inputs=i_say,
                inputs_show_user=i_say_show_user,
                llm_kwargs=llm_kwargs,
                history=[],
                # sys_prompt="请总结模块的主要功能，并根据功能为模块取一个合适的名称。参考项目目录名称，不超过三个词"
                sys_prompt=""
            )

            history.extend([i_say_show_user, gpt_say])
            module_summaries.append(gpt_say)

        # 如果有多个片段，对模块进行综合总结并命名
        if len(functionality_fragments) > 1:
            module_summary = '\n'.join(module_summaries)
        else:
            module_summary = module_summaries[0]
            # i_say = f'根据以上的总结，进一步总结模块 {module_name} 的主要功能，并为其取一个合适的名称，模块名用英文，回答时只回答 模块编号:模块名，切勿回答其他任何信息。'
            # if knowledge is None:
            #     i_say = f'Based on the above summaries, further summarize the main functionality of module {module_no} and give it an appropriate name in English. The name should reference terms from the project directory, not include the project name, not include the project name and avoid including some words like test or testing, and must not exceed three words.Only respond with "Module Number: Module Name" and nothing else.名称不能包含空格、斜杠、横线和括号等特殊符号，只能包含下划线。避免出现test或testing等词语。'
            # else:
            #     i_say = f'基于以上总结，进一步总结模块 {module_no} 的主要功能，并为其提供一个合适的英文名称。要求：1.不能包含项目名称，避免和其他模块重名或相似；2.长度不得超过三个单词。3.名称不能包含空格、斜杠、横线和括号等特殊符号，只能包含下划线。4.名称应参考项目目录中的术语和该软件系统的领域知识。领域知识可以参考README文件，请全面、仔细地阅读整个README文件，重点关注与软件系统功能、特性、架构模式或架构风格等相关的内容。这个项目的README文件内容是：{knowledge}。'
        if knowledge is None:
            i_say = f'模块 {module_no} 的主要功能是{module_summary}，为其提供一个合适的英文名称。要求：1.不能包含项目名称，避免和其他模块重名或相似；2.长度不得超过三个单词，避免出现test或testing等词语。3.名称不能包含空格、斜杠、横线和括号等特殊符号，只能包含下划线。4.名称应参考项目目录中的术语和该软件系统的领域知识。注意：回答中不要包含任何冗余内容，包括描述。必须严格按照以下输出格式，将模块名包裹在尖括号中:<此处填写模块名>'
        else:
            i_say = f'模块 {module_no} 的主要功能是{module_summary}，为其提供一个合适的英文名称。要求：1.不能包含项目名称，避免和其他模块重名或相似；2.长度不得超过三个单词，避免出现test或testing等词语。3.名称不能包含空格、斜杠、横线和括号等特殊符号，只能包含下划线。4.名称应参考项目目录中的术语和该软件系统的领域知识。领域知识可以参考README文件，请全面、仔细地阅读整个README文件，重点关注与软件系统功能、特性、架构模式或架构风格等相关的内容。这个项目的README文件内容是：{knowledge}。注意：回答中不要包含任何冗余内容，包括描述。必须严格按照以下输出格式，将模块名包裹在尖括号中:<此处填写模块名>'
        # i_say_show_user = f'正在综合总结模块 {module_name}。'
        i_say_show_user = f'Further summarizing module {module_no}.'

        # gpt_say = request_gpt_model_in_new_thread_with_no_ui(
        #     inputs=i_say,
        #     inputs_show_user=i_say_show_user,
        #     llm_kwargs=llm_kwargs,
        #     history=history,
        #     # sys_prompt="请总结模块的主要功能，并为其取一个合适的名称。"
        #     sys_prompt="Please summarize the main functionality of the module and give it an appropriate name."
        # )
        # history.extend([i_say_show_user, gpt_say])
        # import re
        # # 去除开头非字母数字字符
        # processed_name = re.sub(r'^[^a-zA-Z0-9]+', '', gpt_say)
        # # 替换除字母、数字和下划线以外的所有字符为下划线，并删除中文等非英文字符
        # processed_name = re.sub(r'[^\w\s]', '_', processed_name)  # 替换特殊符号为下划线
        # processed_name = re.sub(r'[\u4e00-\u9fff]', '', processed_name)  # 删除中文字符
        # processed_name = re.sub(r'\s+', '_', processed_name)  # 将空格替换为下划线
        
        import re
        import logging
        logger = logging.getLogger(__name__)
        # for attempt in range(3):  # 最多重试三次
        gpt_say = request_gpt_model_in_new_thread_with_no_ui(
            inputs=i_say,
            inputs_show_user=i_say_show_user,
            llm_kwargs=llm_kwargs,
            history=history,
            sys_prompt="注意：回答中不要包含任何冗余内容，包括描述。必须严格按照以下输出格式，将模块名包裹在尖括号中:<此处填写模块名>"
        )
        processed_name = re.search(r"<\s*([A-Za-z_]+)\s*>", gpt_say)
        if processed_name:  #匹配到指定输出格式
            # 处理生成的名称
            processed_name=processed_name.group(1).strip()
            # 进一步处理名称
            processed_name = re.sub(r'^[^a-zA-Z0-9]+', '', processed_name)  # 去除开头非字母数字字符
            processed_name = re.sub(r'[^\w\s]', '_', processed_name)  # 替换特殊符号为下划线
            processed_name = re.sub(r'[\u4e00-\u9fff]', '', processed_name)  # 删除中文字符
            processed_name = re.sub(r'\s+', '_', processed_name)  # 将空格替换为下划线
            # # 检查是否符合要求
            # if "local_message" in processed_name and len(processed_name) >= 50:
            #     # 如果三次重试后仍不符合要求，直接使用 module_no
            #     logger.info(f"生成的模块名不符合要求，使用默认模块编号 {module_no}")
            #     processed_name=module_no
            # else:
            #     logger.info(f"模块编号 {module_no}生成的模块名是：{processed_name}")
        else:
            # 如果没有找到 <name> 标签中的内容，尝试匹配第一对单引号中的内容
            single_quote_pattern = r"`(.*?)`"
            single_quote_match = re.search(single_quote_pattern, gpt_say)

            if single_quote_match:
                processed_name = single_quote_match.group(1).strip()
                # 进一步处理名称
                processed_name = re.sub(r'^[^a-zA-Z0-9]+', '', processed_name)  # 去除开头非字母数字字符
                processed_name = re.sub(r'[^\w\s]', '_', processed_name)  # 替换特殊符号为下划线
                processed_name = re.sub(r'[\u4e00-\u9fff]', '', processed_name)  # 删除中文字符
                processed_name = re.sub(r'\s+', '_', processed_name)  # 将空格替换为下划线
            elif len(gpt_say) <= 20:    # 如果回答很多字，且没有匹配到指定格式，则尝试直接使用回答内容
                processed_name = re.sub(r'^[^a-zA-Z0-9]+', '', gpt_say)  # 去除开头非字母数字字符
                processed_name = re.sub(r'[^\w\s]', '_', processed_name)  # 替换特殊符号为下划线
                processed_name = re.sub(r'[\u4e00-\u9fff]', '', processed_name)  # 删除中文字符
                processed_name = re.sub(r'\s+', '_', processed_name)  # 将空格替换为下划线
            else:   # 如果没有匹配到指定格式，直接使用 module_no
                logger.warning(f"模块编号 {module_no}生成的模块名不符合要求，使用默认模块编号 {module_no}")
                processed_name = module_no

        # 直接填充到 json 结构
        result_modules.append({
            "no": int(module_no),                  # 模块编号或模块名称（视实际需要而定，通常为编号）
            "name": processed_name,           # 处理后的模块名
            "description": module_summary # 模块功能综合描述
        })

        # i_say = f'根据以上的总结，将所有模块名和功能描述统一成md文件中的json块格式输出，格式是\'\'\'json{{"modules": [{{"no": 模块编号1,"name": 模块名1,"description": 模块1功能描述}}, {{"no": 模块编号2,"name": 模块名2,"description": 模块2功能描述}},....}}'
        # i_say = f'Based on the above summaries, unify all module names and functionality descriptions into a JSON block format in an md file. The format is: ```json{{"modules": [{{"no": Module Number 1, "name": Module Name 1, "description": Module 1 Functionality Description}}, {{"no": Module Number 2, "name": Module Name 2, "description": Module 2 Functionality Description}}, ....]}}```. The Module Number should be th integer and the Module Name should be a string.'
    #     i_say = f'Based on the above summaries, unify only this module name and functionality descriptions into a JSON block format in an md file. The format is: ```json{{"modules": [{{"no": (number of this module), "name": (name of this module), "description":  (functionality description of this module)}}]}}```. The Module Number should be th integer and the Module Name should be a string.'
    #     # i_say_show_user = f'正在综合模块名...'
    #     i_say_show_user = f'Unifying module names...'

    #     gpt_say = request_gpt_model_in_new_thread_with_no_ui(
    #         inputs=i_say,
    #         inputs_show_user=i_say_show_user,
    #         llm_kwargs=llm_kwargs,
    #         history=history,
    #         # sys_prompt="请总结所有模块的名称，将他们和编号对应。"
    #         sys_prompt="Please summarize the module name and associate them with its numbers."
    #     )
    #     history.extend([i_say_show_user, gpt_say])
    #     module_summary = gpt_say

    #     # 保存模块的总结和名称
    #     overall_summary.append({
    #         'module_no': module_no,
    #         'module_summary': module_summary
    #     })

    # # 处理完所有模块后，将总结写入文件
    # # summary_output = '模块功能总结：\n'
    # summary_output = 'Module Functionality Summary:\n'
    # for module_info in overall_summary:
    #     summary_output += f"Module {module_info['module_name']}:\n{module_info['module_summary']}\n\n"
    # 汇总成目标结构并写入指定文件
    final_result = {"modules": result_modules}
    with open(module_name_path, 'w', encoding='utf-8') as f:
        json.dump(final_result, f, ensure_ascii=False, indent=4)

    print(f"模块命名结果已写入： {module_name_path}")

    # 将总结结果写入历史记录并提供下载
    res = write_history_to_file(history)
    return res

def analysis_json_dict(json_file, llm_kwargs, plugin_kwargs, history, system_prompt, module_name_path, knowledge=""): #将LLM的回答结果直接写入json文件
    max_token = model_info[llm_kwargs['llm_model']]['max_token']
    TOKEN_LIMIT_PER_FRAGMENT = max_token * 3 // 4
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            json_content = json.load(f)
    except Exception as e:
        raise RuntimeError(f'Unable to read JSON file: {json_file}, error: {str(e)}')

    result_modules = []

    # 处理JSON文件中的每个模块（group）
    modules = json_content.get('structure', [])
    overall_summary = []
    # 给模块新的编号
    new_no=0

    for module in modules:
        module_no = module.get('name', 'Unknown Module')
        nested_items = module.get('nested', [])
        module_type = module.get('@type', '')

        # 收集模块中所有文件的功能描述
        functionalities = []

        def extract_functionalities(items, functionalities_list):
            for item in items:
                if item.get('@type') == 'item':
                    functionality = item.get('Functionality', '')
                    if functionality:
                        functionalities_list.append(functionality)
                elif item.get('@type') == 'group':
                    # 递归处理嵌套的group
                    extract_functionalities(item.get('nested', []), functionalities_list)

        extract_functionalities(nested_items, functionalities)

        # 分段处理功能描述，避免超过token限制
        functionality_fragments = breakdown_text_to_satisfy_token_limit(
            txt='\n'.join(functionalities),
            limit=TOKEN_LIMIT_PER_FRAGMENT,
            llm_model=llm_kwargs['llm_model']
        )

        module_summaries = []
        for i, fragment in enumerate(functionality_fragments):
            i_say = f'以下是一些文件的功能描述，请根据这些描述总结该模块的主要功能： ```{fragment}```'
            i_say_show_user = f'正在总结模块 {module_no} 的第 {i+1}/{len(functionality_fragments)} 个片段。'

            gpt_say = request_gpt_model_in_new_thread_with_no_ui(
                inputs=i_say,
                inputs_show_user=i_say_show_user,
                llm_kwargs=llm_kwargs,
                history=[],
                sys_prompt=""
            )

            history.extend([i_say_show_user, gpt_say])
            module_summaries.append(gpt_say)

        # 如果有多个片段，对模块进行综合总结并命名
        if len(functionality_fragments) > 1:
            module_summary = '\n'.join(module_summaries)
        else:
            module_summary = module_summaries[0]

        processed_name = module_no

        # 直接填充到 json 结构
        result_modules.append({
            "no": new_no,                  # 模块编号或模块名称（视实际需要而定，通常为编号）
            "name": processed_name,           # 处理后的模块名
            "description": module_summary # 模块功能综合描述
        })
        new_no += 1
    final_result = {"modules": result_modules}
    with open(module_name_path, 'w', encoding='utf-8') as f:
        json.dump(final_result, f, ensure_ascii=False, indent=4)

    print(f"模块命名结果已写入： {module_name_path}")

    # 将总结结果写入历史记录并提供下载
    res = write_history_to_file(history)
    return res

def mapping_module(cluster_file,module_names,output_file):
    with open(cluster_file, 'r', encoding='utf-8') as cf:
        clusters = json.load(cf)

    # 读取第二个 JSON 文件
    with open(module_names, 'r', encoding='utf-8') as mn:
        names = json.load(mn)

    # 创建一个字典，将模块编号映射到模块名称
    module_mapping = {module['no']: module['name'] for module in names['modules']}

    # 遍历第一个文件的结构，替换 group 的 name 字段为模块名称
    for group in clusters['structure']:
        group_no = int(group['name'])  # 获取组的编号
        # group_no = group['name']  # 获取组的编号
        if module_mapping.get(group_no):
            group['name'] = module_mapping.get(group_no)
        else:
            group['name'] = group_no

    # 将修改后的数据保存到新的 JSON 文件
    with open(output_file, 'w', encoding='utf-8') as f_out:
        json.dump(clusters, f_out, ensure_ascii=False, indent=4)


def replace_no_with_name(cluster_result_path, cc_map, output_path):
    # 读取 cluster_result_named.json 文件
    with open(cluster_result_path, 'r', encoding='utf-8') as f:
        cluster_data = json.load(f)

    # 创建一个映射字典
    no_to_name = {module['no']: module['name'] for module in cluster_data['modules']}

    # 读取 enre_cluster_component_mapping.json 文件
    with open(cc_map, 'r', encoding='utf-8') as f:
        map_data = json.load(f)

    # 检查 enre_data 是否包含 'structure' 键
    if 'structure' not in map_data:
        print("错误: 'structure' 键不存在于 enre_cluster_component_mapping.json 文件中")
        print("文件内容:", map_data)
    else:
        # 遍历 'structure' 中的每个 'component'
        for component in map_data['structure']:
            # 遍历 'nested' 数组中的每个 'cluster'
            for cluster in component['nested']:
                no = cluster.get('name')  # 获取 No. 字段的值
                if no in no_to_name:
                    # 用对应的 name 替换 No. 字段
                    cluster['name'] = no_to_name[no]  # 替换为 name

        # 将修改后的数据写入一个新文件
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(map_data, f, ensure_ascii=False, indent=4)

        print(f"替换完成，结果已写入 {output_path}")

def check_file_exists_and_not_empty(file_path):
    return os.path.exists(file_path) and os.path.getsize(file_path) > 0

def deduplicate_module_names(module_name_path):
    """
    去重 module_name_path 文件中的模块，确保每个 no 只保留一条记录。
    同时将模块名中的空格替换为下划线 "_"
    """
    with open(module_name_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 使用字典去重，键为模块编号 (no)
    unique_modules = {}
    for module in data['modules']:
        no = module['no']
        if no not in unique_modules:
            # 替换模块名中的空格为下划线

            module['name'] = module['name'].replace(" ", "_")

            unique_modules[no] = module

    # 将去重后的模块列表写回文件
    deduplicated_data = {'modules': list(unique_modules.values())}
    with open(module_name_path, 'w', encoding='utf-8') as f:
        json.dump(deduplicated_data, f, ensure_ascii=False, indent=4)

    print(f"去重完成，结果已写入 {module_name_path}")

def module_naming(result_dir,project_name,cluster_path,functionality_path,knowledge=None):
    llm_kwargs = tl.get_default_kwargs()
    # cluster_path=sys.argv[2]
    # functionality_path=sys.argv[3]
    # folder_path=sys.argv[1

    merged_path='.\\cache\\merged.json'
    named_cluster_path= os.path.join(result_dir,project_name, f"{project_name}_NamedClusters.json")
    module_name_path = os.path.join(result_dir, project_name, 'cluster_result_named.json')
    cc_map = os.path.join(result_dir, project_name, f"{project_name}_cluster_component_mapping.json")
    cluster_component_path = os.path.join(result_dir, project_name, f"{project_name}_ClusterComponent.json")

    if check_file_exists_and_not_empty(merged_path) and check_file_exists_and_not_empty(named_cluster_path) and check_file_exists_and_not_empty(module_name_path) and check_file_exists_and_not_empty(cc_map) and check_file_exists_and_not_empty(cluster_component_path):
        print("Find cache.")
        return named_cluster_path,cluster_component_path # 如果文件都存在且不为空，直接结束函数

    merge_functionality_with_clusters(cluster_path, functionality_path, merged_path)
    module_name_res=analysis_json(json_file=merged_path,llm_kwargs=llm_kwargs, plugin_kwargs={}, history=[], system_prompt="",module_name_path=module_name_path,knowledge=knowledge)
    # md2json_name(module_name_res,module_name_path)
    deduplicate_module_names(module_name_path)
    # if not check_file_exists_and_not_empty(cc_map):
    mapping_module(cluster_path,module_name_path,named_cluster_path)
    replace_no_with_name(module_name_path,cc_map,cluster_component_path)
    return named_cluster_path,cluster_component_path

def module_naming_dict(result_dir,project_name,cluster_path,functionality_path,knowledge=None):
    llm_kwargs = tl.get_default_kwargs()
    # cluster_path=sys.argv[2]
    # functionality_path=sys.argv[3]
    # folder_path=sys.argv[1

    merged_path='.\\cache\\merged.json'
    named_cluster_path= os.path.join(result_dir,project_name, f"{project_name}_NamedClusters.json")
    module_name_path = os.path.join(result_dir, project_name, 'cluster_result_named.json')
    cc_map = os.path.join(result_dir, project_name, f"{project_name}_cluster_component_mapping.json")
    cluster_component_path = os.path.join(result_dir, project_name, f"{project_name}_ClusterComponent.json")

    if check_file_exists_and_not_empty(merged_path) and check_file_exists_and_not_empty(named_cluster_path) and check_file_exists_and_not_empty(module_name_path) and check_file_exists_and_not_empty(cc_map) and check_file_exists_and_not_empty(cluster_component_path):
        print("Find cache.")
        return named_cluster_path,cluster_component_path # 如果文件都存在且不为空，直接结束函数

    merge_functionality_with_clusters(cluster_path, functionality_path, merged_path)
    analysis_json_dict(json_file=merged_path,llm_kwargs=llm_kwargs, plugin_kwargs={}, history=[], system_prompt="",module_name_path=module_name_path,knowledge=knowledge)
    # mapping_module(cluster_path,module_name_path,named_cluster_path)
    shutil.copyfile(cluster_path, named_cluster_path)
    replace_no_with_name(module_name_path,cc_map,cluster_component_path)
    return named_cluster_path,cluster_component_path

def module_naming_double_check(named_cluster_path_v1, cluster_component_path_v1,named_cluster_path_v2, cluster_component_path_v2):
    import json
    import os
    from collections import defaultdict

    # 调用 module_naming 对两个版本进行模块命名
    # named_cluster_path_v1, cluster_component_path_v1 = module_naming(result_dir, project_v1, cluster_path_v1, func_path_v1)
    # named_cluster_path_v2, cluster_component_path_v2 = module_naming(result_dir, project_v2, cluster_path_v2, func_path_v2)

    # 读取 named_cluster_path 文件
    with open(named_cluster_path_v1, 'r', encoding='utf-8') as f1:
        clusters_v1 = json.load(f1)
    with open(named_cluster_path_v2, 'r', encoding='utf-8') as f2:
        clusters_v2 = json.load(f2)

    # 提取簇的文件集合
    def extract_cluster_files(cluster_data):
        cluster_files = defaultdict(set)
        for group in cluster_data.get('structure', []):
            cluster_id = group['name']
            files = {item['name'] for item in group.get('nested', []) if item.get('@type') == 'item'}
            cluster_files[cluster_id].update(files)
        return cluster_files

    cluster_files_v1 = extract_cluster_files(clusters_v1)
    cluster_files_v2 = extract_cluster_files(clusters_v2)

    # 构建候选匹配项列表：[(v2_id, v1_id, overlap_count)]
    candidate_matches = []
    for cluster_id_v2, files_v2 in cluster_files_v2.items():
        for cluster_id_v1, files_v1 in cluster_files_v1.items():
            overlap = len(files_v1 & files_v2)
            if overlap >= len(files_v2) / 2:  # 重合度超过一半
                candidate_matches.append((cluster_id_v2, cluster_id_v1, overlap))

    # 匹配：按照 overlap 降序，确保唯一匹配（贪心策略）
    candidate_matches.sort(key=lambda x: -x[2])  # 按 overlap 倒序排序
    used_v1 = set()
    used_v2 = set()
    matched_clusters = {}

    for cluster_id_v2, cluster_id_v1, _ in candidate_matches:
        if cluster_id_v2 not in used_v2 and cluster_id_v1 not in used_v1:
            matched_clusters[cluster_id_v1] = cluster_id_v2  # 键为 cluster_id_v1，值为 cluster_id_v2
            used_v2.add(cluster_id_v2)
            used_v1.add(cluster_id_v1)

    # 打印匹配到的簇数量
    print(f"\n匹配到的簇数量：{len(matched_clusters)}")

    # 更新 v1 的簇名称
    for group in clusters_v1.get('structure', []):
        cluster_id_v1 = group['name']
        if cluster_id_v1 in matched_clusters:
            group['name'] = matched_clusters[cluster_id_v1]

    # 写回更新后的 named_cluster_path_v1 文件
    with open(named_cluster_path_v1, 'w', encoding='utf-8') as f1:
        json.dump(clusters_v1, f1, ensure_ascii=False, indent=4)

    # 同步更新 cluster_component_path_v1 文件
    with open(cluster_component_path_v1, 'r', encoding='utf-8') as f:
        cluster_component_data = json.load(f)

    for component in cluster_component_data.get('structure', []):
        for cluster in component.get('nested', []):
            cluster_id_v1 = cluster.get('name')
            if cluster_id_v1 in matched_clusters:
                cluster['name'] = matched_clusters[cluster_id_v1]

    with open(cluster_component_path_v1, 'w', encoding='utf-8') as f:
        json.dump(cluster_component_data, f, ensure_ascii=False, indent=4)

    # 打印两个版本的模块名
    print("\n版本1的模块名：")
    for group in clusters_v1.get('structure', []):
        print(group['name'])

    print("\n版本2的模块名：")
    for group in clusters_v2.get('structure', []):
        print(group['name'])

    print("簇匹配完成，并已更新 named_cluster_path_v1 和 cluster_component_path_v1 文件。")


if __name__ == "__main__":
    ############################## <测试用> ##################################
    module_naming('.\\results','curve-v0.2.0-beta','.\\results\\curve-v0.2.0-beta\\cluster_result.json','.\\results\\curve-v0.2.0-beta\\curve-v0.2.0-beta_CodeSem.json')