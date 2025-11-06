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
from algorithm.comparing_clusters import get_cluster_mapping,json2cluster_dict

def analysis_json(json_file, llm_kwargs, plugin_kwargs, history, system_prompt):

    max_token = model_info[llm_kwargs['llm_model']]['max_token']
    TOKEN_LIMIT_PER_FRAGMENT = max_token * 3 // 4
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            json_content = json.load(f)
    except Exception as e:
        raise RuntimeError(f'无法读取JSON文件: {json_file}，错误信息: {str(e)}')

    # 处理JSON文件中的每个模块（group）
    modules = json_content.get('structure', [])
    overall_summary = []
    for module in modules:
        module_name = module.get('name', 'Unknown Module')
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
            i_say = f'以下是一些文件的功能描述，请根据这些描述总结该模块的主要功能：```{fragment}```'
            i_say_show_user = f'正在总结模块 {module_name} 的第 {i+1}/{len(functionality_fragments)} 个片段。'

            gpt_say = request_gpt_model_in_new_thread_with_no_ui(
                inputs=i_say,
                inputs_show_user=i_say_show_user,
                llm_kwargs=llm_kwargs,
                history=[],
                sys_prompt="Please summarize the main functionality of the module and give it an appropriate name. The name should reference terms from the project directory, not include the project name and must not exceed three words.（模块名不能包含空格）"
            )

            history.extend([i_say_show_user, gpt_say])
            module_summaries.append(gpt_say)

        # 如果有多个片段，对模块进行综合总结并命名
        if len(functionality_fragments) > 1:
            combined_summaries = '\n'.join(module_summaries)
            i_say = f'Based on the above summaries, further summarize the main functionality of module {module_name} and give it an appropriate name in English. The name should reference terms from the project directory, not include the project name and must not exceed three words.Only respond with "Module Number: Module Name" and nothing else.（模块名不能包含空格）'
            i_say_show_user = f'正在综合总结模块 {module_name}。'

            gpt_say =request_gpt_model_in_new_thread_with_no_ui(
                inputs=i_say,
                inputs_show_user=i_say_show_user,
                llm_kwargs=llm_kwargs,
                history=history,
                sys_prompt="请总结模块的主要功能，并为其取一个合适的英文名称。"
            )

            history.extend([i_say_show_user, gpt_say])
            module_summary = gpt_say
        else:
            module_summary = module_summaries[0]

        i_say = f'根据以上的总结，将所有模块名和功能描述统一成md文件中的json块格式输出，格式是\'\'\'json{{"modules": [{{"no": 模块编号1,"name": 模块名1,"description": 模块1功能描述}}, {{"no": 模块编号2,"name": 模块名2,"description": 模块2功能描述}},....}}'
        i_say_show_user = f'正在综合模块名...'

        gpt_say =request_gpt_model_in_new_thread_with_no_ui(
            inputs=i_say,
            inputs_show_user=i_say_show_user,
            llm_kwargs=llm_kwargs,
            history=history,
            sys_prompt="请总结所有模块的名称，将他们和编号对应。"
        )
        history.extend([i_say_show_user, gpt_say])
        module_summary = gpt_say

        # 保存模块的总结和名称
        overall_summary.append({
            'module_name': module_name,
            'module_summary': module_summary
        })

    # 处理完所有模块后，将总结写入文件
    summary_output = '模块功能总结：\n'
    for module_info in overall_summary:
        summary_output += f"模块 {module_info['module_name']}:\n{module_info['module_summary']}\n\n"

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
        # group_no = int(group['name'])  # 获取组的编号
        group_no = group['name']  # 获取组的编号
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

def module_naming(result_dir,project_name,cluster_path,functionality_path):
    llm_kwargs = tl.get_default_kwargs()
    # cluster_path=sys.argv[2]
    # functionality_path=sys.argv[3]
    # folder_path=sys.argv[1

    merged_path='.\\cache\\merged.json'
    named_cluster_path= os.path.join(result_dir,project_name, f"{project_name}_NamedClusters.json")
    module_name_path = os.path.join(result_dir, project_name, 'cluster_result_named.json')
    cc_map = os.path.join(result_dir, project_name, f"{project_name}_cluster_component_mapping.json")
    cluster_component_path = os.path.join(result_dir, project_name, f"{project_name}_ClusterComponent.json")

    if check_file_exists_and_not_empty(merged_path) and check_file_exists_and_not_empty(named_cluster_path) and check_file_exists_and_not_empty(module_name_path):
        print("Find cache.")
        return named_cluster_path,cluster_component_path # 如果文件都存在且不为空，直接结束函数

    merge_functionality_with_clusters(cluster_path, functionality_path, merged_path)
    module_name_res=analysis_json(json_file=merged_path,llm_kwargs=llm_kwargs, plugin_kwargs={}, history=[], system_prompt="")
    md2json_name(module_name_res,module_name_path)
    deduplicate_module_names(module_name_path)
    mapping_module(cluster_path,module_name_path,named_cluster_path)
    replace_no_with_name(module_name_path,cc_map,cluster_component_path)
    return named_cluster_path,cluster_component_path

