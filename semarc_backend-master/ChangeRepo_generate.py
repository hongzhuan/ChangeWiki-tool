import os
import json
import time
from crazy_utils_no_ui import request_gpt_model_in_new_thread_with_no_ui
from toolbox import write_history_to_file
from cmt_log_process.analyze_log import analyze_commit_log2
from uml_to_code_generation import tools as tl
from make_md_table import generate_md_tables_by_module
from commit_func import add_functions_and_write_new_json

def map_files_to_modules(commit_log_data, module_file_mapping):
    """
    将文件与模块映射到一起，更新 commit log 数据。
    """
    for commit in commit_log_data.get("summary", []):
        if "files" in commit:
            updated_files = []
            for file in commit["files"]:
                # 查找文件对应的模块
                module_name = None
                for module, files in module_file_mapping.items():
                    if file in files:
                        module_name = module
                        break
                # 更新文件信息，添加模块字段
                updated_files.append({"file": file, "module": module_name})
            # 更新 commit 的 files 字段
            commit["files"] = updated_files
    return commit_log_data

def read_module_file_mapping_from_nested_json(mapping_path):
    """
    从嵌套的 JSON 文件中读取模块与文件的映射关系。
    """
    with open(mapping_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    module_file_mapping = {}

    def parse_structure(structure, parent_name=""):
        for item in structure:
            if item["@type"] == "group":
                # 如果是 group，递归解析其 nested 部分
                group_name = item["name"]
                parse_structure(item["nested"], group_name)
            elif item["@type"] == "item":
                # 如果是 item，将文件添加到对应的模块
                file_name = item["name"]
                if parent_name not in module_file_mapping:
                    module_file_mapping[parent_name] = []
                module_file_mapping[parent_name].append(file_name)

    parse_structure(data["structure"])
    print(f"模块与文件映射关系已加载: {mapping_path}")
    return module_file_mapping

def read_input_files(version1_files, version2_files):
    """
    读取输入文件，包括版本1和版本2的模块/组件信息。
    """
    version1_data = {}
    version2_data = {}
    for file_path in version1_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            version1_data[os.path.basename(file_path)] = json.load(f)
    for file_path in version2_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            version2_data[os.path.basename(file_path)] = json.load(f)

    return version1_data, version2_data


def read_template(template_path):
    """
    读取报告模板内容。
    """
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    print(f"报告模板已加载: {template_path}")
    return template_content


def group_commits_by_module(commit_log_data):
    """
    按模块划分 commit log。
    如果某条 commit 的文件为空，则将其划分到所有模块；
    如果文件只涉及一个模块，则划分到该模块；
    如果文件涉及多个模块，则划分到所有涉及的模块。
    """
    module_commits = {}

    for commit in commit_log_data.get("summary", []):
        files = commit.get("files", [])
        if not files:
            # 如果文件列表为空，将 commit 分配到所有模块
            for module in module_commits.keys():
                module_commits[module].append(commit)
        else:
            involved_modules = set()
            for file_entry in files:
                module_name = file_entry.get("module")  # 从文件中获取模块名
                if module_name:
                    involved_modules.add(module_name)

            if not involved_modules:
                continue

            for module_name in involved_modules:
                if module_name not in module_commits:
                    module_commits[module_name] = []
                module_commits[module_name].append(commit)

    return module_commits

def generate_module_table_no_batch(module_name, commits, llm_kwargs, history, template_content):
    """
    为模块生成总结性的变更表格，一次性传递所有日志给大模型进行分析。
    """
    # 将所有 commit 的详细信息拼接成一个字符串
    commit_details = "\n".join(
        [f"- Commit ID: {commit.get('ID', 'N/A')}, 类型: {commit.get('type', 'N/A')}, 描述: {commit.get('content', 'N/A')}" 
         for commit in commits]
    )

    sys_prompt = (
        f"你是一个软件架构师，负责总结模块的关键变更点并生成表格。\n"
        # f"以下是报告模板，请确保生成的表格符合此模板的格式要求：\n\n"
        # f"{template_content}"
    )

    prompt = (
        f"以下是模块 {module_name} 的所有变更记录（共 {len(commits)} 条）：\n\n"
        f"{commit_details}\n\n"
        f"表格格式如下，请确保生成的表格符合此格式，表格必须包含五列：变更类型，变更内容，关键函数，相关文件，Commit ID，具体如下：\n\n"
        f"| 变更类型       | 变更内容       | 关键函数       | 相关文件       | Commit ID       |\n"
        f"| -------------- | -------------- | -------------- | -------------- | --------------- |\n"
        f"| （功能特性变更/非功能特性变更） | （填写变更内容，不要直接填写content内容，而是进行总结和概括） | （填写关键函数，可以记录json数据中的“message”字段提及的函数） | （填写相关文件，一个或多个） | （填写相关的 Commit ID，有可能不止一个） |\n\n"
        f"请根据以上格式生成表格，文字部分统一用中文，确保内容准确且完整，回答的内容只包含表格，不要有其余任何冗余的注释或文字说明。"
    )

    # 调用大模型生成表格
    table = request_gpt_model_in_new_thread_with_no_ui(
        inputs=prompt,
        inputs_show_user=f"生成模块 {module_name} 的总结性变更表格（一次性分析所有日志）",
        llm_kwargs=llm_kwargs,
        history=history,
        sys_prompt=sys_prompt
    )

    # 返回带模块名的表格
    # return f"#### **{module_name}**\n\n{table}"
    return table

# def generate_module_table(module_name, commits, llm_kwargs, history, template_content):
#     """
#     为模块生成总结性的变更表格，利用大模型分析和分组。
#     """
#     batch_size = 20  # 每组 20 条 commit
#     total_commits = len(commits)
#     final_table = ""  # 用于存储最终的表格内容

#     sys_prompt = (
#         f"你是一个软件架构师，负责总结模块的关键变更点并生成表格。\n"
#         f"以下是报告模板，请确保生成的表格符合此模板的格式要求：\n\n"
#         f"{template_content}"
#     )

#     for batch_start in range(0, total_commits, batch_size):
#         batch_commits = commits[batch_start:batch_start + batch_size]
#         commit_details = "\n".join(
#             [f"- Commit ID: {commit.get('ID', 'N/A')}, 类型: {commit.get('type', 'N/A')}, 描述: {commit.get('content', 'N/A')}" 
#              for commit in batch_commits]
#         )
#         prompt = (
#             f"以下是模块 {module_name} 的部分变更记录（第 {batch_start // batch_size + 1} 批次，共 {len(batch_commits)} 条）：\n\n"
#             f"{commit_details}\n\n"
#             f"以下是当前已生成的表格内容，请在此基础上结合新信息进行新增、完善或总结：\n\n"
#             f"{final_table if final_table else '（当前表格为空，请从头开始生成）'}\n\n"
#             f"表格格式如下，请确保生成的表格符合此格式：\n\n"
#             f"| 变更类型       | 变更内容       | 关键函数       | 相关文件       | Commit ID       |\n"
#             f"| -------------- | -------------- | -------------- | -------------- | --------------- |\n"
#             f"| （业务变更/非业务变更） | （填写变更内容，不要直接填写content内容，而是进行总结和概括） | （填写关键函数，可以记录json数据中的“message”字段提及的函数） | （填写相关文件，一个或多个） | （填写相关的 Commit ID，有可能不止一个） |\n\n"
#             f"请根据以上格式生成表格，文字部分统一用中文，确保内容准确且完整，回答的内容只包含迭代更新后的表格，不要有其余任何冗余的注释或文字说明。"
#         )
#         table = request_gpt_model_in_new_thread_with_no_ui(
#             inputs=prompt,
#             inputs_show_user=f"生成模块 {module_name} 的总结性变更表格（第 {batch_start // batch_size + 1} 批次）",
#             llm_kwargs=llm_kwargs,
#             history=history,
#             sys_prompt=sys_prompt
#         )
#         final_table = table

#     # 返回带模块名的表格
#     return f"#### **{module_name}**\n\n{final_table}"


def generate_module_summary(module_name, table_content, llm_kwargs, history, version1_module_sum, version1_component_sum, version1_cluster_component, version2_module_sum, version2_component_sum, version2_cluster_component, template_content):
    """
    为模块生成文字总结，包含版本1和版本2的上下文信息。
    """
    version1_prompt = (
        f"版本1的模块信息：\n{json.dumps(version1_module_sum, ensure_ascii=False, indent=4)}\n\n"
        f"版本1的组件信息：\n{json.dumps(version1_component_sum, ensure_ascii=False, indent=4)}\n\n"
        f"版本1的组件与模块映射关系：\n{json.dumps(version1_cluster_component, ensure_ascii=False, indent=4)}"
    )
    version2_prompt = (
        f"版本2的模块信息：\n{json.dumps(version2_module_sum, ensure_ascii=False, indent=4)}\n\n"
        f"版本2的组件信息：\n{json.dumps(version2_component_sum, ensure_ascii=False, indent=4)}\n\n"
        f"版本2的组件与模块映射关系：\n{json.dumps(version2_cluster_component, ensure_ascii=False, indent=4)}"
    )
    sys_prompt = (
        f"你是一个软件架构师，负责生成模块变更的文字总结。\n"
        f"以下是报告模板，请确保生成的文字总结符合此模板的格式要求：\n\n"
        f"{template_content}"
    )
    prompt = (
        f"以下是模块 {module_name} 的变更表格：\n\n"
        f"{table_content}\n\n"
        f"以下是两个版本的模块和组件信息：\n\n"
        f"{version1_prompt}\n\n{version2_prompt}\n\n"
        f"请基于以上内容填充模板生成该模块的文字总结。模板中的模块变更应为一段话，是对该模块变更的整体总结；模板中的功能特性变更总结和非功能特性变更总结部分，描述变更的主要内容和影响，以列表的形式呈现。回答时严格遵循模板相应部分的格式要求，除了报告内容不要回答其余任何冗余的信息"
    )
    summary = request_gpt_model_in_new_thread_with_no_ui(
        inputs=prompt,
        inputs_show_user=f"生成模块 {module_name} 的文字总结",
        llm_kwargs=llm_kwargs,
        history=history,
        sys_prompt=sys_prompt
    )
    return summary


def generate_component_summary(component_name, all_tables, all_summaries, llm_kwargs, history,
                              version1_module_sum, version1_component_sum, version1_cluster_component,
                              version2_module_sum, version2_component_sum, version2_cluster_component, template_content):
    """
    生成单个组件级别的总结，包含版本1和版本2的上下文信息。
    只聚焦于当前组件相关内容。
    """
    version1_prompt = (
        f"版本1的模块信息：\n{json.dumps(version1_module_sum, ensure_ascii=False, indent=4)}\n\n"
        f"版本1的组件信息：\n{json.dumps(version1_component_sum, ensure_ascii=False, indent=4)}\n\n"
        f"版本1的组件与模块映射关系：\n{json.dumps(version1_cluster_component, ensure_ascii=False, indent=4)}"
    )
    version2_prompt = (
        f"版本2的模块信息：\n{json.dumps(version2_module_sum, ensure_ascii=False, indent=4)}\n\n"
        f"版本2的组件信息：\n{json.dumps(version2_component_sum, ensure_ascii=False, indent=4)}\n\n"
        f"版本2的组件与模块映射关系：\n{json.dumps(version2_cluster_component, ensure_ascii=False, indent=4)}"
    )
    # 只筛选与该组件相关的模块表格和总结（假设组件与模块有映射关系）
    related_modules = []
    if component_name in version2_cluster_component:
        related_modules = version2_cluster_component[component_name]
    related_tables = [table for table in all_tables if any(m in table for m in related_modules)]
    related_summaries = [summary for summary in all_summaries if any(m in summary for m in related_modules)]

    sys_prompt = (
        f"你是一个软件架构师，负责生成组件级别的变更总结。\n"
        f"以下是报告模板，请确保生成的总结符合此模板的格式要求：\n\n"
        f"{template_content}"
    )
    prompt = (
        f"以下是该组件相关模块的变更表格和文字总结：\n\n"
        f"{''.join(related_tables)}\n\n"
        f"{''.join(related_summaries)}\n\n"
        f"以下是两个版本的模块和组件信息：\n\n"
        f"{version1_prompt}\n\n{version2_prompt}\n\n"
        f"请基于以上内容生成该组件的总结，描述主要变更内容和影响，以列表的形式呈现。"
    )
    summary = request_gpt_model_in_new_thread_with_no_ui(
        inputs=prompt,
        inputs_show_user=f"生成组件 {component_name} 的总结",
        llm_kwargs=llm_kwargs,
        history=history,
        sys_prompt=sys_prompt
    )
    return summary


def generate_conclusion(all_tables, all_summaries, component_summary, llm_kwargs, history, template_content):
    """
    生成综合结论，基于模块表格、模块总结和组件总结。
    """
    sys_prompt = (
        f"你是一个软件架构师，负责生成架构变更的综合结论。\n"
        f"以下是报告模板，请确保生成的综合结论符合此模板的格式要求：\n\n"
        f"{template_content}"
    )
    prompt = (
        f"以下是所有模块的变更表格和文字总结：\n\n"
        f"{''.join(all_tables)}\n\n"
        f"{''.join(all_summaries)}\n\n"
        f"以下是组件总结：\n\n"
        f"{component_summary}\n\n"
        f"请基于以上内容生成综合结论，描述整体变更的优先级、影响范围和后续行动建议，以列表的形式呈现。"
    )
    conclusion = request_gpt_model_in_new_thread_with_no_ui(
        inputs=prompt,
        inputs_show_user="生成综合结论",
        llm_kwargs=llm_kwargs,
        history=history,
        sys_prompt=sys_prompt
    )
    return conclusion


def assemble_full_report(all_tables, all_summaries, component_summary, conclusion, template_content):
    """
    组装完整的架构变更报告。
    """
    report = template_content.replace("{{module_changes}}", "\n\n".join(all_tables))
    report = report.replace("{{module_summaries}}", "\n\n".join(all_summaries))
    report = report.replace("{{component_summary}}", component_summary)
    report = report.replace("{{conclusion}}", conclusion)
    return report

def assemble_full_report_from_files(report_dir, template_content):
    """
    组装完整的架构变更报告，从各部分已保存的md文件读取内容。
    """
    # 读取模块表格和总结
    module_tables = []
    module_summaries = []
    for fname in os.listdir(report_dir):
        if fname.endswith("_report.md") and not fname.endswith("_component_report.md"):
            with open(os.path.join(report_dir, fname), 'r', encoding='utf-8') as f:
                content = f.read()
                # 表格和总结用 --- 分隔
                parts = content.split('---')
                if len(parts) >= 2:
                    module_tables.append(parts[0].strip())
                    module_summaries.append(parts[1].strip())
                else:
                    module_tables.append(content.strip())

    # 读取组件总结
    component_summaries = []
    for fname in os.listdir(report_dir):
        if fname.endswith("_component_report.md"):
            with open(os.path.join(report_dir, fname), 'r', encoding='utf-8') as f:
                component_summaries.append(f.read().strip())

    # 读取综合结论
    conclusion_path = os.path.join(report_dir, "conclusion.md")
    if os.path.exists(conclusion_path):
        with open(conclusion_path, 'r', encoding='utf-8') as f:
            conclusion = f.read().strip()
    else:
        conclusion = ""

    # 按模板组装
    report = template_content
    report = report.replace("{{module_changes}}", "\n\n".join(module_tables))
    report = report.replace("{{module_summaries}}", "\n\n".join(module_summaries))
    report = report.replace("{{component_changes}}", "\n\n".join(component_summaries))
    report = report.replace("{{conclusion}}", conclusion)
    return report


def format_final_report(all_tables, all_summaries, component_summary, conclusion, template_content):
    """
    格式化最终报告内容，确保表格在上方，文字总结在下方。
    """
    # 将表格部分组织在一起
    tables_section = "\n\n".join(all_tables)

    # 将文字总结部分组织在一起
    summaries_section = "\n\n".join(all_summaries)

    # 替换模板中的占位符
    report = template_content.replace("{{module_changes}}", tables_section)
    report = report.replace("{{module_summaries}}", summaries_section)
    report = report.replace("{{component_summary}}", component_summary)
    report = report.replace("{{conclusion}}", conclusion)

    return report


def generate_architecture_change_reports(project_name, v1, v2, commit_log_json_path, commit_log_module, recovered_result,code_change_dir):
    """
    生成架构变更报告的主函数接口。
    """
    start_time = time.time()

    v1=v1.replace("/", "")
    v2=v2.replace("/", "")
    
    # 结果文件路径
    recovered_module_path = os.path.join(recovered_result, f"{project_name}-{v2}",f"{project_name}-{v2}_NamedClusters.json")
    version1_files = [
        os.path.join(recovered_result,f"{project_name}-{v1}" ,f"{project_name}-{v1}_ModuleSum.json"),
        os.path.join(recovered_result,f"{project_name}-{v1}", f"{project_name}-{v1}_ComponentSum.json"),
        os.path.join(recovered_result,f"{project_name}-{v1}", f"{project_name}-{v1}_ClusterComponent.json")
    ]
    version2_files = [
        os.path.join(recovered_result,f"{project_name}-{v2}", f"{project_name}-{v2}_ModuleSum.json"),
        os.path.join(recovered_result, f"{project_name}-{v2}",f"{project_name}-{v2}_ComponentSum.json"),
        os.path.join(recovered_result, f"{project_name}-{v2}",f"{project_name}-{v2}_ClusterComponent.json")
    ]
    template_path = "D:\\Huawei\\new\\semarc_backend\\repo_template.md"
    module_template_path = "D:\\Huawei\\new\\semarc_backend\\module_repo_template.md"
    compoennt_template_path = "D:\\Huawei\\new\\semarc_backend\\component_repo_template.md"
    conclusion_template_path = "D:\\Huawei\\new\\semarc_backend\\conclusion_repo_template.md"

    commit_log_module_func_path=os.path.join(recovered_result, f"{project_name}-{v1}{v2}", f"{project_name}_log_module_func.json")

    # Step 1: 检查并加载 commit log 数据
    if os.path.exists(commit_log_module) and os.path.getsize(commit_log_module) > 0:
        print(f"文件 {commit_log_module} 已存在且不为空，跳过生成步骤。")
        with open(commit_log_module, 'r', encoding='utf-8') as f:
            commit_log_data = json.load(f)
    else:
        print("读取模块与文件的映射关系...")
        module_file_mapping = read_module_file_mapping_from_nested_json(recovered_module_path)
        print("读取 commit log 数据...")
        with open(commit_log_json_path, 'r', encoding='utf-8') as f:
            commit_log_data = json.load(f)
        print("将文件与模块映射到一起...")
        updated_commit_log_data = map_files_to_modules(commit_log_data, module_file_mapping)
        print("保存更新后的 commit log 数据...")
        with open(commit_log_module, 'w', encoding='utf-8') as f:
            json.dump(updated_commit_log_data, f, ensure_ascii=False, indent=4)
        commit_log_data = updated_commit_log_data
    add_functions_and_write_new_json(commit_log_module,code_change_dir, commit_log_module_func_path)

    # Step 2: 读取 LLM 参数
    llm_kwargs = tl.get_default_kwargs()

    # Step 3: 读取版本1和版本2的模块信息
    # 读取版本1的文件
    with open(version1_files[0], 'r', encoding='utf-8') as f:
        version1_module_sum = json.load(f)
    with open(version1_files[1], 'r', encoding='utf-8') as f:
        version1_component_sum = json.load(f)
    with open(version1_files[2], 'r', encoding='utf-8') as f:
        version1_cluster_component = json.load(f)

    # 读取版本2的文件
    with open(version2_files[0], 'r', encoding='utf-8') as f:
        version2_module_sum = json.load(f)
    with open(version2_files[1], 'r', encoding='utf-8') as f:
        version2_component_sum = json.load(f)
    with open(version2_files[2], 'r', encoding='utf-8') as f:
        version2_cluster_component = json.load(f)

    # Step 4: 读取报告模板,区分模块/组件独立报告和完整报告模板
    print("读取报告模板...")
    template_content = read_template(template_path)
    module_template_content = read_template(module_template_path)
    component_template_content = read_template(compoennt_template_path)
    conclusion_template_content = read_template(conclusion_template_path)

    # Step 5: 按模块划分 commit log
    print("按模块划分 commit log...")
    module_commits = group_commits_by_module(commit_log_data)

    # Step 6: 为每个模块生成表格
    print("为每个模块生成表格...")
    all_tables = []
    for module_name, commits in module_commits.items():
        # 使用最新的表格生成方法
        # 生成所有模块表格到临时目录
        temp_md_dir = os.path.join(recovered_result, f"{project_name}-{v1}{v2}", f"{project_name}_md_tables")
        os.makedirs(temp_md_dir, exist_ok=True)
        # 只生成一次所有表格
        if not all_tables:
            # 这里假设libuv_log_module_func.json已生成
            generate_md_tables_by_module(commit_log_module_func_path, temp_md_dir)
        # 读取当前模块的表格内容
        sanitized_module_name = str(module_name).replace("/", "_")
        module_md_path = os.path.join(temp_md_dir, f"{module_name if module_name != 'N/A' else 'unknown_module'}.md")
        if os.path.exists(module_md_path):
            with open(module_md_path, 'r', encoding='utf-8') as f:
                table_content = f.read()
        else:
            table_content = f"(无表格内容)"
        table_with_title = f"### {module_name} 模块变更\n\n{table_content}"
        all_tables.append(table_with_title)
        output_dir = os.path.join(recovered_result, f"{project_name}-{v1}{v2}")
        os.makedirs(output_dir, exist_ok=True)
        module_report_path = os.path.join(output_dir, f"{project_name}_{sanitized_module_name}_report.md")
        with open(module_report_path, 'w', encoding='utf-8') as f:
            f.write(table_content)
        print(f"模块表格已保存到: {module_report_path}")

    # Step 7: 为每个模块生成文字总结并保存
    print("为每个模块生成文字总结...")
    all_summaries = []
    for module_name, table_content in zip(module_commits.keys(), all_tables):
        summary_history = []
        summary = generate_module_summary(
            module_name, table_content, llm_kwargs, summary_history,
            version1_module_sum, version1_component_sum, version1_cluster_component,
            version2_module_sum, version2_component_sum, version2_cluster_component,
            module_template_content
        )
        summary_with_title = f"#### {module_name} 模块总结\n\n{summary}"
        all_summaries.append(summary_with_title)

        sanitized_module_name = str(module_name).replace("/", "_")
        module_report_path = os.path.join(recovered_result, f"{project_name}-{v1}{v2}", f"{project_name}_{sanitized_module_name}_report.md")
        with open(module_report_path, 'a', encoding='utf-8') as f:
            f.write("\n\n---\n\n")
            f.write(summary)
        print(f"模块总结已保存到: {module_report_path}")

    # Step 8: 生成组件总结
    print("生成组件总结...")
    all_component_summaries = []
    for component in version2_component_sum.get("summary", []):
        component_name = component.get("file")
        if not component_name:
            continue
        component_history = []
        component_summary = generate_component_summary(
            component_name, all_tables, all_summaries, llm_kwargs, component_history,
            version1_module_sum, version1_component_sum, version1_cluster_component,
            version2_module_sum, version2_component_sum, version2_cluster_component,
            component_template_content
        )
        component_summary_with_title = f"### {component_name} 组件总结\n\n{component_summary}"
        all_component_summaries.append(component_summary_with_title)

        sanitized_component_name = component_name.replace("/", "_")
        component_report_path = os.path.join(
            recovered_result, f"{project_name}-{v1}{v2}", f"{project_name}_{sanitized_component_name}_component_report.md"
        )
        with open(component_report_path, 'w', encoding='utf-8') as f:
            f.write(component_summary)
        print(f"组件总结已保存到: {component_report_path}")

    # Step 9: 生成综合结论
    print("生成综合结论...")
    conclusion_history = []
    conclusion = generate_conclusion(all_tables, all_summaries, "\n\n".join(all_component_summaries), llm_kwargs, conclusion_history, conclusion_template_content)
    write_history_to_file(["综合结论", conclusion])
    conclusion_path = os.path.join(
            recovered_result, f"{project_name}-{v1}{v2}", f"{project_name}_conclusion.md"
        )
    with open(conclusion_path, 'w', encoding='utf-8') as f:
        f.write(conclusion)
    print(f"综合结论已保存到: {conclusion_path}")

    # Step 10: 组装完整报告
    print("组装完整报告...")
    report = template_content
    report = report.replace("{{module_changes}}", "\n\n".join(all_tables))
    report = report.replace("{{module_summaries}}", "\n\n".join(all_summaries))
    report = report.replace("{{component_changes}}", "\n\n".join(all_component_summaries))
    report = report.replace("{{conclusion}}", conclusion)

    # Step 11: 保存完整报告
    output_path = os.path.join(recovered_result, f"{project_name}-{v1}{v2}", f"{project_name}_full_report.md")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"完整架构变更报告已保存到: {output_path}")

    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算运行时间
    print(f"Total execution time: {elapsed_time:.2f} seconds")  # 打印运行时间

if __name__ == "__main__":
    project_name = "libuv"
    v2="v1.48.0"
    v1="v1.44.2"
    commit_log_path = "D:\\Huawei\\new\\semarc_backend\\results\\libuv-v1.44.2v1.48.0\\libuv_log.txt"
    commit_log_json_path = "D:\\Huawei\\new\\semarc_backend\\results\\libuv-v1.44.2v1.48.0\\libuv_log.json"
    commit_log_module = "D:\\Huawei\\new\\semarc_backend\\results\\libuv-v1.44.2v1.48.0\\libuv_log_module.json"
    recovered_result = ".\\results"
    code_change_dir="D:\\Huawei\\new\\semarc_backend\\results\\libuv-v1.44.2v1.48.0\\code_changes\\libuv-c42e4a1b-2afed16f"

    # analyze_commit_log2(commit_log_path,commit_log_json_path)
    generate_architecture_change_reports(project_name, v1,v2,commit_log_json_path, commit_log_module, recovered_result,code_change_dir)
    #commit_log_json_path是已经存在的，commit_log_module是生成的