def merge_clusters_by_pair(cluster_path_v1, cluster_path_v2, cluster_id_v1, cluster_id_v2, func_path_v1, func_path_v2):
    """
    构造一个合并后的 JSON 文件，包含 v1 和 v2 中一对 cluster 的功能文件信息。
    返回生成的合并 JSON 路径。
    """
    import uuid
    from clusters_func import merge_functionality_with_clusters

    # 临时路径
    temp_output_path = f".\\cache\\merged_cluster_pair_{cluster_id_v1}_{cluster_id_v2}_{uuid.uuid4().hex[:6]}.json"

    # 读取聚类信息
    with open(cluster_path_v1, 'r', encoding='utf-8') as f1:
        clusters_v1 = json.load(f1)
    with open(cluster_path_v2, 'r', encoding='utf-8') as f2:
        clusters_v2 = json.load(f2)

    def extract_files(cluster_json, cluster_id):
        for group in cluster_json.get("structure", []):
            if str(group.get("name")) == str(cluster_id):
                return group.get("nested", [])
        return []

    # 提取两个簇下的文件项
    nested_v1 = extract_files(clusters_v1, cluster_id_v1)
    nested_v2 = extract_files(clusters_v2, cluster_id_v2)

    # 合并结构
    merged_structure = {
        "@type": "group",
        "name": f"{cluster_id_v1}-{cluster_id_v2}",
        "nested": nested_v1 + nested_v2
    }

    merged_json = {
        "structure": [merged_structure]
    }

    # 保存结构临时文件
    with open(temp_output_path, 'w', encoding='utf-8') as f:
        json.dump(merged_json, f, ensure_ascii=False, indent=4)

    # 调用功能合并模块
    merge_functionality_with_clusters(temp_output_path, [func_path_v1, func_path_v2], temp_output_path)

    return temp_output_path

def extract_cluster_subjson(cluster_path, cluster_id):
    """
    提取给定 cluster_path 中指定 cluster_id 的结构，包装成完整结构 JSON 并返回新文件路径。

    参数:
        cluster_path: 原始 cluster_result.json 文件路径
        cluster_id: 要提取的簇编号（整数或字符串）

    返回:
        保存了该 cluster 的新 JSON 文件路径
    """
    import uuid

    with open(cluster_path, 'r', encoding='utf-8') as f:
        cluster_data = json.load(f)

    matched_group = None
    for group in cluster_data.get('structure', []):
        if str(group.get('name')) == str(cluster_id):
            matched_group = group
            break

    if matched_group is None:
        raise ValueError(f"未找到 cluster ID 为 {cluster_id} 的结构")

    output = {
        "structure": [matched_group]
    }

    output_path = f".\\cache\\single_cluster_{cluster_id}_{uuid.uuid4().hex[:6]}.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

    return output_path


def module_naming_double_check(result_dir, project_v1, project_v2, cluster_path_v1, cluster_path_v2, func_path_v1, func_path_v2):
    import json
    import os
    from collections import defaultdict

    # 调用 module_naming 对两个版本进行模块命名
    named_cluster_path_v1, cluster_component_path_v1 = module_naming(result_dir, project_v1, cluster_path_v1, func_path_v1)
    named_cluster_path_v2, cluster_component_path_v2 = module_naming(result_dir, project_v2, cluster_path_v2, func_path_v2)

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
    # module_naming('D:\\SemArc_backend\\results','enre','D:\\SemArc_backend\\results\\enre\\cluster_result.json','D:\\SemArc_backend\\results\\enre\\enre_CodeSem.json')
    module_naming_double_check(
        'D:\\SemArc_backend\\results',
        'libuv_new-1.44.2',
        'libuv_new-1.48.0',
        'D:\\SemArc_backend\\results\\libuv-1.44.2\\cluster_result.json',
        'D:\\SemArc_backend\\results\\libuv-1.48.0\\cluster_result.json',
        'D:\\SemArc_backend\\results\\libuv-1.44.2\\libuv-1.44.2_CodeSem.json',
        'D:\\SemArc_backend\\results\\libuv-1.48.0\\libuv-1.48.0_CodeSem.json'
    )