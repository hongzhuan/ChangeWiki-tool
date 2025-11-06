import json
import sys
import logging
import shutil
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin

# from llm.change_semantic_generate import AnalysisInput,SemanticChangeAnalyzer

import utils.utils
from database.auth import register_user, login_user  # ← 新增
from database.history import get_history, add_history
from database.user_profile import get_user, update_user
from architecture_change.plantuml_add_color import update_plantuml_colors
from llm.change_semantic_concurrent_generate import AnalysisInput, SemanticChangeAnalyzer
from uml_to_code_generation import tools as tl
from architecture_change.component_cluster_add_color import component_cluster_add_color
from architecture_change.replace_plantuml_color_from_graphIDfunc import \
    replace_plantuml_color_from_graphIDfunc_component_cluster
from md2json import md2json_sum, md2json
from arch_pattern_analysis import execute_parsing_and_analysis
from semantic_analysis import code_semantic_analysis, get_semantic
from cluster_project import cluster_project
from module_naming_eng import module_naming, module_naming_double_check,module_naming_dict
from merge_final_json import merge_json_files
from graph_json import graph_json
from graph_add_function_json import merge_functionality_with_clusters, convert_component_to_sum, convert_module_to_sum
from architecture_change.a2a import a2a
from architecture_change.a2a_backup import a2a_update
from architecture_change.json2rsf import json_to_rsf
from architecture_change.file_change_info import file_change
from architecture_change.architecture_change_update_json import update_json
from architecture_change.convert_json_to_plantuml import convert_json_to_plantuml
from architecture_change.get_before_after_code import get_code_diff
from gitClone.clone_repo_with_retry import clone_repo_with_retry
import os
import subprocess
import tempfile
from architecture_change.mapping_module_file_change_count import combine_method
import shutil
from architecture_change.compare_plantuml_diff import compare_plantuml_json_versions_diff
from architecture_change.mapping_module_file_change_count import combine_method_add_file_numbers_info
from flask_socketio import SocketIO, emit
import time
import threading
import architecture_change.generate_mermaid as gm
from algorithm.comparing_clusters import get_cluster_mapping
from ChangeRepo_generate import generate_architecture_change_reports
from ChangeRepo_generate import analyze_commit_log2
import json

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import stat
import architecture_change.generate_mermaid as gm
import utils.utils
from architecture_change.component_cluster_add_color import component_cluster_add_color

from database.auth import register_user, login_user  # ← 新增
from database.history import get_history, add_history
from database.user_profile import get_user, update_user

from llm.change_semantic_concurrent_generate import AnalysisInput, SemanticChangeAnalyzer
from uml_to_code_generation import tools as tl
from md2json import md2json_sum, md2json
from arch_pattern_analysis import execute_parsing_and_analysis
from semantic_analysis import code_semantic_analysis, get_semantic
from cluster_project import cluster_project
from module_naming_eng import module_naming
from merge_final_json import merge_json_files
from graph_json import graph_json
from graph_add_function_json import merge_functionality_with_clusters, convert_component_to_sum, convert_module_to_sum
from architecture_change.a2a import a2a
from architecture_change.a2a_backup import a2a_update
from architecture_change.json2rsf import json_to_rsf
from architecture_change.file_change_info import file_change
from architecture_change.architecture_change_update_json import update_json
from architecture_change.convert_json_to_plantuml import convert_json_to_plantuml
from architecture_change.merge_Graph_Entities_json_to_Whole_reverse_tree_layer import \
    merge_Graph_Entities_json_to_Whole_reverse_tree_layer
import os
import subprocess
import tempfile
from architecture_change.mapping_module_file_change_count import combine_method
import shutil
from architecture_change.compare_plantuml_diff import compare_plantuml_json_versions_diff
from architecture_change.mapping_module_file_change_count import combine_method_add_file_numbers_info
from flask_socketio import SocketIO, emit
import time
import threading
from algorithm.comparing_clusters import get_cluster_mapping
from ChangeRepo_generate import generate_architecture_change_reports
from ChangeRepo_generate import analyze_commit_log2
from pymongo import MongoClient
import os
import json

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import stat
import architecture_change.generate_mermaid as gm
import utils.utils
from architecture_change.component_cluster_add_color import component_cluster_add_color

from database.contents import \
    MAX_DOCUMENT_SIZE  # MAX_DOCUMENT_SIZE = 15*1024*1024 :contentReference[oaicite:0]{index=0}
from database.db import fs
from bson.objectid import ObjectId
from database.db import users_col, analysis_records_col, analysis_contents_col
from database.auth import register_user, login_user
from database.history import get_history, add_history, get_history_by_id
from database.user_profile import get_user, update_user
from database.contents import get_content_by_path, save_contents

from llm.change_semantic_concurrent_generate import AnalysisInput, SemanticChangeAnalyzer
from uml_to_code_generation import tools as tl
from md2json import md2json_sum, md2json
from arch_pattern_analysis import execute_parsing_and_analysis
from semantic_analysis import code_semantic_analysis, get_semantic
from cluster_project import cluster_project
from module_naming_eng import module_naming
from merge_final_json import merge_json_files
from graph_json import graph_json
from graph_add_function_json import merge_functionality_with_clusters, convert_component_to_sum, convert_module_to_sum
from architecture_change.a2a import a2a
from architecture_change.a2a_backup import a2a_update
from architecture_change.json2rsf import json_to_rsf
from architecture_change.file_change_info import file_change
from architecture_change.architecture_change_update_json import update_json
from architecture_change.convert_json_to_plantuml import convert_json_to_plantuml
import os
import subprocess
import tempfile
from architecture_change.mapping_module_file_change_count import combine_method
import shutil
from architecture_change.compare_plantuml_diff import compare_plantuml_json_versions_diff
from architecture_change.mapping_module_file_change_count import combine_method_add_file_numbers_info
from flask_socketio import SocketIO, emit
import time
import threading
from algorithm.comparing_clusters import get_cluster_mapping
from ChangeRepo_generate import generate_architecture_change_reports
from ChangeRepo_generate import analyze_commit_log2
from pymongo import MongoClient
import os

# 从环境变量获取 MongoDB 配置（否则使用默认值）
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'semarc_db')

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # 允许跨域
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True,
     methods=["GET", "POST", "PUT", "DELETE"])  # 允许跨域请求

# 确保results目录存在，路径基于app.py文件所在目录
result_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
os.makedirs(result_dir, exist_ok=True)
whole_project_path = ''
count = 0
rsf_version1 = ''
rsf_version2 = ''
version1_path = ''
version2_path = ''
global_repo_url = ''
clone_url_no_version = ''
version1_tag = ''
version2_tag = ''
whole_project_name = ''
local_project_name = 'SemArc_backend'
analysis_project_language = ''
repo_clone_local_path = ''
code_changes_root_path = ''
log_path = os.path.join(result_dir, 'run.log')
log_file = open(log_path, 'w', encoding='utf-8')
sys.stdout = log_file
sys.stderr = log_file
# 配置日志记录器
# log_path = os.path.join(result_dir, 'run.log')
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler(log_path, encoding='utf-8'),  # 写入日志文件
#         logging.StreamHandler()  # 输出到终端
#     ]
# )

# 示例：替换原来的 `sys.stdout` 和 `sys.stderr` 重定向
logging.info("日志系统已初始化，日志将同时输出到终端和文件。")

# 关键字映射：自动转换为超链接
keyword_links = {
    "数据分析": "page_data_analysis.md",
    "人工智能": "page_ai.md",
    "机器学习": "page_ml.md"
}

tasks = [
    {"id": 1, "name": "版本1的架构逆向", "progress": 0, "children": [
        {"id": 11, "name": "静态代码依赖解析", "progress": 0},
        {"id": 12, "name": "代码语义生成", "progress": 0},
        {"id": 13, "name": "架构语义生成", "progress": 0}
    ]},
    {"id": 2, "name": "版本2的架构逆向", "progress": 0, "children": [
        {"id": 15, "name": "静态代码依赖解析", "progress": 0},
        {"id": 14, "name": "代码语义生成", "progress": 0},
        {"id": 16, "name": "架构语义生成", "progress": 0}
    ]},
    {"id": 3, "name": "变更分析", "progress": 0, "children": [
        {"id": 17, "name": "结构变更分析", "progress": 0},
        {"id": 18, "name": "提交历史分析", "progress": 0},
        {"id": 19, "name": "代码实体变更", "progress": 0}
    ]},
]


def calculate_parent_progress():
    """更新父任务的进度 = 子任务进度的平均值"""
    for task in tasks:
        if "children" in task:
            child_progress = [subtask["progress"] for subtask in task["children"]]
            task["progress"] = int(sum(child_progress) / len(child_progress))  # 计算平均进度


def update_progress():
    """模拟任务执行并逐步更新进度"""
    for _ in range(10):
        time.sleep(1)  # 模拟执行时间
        for task in tasks:
            if "children" in task:
                for subtask in task["children"]:
                    subtask["progress"] = min(subtask["progress"] + 15, 100)  # 子任务先完成
            else:
                task["progress"] = min(task["progress"] + 10, 100)  # 独立任务

        calculate_parent_progress()  # 计算父任务进度
        socketio.emit("progress_update", {"tasks": tasks})  # 发送进度更新

    socketio.emit("progress_complete", {"message": "所有任务执行完成！"})


@app.route("/api/register", methods=["POST"])
def api_register():
    return register_user()


@app.route("/api/login", methods=["POST"])
def api_login():
    return login_user()


@app.route("/api/history/<username>", methods=["GET"])
# @app.route("/api/history", methods=["POST"])
# @cross_origin(origins="*", methods=["POST"])
def api_history(username):
    # data = request.json
    # username = data.get("username")
    return get_history(username)


@app.route("/api/history", methods=["POST"])
def api_add_history():
    return add_history()


@app.route("/api/user/<username>", methods=["GET"])
@cross_origin(origins="*", methods=["GET"])
def api_get_user(username):
    return get_user(username)


@app.route("/api/user/<username>", methods=["PUT"])
@cross_origin(origins="*", methods=["PUT"])
def api_update_user(username):
    return update_user(username)


@app.route("/api/historyContents/<record_id>", methods=["GET"])
def api_history_by_id(record_id):
    return get_history_by_id(record_id)


@app.route("/api/save_contents", methods=["POST"])
def api_save_contents():
    """
    前端 POST { analysisId: "<id>" }
    后端根据 analysis_records 中的 projectName/version 标签
    调用 save_contents 把三个子文件夹写进 analysis_contents。
    """
    data = request.get_json(silent=True) or {}
    aid = data.get("analysisId")
    if not aid:
        return jsonify({"error": "缺少 analysisId"}), 400

    rec = analysis_records_col.find_one(
        {"_id": ObjectId(aid)},
        {"projectName": 1, "version1": 1, "version2": 1}
    )
    if not rec:
        return jsonify({"error": "记录不存在"}), 404

    project = rec["projectName"]
    v1 = rec["version1"]
    v2 = rec["version2"]

    # 这里取全局 result_dir
    base_results = result_dir  # e.g. os.path.join(os.getcwd(), "results")

    # 只遍历这三条子目录
    folders = [
        f"{project}-{v1}",
        f"{project}-{v2}",
        f"{project}-{v1}{v2}"
    ]
    # 针对每个子目录，都把它写入 db
    for sub in folders:
        full = os.path.join(base_results, sub)
        if os.path.isdir(full):
            save_contents(aid, full)

    return jsonify({"status": "ok"}), 200


@app.route("/start")
def start_task():
    """启动任务"""
    socketio.start_background_task(target=update_progress)
    return {"message": "任务已启动"}


def process_markdown(content):
    """将关键字转换为超链接"""
    for keyword, link in keyword_links.items():
        content = content.replace(keyword, f"[{keyword}]({link})")
    return content


@app.route("/get_markdown_architecture_change_report", methods=["POST"])
def get_architecture_change_report():
    # 解析请求参数
    data = request.get_json(silent=True) or {}
    analysis_id = data.get("analysisId")
    if not analysis_id:
        return jsonify({"error": "缺少 analysisId"}), 400

    # 查 analysis_records，取出 projectName、version1、version2
    rec = analysis_records_col.find_one(
        {"_id": ObjectId(analysis_id)},
        {"projectName": 1, "version1": 1, "version2": 1, "analysisFolder": 1}
    )
    if not rec:
        return jsonify({"error": "记录不存在"}), 404

    project_name = rec["projectName"]
    v1 = rec["version1"]
    v2 = rec["version2"]
    # 按约定拼接
    analysis_folder = f"{project_name}-{v1}{v2}"

    # 拼出相对路径，与 save_contents 存入的 Path 一一对应
    rel_path = f"{analysis_folder}\\{project_name}_full_report.md"

    print(rel_path)
    print("开始从数据库中获取内容")

    # 从 MongoDB 取内容
    content = get_content_by_path(analysis_id, rel_path)
    if content is None:
        print("Markdown 文件不存在")
        return jsonify({"error": "Markdown 文件不存在"}), 404

    # 返回给前端
    print("获取架构变更报告成功")
    return jsonify({"content": content}), 200


@app.route("/get_markdown", methods=["POST"])
def get_markdown():
    data = request.get_json(silent=True) or {}
    analysis_id = data.get("analysisId")
    if not analysis_id:
        return jsonify({"error": "缺少 analysisId"}), 400

    # 从数据库查记录
    rec = analysis_records_col.find_one(
        {"_id": ObjectId(analysis_id)},
        {"projectName": 1, "version1": 1, "version2": 1, "code_changes_root_path": 1}
    )
    if not rec:
        return jsonify({"error": "记录不存在"}), 404

    project_name = rec["projectName"]
    v1 = rec["version1"]
    v2 = rec["version2"]
    code_changes_root = rec["code_changes_root_path"]
    code_changes_root = os.path.basename(code_changes_root)

    # 拼接文件路径基本路径
    analysis_folder = f"{project_name}-{v1}{v2}"

    raw_label = data.get("label")
    # 如果是字符串类型，进行 replace 操作；如果是数字，直接转为字符串
    if isinstance(raw_label, str):
        label = raw_label.replace("/", "_")
    else:
        label = str(raw_label)  # 数字类型直接转为字符串

    category = data.get("category")
    node = data.get("node_allInfo")

    # 拼接 analysis_folder 生成相对路径 rel_path
    if category == 'cluster':
        rel_path = f"{analysis_folder}\\{project_name}_{label}_report.md"
    elif category == 'component':
        rel_path = f"{analysis_folder}\\{project_name}_{label}_component_report.md"
    elif category == 'file':
        file_name = label.replace("_", "----")
        rel_path = (
            f"{analysis_folder}\\code_changes\\"
            f"{code_changes_root}\\{file_name}\\semantic.txt"
        )
    elif category == 'Function':
        parent_Name = node.get("parentName", "")

        # 拼接 entities_changes_info_json_root 的路径
        entities_changes_info_json_root = (
            f"{analysis_folder}\\code_changes\\"
            f"{code_changes_root}\\entities_changes_info.json"
        )

        before_code, after_code = get_code_diff(label, parent_Name, entities_changes_info_json_root, analysis_id)

        parent_Name1 = parent_Name.replace("/", "----")
        label_name1 = os.path.basename(node.get('entity_path', '').rstrip('\\/'))

        function_semantic_file = (
            f'{analysis_folder}\\code_changes\\'
            f'{code_changes_root}\\{parent_Name1}\\{label_name1}\\semantic.txt'
        )

        # 从 MongoDB 读取内容并返回给前端
        content = get_content_by_path(analysis_id, function_semantic_file)
        if content is None:
            return jsonify({"error": " Function Markdown 文件不存在"}), 404

        return jsonify({"content": content, "before_code": before_code, "after_code": after_code}), 200

    else:
        return jsonify({"error": "未知的 category"}), 400

    # 从 MongoDB 读取内容并返回给前端
    logging.info(f"rel_path: {rel_path}")
    logging.info(f"category: {category}")
    content = get_content_by_path(analysis_id, rel_path)
    if content is None:
        return jsonify({"error": "Markdown 文件不存在"}), 404

    return jsonify({"content": content}), 200


@app.route("/get_markdown_architecture_version_summary_report", methods=["POST"])
@cross_origin(origins="*", methods=["POST"])
def get_architecture_version_summary_report():
    # 解析请求参数
    data = request.get_json(silent=True) or {}
    analysis_id = data.get("analysisId")
    if not analysis_id:
        return jsonify({"error": "缺少 analysisId"}), 400

    # 从 analysis_records 集合中查出对应记录
    rec = analysis_records_col.find_one(
        {"_id": ObjectId(analysis_id)},
        {"projectName": 1, "version1": 1, "version2": 1, "analysisFolder": 1}
    )
    if not rec:
        return jsonify({"error": "记录不存在"}), 404

    project_name = rec["projectName"]
    v1 = rec["version1"]
    v2 = rec["version2"]
    # 原有 analysisFolder 字段可能保存了不含前缀的目录名，这里直接用带 results/ 前缀的新版拼法
    analysis_folder = f"{project_name}-{v1}{v2}"

    # 拼出与 save_contents 时一致的相对路径
    rel_path = f"{analysis_folder}\\{project_name}_conclusion.md"

    logging.info(f"rel_path: {rel_path}")

    # 调用 get_content_by_path 从 analysis_contents 集合中取出 content
    content = get_content_by_path(analysis_id, rel_path)
    if content is None:
        return jsonify({"error": "Markdown 文件不存在"}), 404

    # 返回给前端
    return jsonify({"content": content}), 200


@app.route('/get_markdown_by_key')
def get_markdown_by_key():
    key = request.args.get('key')
    # file_path = os.path.join(BASE_MD_PATH, f"{key}.md")
    file_path = "D:\\SemArc_backend\\architecture_change\\un_run.md"
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({"content": content})
    else:
        return jsonify({"content": f"🔍 未找到与 '{key}' 对应的文档"}), 404


@app.route("/api/generate_plantuml", methods=["POST"])
def get_plantuml_data():
    print("Received GET request at /api/plantuml")
    global version1_path
    global version2_path
    global version1_tag
    global version2_tag
    version1_modify_tag = version1_tag.replace("/", "")
    version2_modify_tag = version2_tag.replace("/", "")
    print("/api/plantuml中version1_path:")
    print(version1_path)
    print("/api/plantuml中version2_path:")
    print(version2_path)
    input_version1_json_to_plantuml = f'{version1_path}_ClusterComponent.json'
    output_path_version1_plantuml_json_data = f'{version1_path}_Plantuml_json_data.json'
    input_version2_json_to_plantuml = f'{version2_path}_ClusterComponent.json'
    output_path_version2_plantuml_json_data = f'{version2_path}_Plantuml_json_data.json'
    component2_cluster2_add_color = os.path.join(result_dir, f'{whole_project_name}-{version2_modify_tag}',
                                                 f'{whole_project_name}-{version2_modify_tag}_GraphIDFunc_modify_add_component_cluster_color.json')
    component1_cluster1_add_color = os.path.join(result_dir, f'{whole_project_name}-{version1_modify_tag}',
                                                 f'{whole_project_name}-{version1_modify_tag}_GraphIDFunc_modify_add_component_cluster_color.json')

    convert_json_to_plantuml(input_version1_json_to_plantuml, output_path_version1_plantuml_json_data)
    convert_json_to_plantuml(input_version2_json_to_plantuml, output_path_version2_plantuml_json_data)
    update_plantuml_colors(output_path_version1_plantuml_json_data, component1_cluster1_add_color,
                           output_path_version1_plantuml_json_data)
    update_plantuml_colors(output_path_version2_plantuml_json_data, component2_cluster2_add_color,
                           output_path_version2_plantuml_json_data)
    architecture_change_plantuml = compare_plantuml_json_versions_diff(output_path_version1_plantuml_json_data,
                                                                       output_path_version2_plantuml_json_data)

    plantuml_data_json = os.path.join(result_dir, f'{whole_project_name}-{version1_modify_tag}{version2_modify_tag}',
                                      f'{whole_project_name}_plantuml_data.json')
    # 在plantuml_data_json中添加一个字段，architecture_name: 值为 f"{whole_project_name}架构变更"
    architecture_change_plantuml['architecture_name'] = f"{whole_project_name}_architecture_change"

    # 修改architecture_change_plantuml中components字段下elements中各Item的color 使用component1_cluster1_add_color和component2_cluster2_add_color中structure的item为cluster的color
    # with open(component1_cluster1_add_color, 'r', encoding='utf-8') as f:
    #     component1_cluster1_add_color_data = json.load(f)
    # with open(component2_cluster2_add_color, 'r', encoding='utf-8') as f:
    #     component2_cluster2_add_color_data = json.load(f)
    # for component in architecture_change_plantuml['components']:

    with open(plantuml_data_json, 'w', encoding='utf-8') as f:
        json.dump(architecture_change_plantuml, f, ensure_ascii=False, indent=4)
    generate_mermaid = gm.json_to_mermaid(architecture_change_plantuml)
    # 将生成的Mermaid json文档保存到文件
    mermaid_file_path = os.path.join(result_dir, f'{whole_project_name}-{version1_modify_tag}{version2_modify_tag}',
                                     f'{whole_project_name}_architecture_change_mermaid.mmd')
    open(mermaid_file_path, 'w', encoding='utf-8').write(generate_mermaid)
    print("generate_mermaid")
    print(generate_mermaid)
    # return {"architecture_data":architecture_change_plantuml}
    return {"mermaid_data": generate_mermaid}


@app.route("/api/get_plantuml", methods=["POST"])
def get_plantuml():
    data = request.get_json(silent=True) or {}
    analysis_id = data.get("analysisId")
    if not analysis_id:
        return {"error": "analysisId is required"}, 400

    # 先获取一下 project_name/version1_tag/version2_tag，用来拼出保存时的 Path
    rec = analysis_records_col.find_one({"_id": ObjectId(analysis_id)})
    if not rec:
        logging.info("记录不存在")
        return {"error": "记录不存在"}, 404

    projectName = rec["projectName"]
    v1 = rec["version1"]
    v2 = rec["version2"]
    rel_path = f"{projectName}-{v1}{v2}\\{projectName}_architecture_change_mermaid.mmd"

    content = get_content_by_path(analysis_id, rel_path)
    if content is None:
        logging.info(f"rel_path路径：{rel_path}")
        logging.info("Mermaid 文件内容未找到")
        return {"error": "Mermaid 文件内容未找到"}, 404

    return {"mermaid_data": content}


@app.route('/compare_architecture_change', methods=['POST'])
def architecture_change():
    global rsf_version1
    global rsf_version2
    global version1_path
    global version2_path
    global version1_tag
    global version2_tag
    global global_repo_url
    global code_changes_root_path
    print("compare_architecture_change中version1_path:")
    # eg. D:\backend\semarc_backend\results\jianshi-v1.0\jianshi-v1.0
    print(version1_path)
    print("compare_architecture_change中rsf_version1:")
    # eg. D:\backend\semarc_backend\results\jianshi-v1.0\jianshi-v1.0_rsf.rsf
    print(rsf_version1)
    print("compare_architecture_change中version2_path:")
    # eg. D:\backend\semarc_backend\results\jianshi-v2.0\jianshi-v2.0
    print(version2_path)
    print("compare_architecture_change中rsf_version2:")
    #eg. D:\backend\semarc_backend\results\jianshi-v2.0\jianshi-v2.0_rsf.rsf
    print(rsf_version2)
    version1_project_path = ''
    version2_project_path = ''
    version1_modify_tag = version1_tag.replace("/", "")
    version2_modify_tag = version2_tag.replace("/", "")
    if rsf_version1 is not '' and rsf_version2 is not '':
        version1_version2_a2a_mapping_weight_path = f'{version1_path}_{version1_modify_tag}_{version2_modify_tag}_a2a_mapping_weight.txt'
        # res, a2a_value, change_total=a2a(rsf_version1,rsf_version2)

        res, a2a_value, change_total = a2a_update(rsf_version1, rsf_version2, version1_version2_a2a_mapping_weight_path)
        # print("version1_tag",version1_tag)
        # print("version2_tag",version2_tag)
        # print("global_repo_url",global_repo_url)
        a2a_tableInfo_path = f'{version1_path}_{version1_modify_tag}_{version2_modify_tag}_a2a_mapping_weight_table.json'
        a2a_tableInfo_json = combine_method(global_repo_url, version1_tag, version2_tag,
                                            f'{version1_path}_{version1_modify_tag}_{version1_modify_tag}_file_change_count.json',
                                            rsf_version1, rsf_version2, version1_version2_a2a_mapping_weight_path,
                                            a2a_tableInfo_path)

        added, removed, moved, added_files, removed_files, moved_files, file_unit_operation_change = file_change(
            rsf_version1, rsf_version2, res, f'{version1_path}_cluster_contain_file_info.json',
            f'{version1_path}_file_unit_operation_change.json')

        a2a_tableInfo_json_add_fileInfo = combine_method_add_file_numbers_info(a2a_tableInfo_json,
                                                                               f'{version1_path}_cluster_contain_file_info.json')
        # input_version1_file = f'{version1_project_path}_GraphIDFunc.json'
        input_version1_file = f'{version1_path}_GraphIDFunc.json'
        # output_version1_file = f'{version1_project_path}_version1_change_Files.json
        output_version1_file = f'{version1_path}_GraphIDFunc_modify_add_color.json'
        component1_cluster1_add_color = f'{version1_path}_GraphIDFunc_modify_add_component_cluster_color.json'
        architecture1_change_json = update_json(input_version1_file, output_version1_file, added_files, removed_files,
                                                moved_files)
        print("architecture1_change_json")
        print(architecture1_change_json)
        input_version2_file = f'{version2_path}_GraphIDFunc.json'
        output_version2_file = f'{version2_path}_GraphIDFunc_modify_add_color.json'
        component2_cluster2_add_color = f'{version2_path}_GraphIDFunc_modify_add_component_cluster_color.json'
        architecture2_change_json = update_json(input_version2_file, output_version2_file, added_files, removed_files,
                                                moved_files)

        architecture1_component_cluster_add_color_change, architecture2_component_cluster_add_color_change = component_cluster_add_color(
            architecture1_change_json, architecture2_change_json, version1_version2_a2a_mapping_weight_path)
        with open(component1_cluster1_add_color, 'w', encoding='utf-8') as f:
            json.dump(architecture1_component_cluster_add_color_change, f, indent=4)
        with open(component2_cluster2_add_color, 'w', encoding='utf-8') as f:
            json.dump(architecture2_component_cluster_add_color_change, f, indent=4)

        # print(architecture2_change_json)
        # with open(architecture1_change_json,'r',encoding='utf-8') as f:
        #     architecture1_change_json = json.load(f)
        # with open(architecture2_change_json,'r',encoding='utf-8') as f:
        #     architecture2_change_json = json.load(f)
        # file_belongto_cluster_change = file_operation_change(rsf_version1,rsf_version2,res,added_files,removed_files,moved_files)
        # print(type(res))
        # print(res)
        version1_component_cluster_file_code_all_level = merge_Graph_Entities_json_to_Whole_reverse_tree_layer(
            os.path.join(code_changes_root_path, 'entities_changes_info.json'), component1_cluster1_add_color,
            f'{version1_path}_project_all_level_entities.json')
        version2_component_cluster_file_code_all_level = merge_Graph_Entities_json_to_Whole_reverse_tree_layer(
            os.path.join(code_changes_root_path, 'entities_changes_info.json'), component2_cluster2_add_color,
            f'{version2_path}_project_all_level_entities.json')
        print("architecture_change中version1_component_cluster_file_code_all_level： ",
              version1_component_cluster_file_code_all_level)
        print("architecture_change中version2_component_cluster_file_code_all_level： ",
              version2_component_cluster_file_code_all_level)
        res_serializable = {str(key): value for key, value in res.items()}

        # 把return中的变量更新到数据库中，原：后端->EventBus->前端；现：后端->database->前端
        # 拿到前端传来的当前分析的 analysisId
        data = request.get_json(silent=True) or {}
        aid = data.get("analysisId")
        if not aid:
            return jsonify({"error": "缺少 analysisId"}), 400

        rec = analysis_records_col.find_one({"_id": ObjectId(aid)})
        if not rec:
            return jsonify({"error": "记录不存在"}), 404

        # 更新记录中的变量
        raw_update_fields = {
            "a2a_value": str(a2a_value),
            "change_total": str(change_total),
            "module_weight": res_serializable,
            "added_file": added,
            "removed_file": removed,
            "moved_file": moved,
            "architecture1_change_json": version1_component_cluster_file_code_all_level,
            "architecture2_change_json": version2_component_cluster_file_code_all_level,
            "file_unit_operation_change_json": file_unit_operation_change,
            "a2a_tableInfo": a2a_tableInfo_json,
            "a2a_tableInfo_json_add_fileInfo": a2a_tableInfo_json_add_fileInfo
        }

        # 辅助函数：对每个字段，若大小超阈值则存 GridFS，否则直接 $set
        def build_update_doc(analysis_id, fields: dict):
            set_ops = {}
            unset_ops = {}
            for key, val in fields.items():
                # 转成字符串以测大小
                raw = json.dumps(val, ensure_ascii=False)
                byte_size = len(raw.encode("utf-8"))
                if byte_size > MAX_DOCUMENT_SIZE:
                    # 存到 GridFS
                    file_id = fs.put(
                        raw.encode("utf-8"),
                        filename=f"{analysis_id}_{key}.json",
                        metadata={"analysisId": ObjectId(analysis_id), "field": key},
                        contentType="application/json"
                    )
                    # 在主文档里记录 gridfs_id
                    set_ops[f"{key}_gridfs_id"] = file_id
                    # 如果之前有直接存储的字段，用 $unset 清理
                    unset_ops[key] = ""
                else:
                    # 小文件直接写入
                    set_ops[key] = val

            update_doc = {}
            if set_ops:
                update_doc["$set"] = set_ops
            if unset_ops:
                update_doc["$unset"] = unset_ops
            return update_doc

        # 构建并执行更新
        update_doc = build_update_doc(aid, raw_update_fields)

        analysis_records_col.update_one(
            {"_id": ObjectId(aid)},
            update_doc
        )

        return {
            "message": "Architecture change analysis completed",
            "status": "success",
            "version1": version1_tag,
            "version2": version2_tag,
            "a2a_value": str(a2a_value),
            "change_total": str(change_total),
            "module_weight": res_serializable,
            "added_file": added,
            "removed_file": removed,
            "moved_file": moved,
            # "architecture1_change_json":architecture1_component_cluster_add_color_change,
            # "architecture2_change_json": architecture2_component_cluster_add_color_change,
            "architecture1_change_json": version1_component_cluster_file_code_all_level,
            "architecture2_change_json": version2_component_cluster_file_code_all_level,
            "file_unit_operation_change_json": file_unit_operation_change,
            "a2a_tableInfo": a2a_tableInfo_json,
            "a2a_tableInfo_json_add_fileInfo": a2a_tableInfo_json_add_fileInfo
        }, 200
    else:
        return {
            "message": "还需要选择一个版本文件",
            "status": "success",
        }, 200


def run_clustering_modify_right(project_url, knowledge):
    # data = request.get_json()
    global rsf_version2
    global version2_path
    global analysis_project_language
    global named_cluster_path_v1
    global cluster_component_path_v1
    project_folder = project_url
    project_name = os.path.basename(project_folder)
    # whole_project_path = project_name
    if not project_folder:
        return jsonify({"error": "project_folder is required"}), 400

    # 构建文件路径
    code_sem_file = os.path.join(result_dir, project_name, f'{project_name}_CodeSem.json')
    # arch_sem_file = os.path.join(result_dir, project_name, f'{project_name}_ArchSem.json')
    global arch_sem_file  #使用同一套架构模式

    # 如果没有生成必要的 .json 文件，则先调用 /get_semantic 接口
    if not os.path.exists(code_sem_file) or not os.path.exists(arch_sem_file):
        # 调用 get_semantic 生成文件
        # analysis_project_language存储逆向分析的项目语言 值是在utils.utils.get_prj_lang(clone_dir)

        # 检查是否存在 README 或 README.md 文件
        readme_path = os.path.join(project_folder, "README")
        readme_md_path = os.path.join(project_folder, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, "r", encoding="utf-8") as readme_file:
                knowledge = readme_file.read()
        elif os.path.exists(readme_md_path):
            with open(readme_md_path, "r", encoding="utf-8") as readme_md_file:
                knowledge = readme_md_file.read()

        get_semantic(language=analysis_project_language, folder_path=project_folder, knowledge=knowledge,
                     arch_sem_path=arch_sem_file)  #领域知识参数：knowledge
        if not os.path.exists(code_sem_file) or not os.path.exists(arch_sem_file):
            return jsonify({"error": "Failed to generate semantic files"}), 500

    # 运行聚类功能
    stopwords_path = 'stopwords.txt'
    # pattern_file_path = os.path.join(result_dir, project_name, f'{project_name}_ArchSem.json')
    # llm_file_path = os.path.join(result_dir, project_name, f'{project_name}_CodeSem.json')
    pattern_file_path = arch_sem_file
    llm_file_path = code_sem_file

    # 在调用 cluster_project 函数之前处理 project_folder
    # if os.path.exists(os.path.join(project_folder, "test")):
    #     test_folder_path = os.path.join(project_folder, "test")
    #     print(f"发现 'test' 文件夹，正在删除: {test_folder_path}")
    #     shutil.rmtree(test_folder_path)  # 删除 'test' 文件夹及其内容
    #     print("'test' 文件夹已删除")

    # try:
    # 调用 cluster_project 函数执行聚类操作
    cluster_project(
        data_paths=[project_folder],
        gt_json_paths=None,
        resolution=1.2,
        result_folder_name=None,
        cache_dir='./cache',
        save_to_csvfile=True,
        stopword_files=[stopwords_path],
        generate_figures=True,
        pattern_file=[pattern_file_path],
        llm_file=[llm_file_path]
    )

    # def remove_empty_clusters(cluster_result_path):
    # # 加载 cluster_result.json
    #     with open(cluster_result_path, 'r', encoding='utf-8') as f:
    #         cluster_result = json.load(f)

    #     new_cluster={
    #         "@schemaVersion":"1.0",
    #         "name": "clustering",
    #         "structure": []
    #     }
    #     # 找到空簇的编号
    #     empty_clusters = [
    #         int(group["name"]) for group in cluster_result["structure"]
    #         if group["@type"] == "group" and not group["nested"]
    #     ]

    #     print(f"Empty clusters found: {empty_clusters}")  # 调试信息

    #     # 加载 cluster_result_named.json
    #     # with open(named_cluster_path, 'r', encoding='utf-8') as f:
    #     #     named_clusters = json.load(f)

    #     # 过滤掉空簇
    #     new_cluster["structure"] = [
    #         module for module in cluster_result["structure"]
    #         if int(module["name"]) not in empty_clusters
    #     ]

    #     # 保存更新后的 cluster_result_named.json
    #     with open(cluster_result_path, 'w', encoding='utf-8') as f:
    #         json.dump(new_cluster, f, indent=4, ensure_ascii=False)

    #     print("Empty clusters removed from named clusters.")

    # # 新增步骤：移除空簇
    # remove_empty_clusters(
    #     os.path.join(result_dir, project_name, f'cluster_result.json'),
    # )

    #模块命名
    print("———————————————————————————————————————开始模块命名———————————————————————————————————————————————————————")
    module_names=os.path.join(result_dir, project_name, f'cluster_result_named.json')
    # named_cluster_path_v2,cluster_component_path_v2=module_naming(result_dir,project_name,os.path.join(result_dir, project_name, f'cluster_result.json'), llm_file_path,knowledge=knowledge)  #领域知识加在这里
    # 目录做模块
    named_cluster_path_v2,cluster_component_path_v2=module_naming_dict(result_dir,project_name,os.path.join(result_dir, project_name, f'cluster_result_pkg.json'), llm_file_path,knowledge=knowledge)  #领域知识加在这里

    # 统一两个版本的模块命名
    # module_naming_double_check(named_cluster_path_v1, cluster_component_path_v1,named_cluster_path_v2, cluster_component_path_v2)
    # print("**********模块命名检查完成！**********\n")

    #合并组件-模块和模块-文件json
    final_json_path = os.path.join(result_dir, project_name, f"{project_name}_Final.json")
    if not os.path.exists(final_json_path):
        merge_json_files(cluster_component_path_v2, named_cluster_path_v2, final_json_path)

    #生成新的graph id
    graph_id_path = os.path.join(result_dir, project_name, f'{project_name}_GraphID.json')
    if not os.path.exists(graph_id_path):
        graph_json(final_json_path, graph_id_path)

    #添加functionality
    component_sum_path = os.path.join(result_dir, project_name, f'{project_name}_ComponentSum.json')
    if not os.path.exists(component_sum_path):
        convert_component_to_sum(pattern_file_path, component_sum_path)
    # 添加生成 ModuleSum.json 的逻辑
    module_sum_path = os.path.join(result_dir, project_name, f'{project_name}_ModuleSum.json')
    if not os.path.exists(module_sum_path):
        convert_module_to_sum(module_names, module_sum_path)

    graph_id_func_path = os.path.join(result_dir, project_name, f'{project_name}_GraphIDFunc.json')  # 可视化json文件

    if not os.path.exists(graph_id_func_path):
        merge_functionality_with_clusters(graph_id_path, llm_file_path, graph_id_func_path, module_sum_path)
        merge_functionality_with_clusters(graph_id_func_path, component_sum_path, graph_id_func_path, module_sum_path)

    json_file_path = os.path.join(os.path.join(result_dir, project_name, f'{project_name}_GraphIDFunc.json'))
    rsf_version2 = json_to_rsf(
        os.path.join(os.path.join(result_dir, project_name, f'{project_name}_NamedClusters.json')),
        os.path.join(os.path.join(result_dir, project_name, f'{project_name}_rsf.rsf')))
    version2_path = os.path.join(os.path.join(result_dir, project_name, f'{project_name}'))
    print("run_clustering_modify_right中version2_path", version2_path)
    if os.path.exists(json_file_path):
        print("json_file_path")
        print(json_file_path)
        print("project_name")
        print(project_name)
        # 读取JSON文件内容
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            file_content = json.load(json_file)
        with open(json_file_path, 'r', encoding='utf-8') as f:
            reverse_layer_graph = json.load(f)
            # print(reverse_layer_graph)
        # 返回JSON文件内容作为响应
        return {
            "sharedFile": file_content,
            "reverse_layer_graph": reverse_layer_graph
        }
    else:
        return {"error": "File not found"}


def run_clustering_modify(project_url, domain_knowledge=""):
    # data = request.get_json()
    global rsf_version1
    global version1_path
    global analysis_project_language
    project_folder = project_url
    print("run_clustering_project_folder", project_folder)
    project_name = os.path.basename(project_folder)
    # whole_project_path = project_name
    if not project_folder:
        return jsonify({"error": "project_folder is required"}), 400

    # 将架构模式和组件作为全局变量
    global arch_sem_file
    # 构建文件路径
    code_sem_file = os.path.join(result_dir, project_name, f'{project_name}_CodeSem.json')
    arch_sem_file = os.path.join(result_dir, project_name, f'{project_name}_ArchSem.json')

    # 如果没有生成必要的 .json 文件，则先调用 /get_semantic 接口
    if not os.path.exists(code_sem_file) or not os.path.exists(arch_sem_file):
        # 调用 get_semantic 生成文件
        # project_lang= utils.utils.get_prj_lang()
        # analysis_project_language 存储逆向分析的项目语言

        # 检查是否存在 README 或 README.md 文件
        readme_path = os.path.join(project_folder, "README")
        readme_md_path = os.path.join(project_folder, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, "r", encoding="utf-8") as readme_file:
                domain_knowledge = readme_file.read()
        elif os.path.exists(readme_md_path):
            with open(readme_md_path, "r", encoding="utf-8") as readme_md_file:
                domain_knowledge = readme_md_file.read()

        get_semantic(language=analysis_project_language, folder_path=project_folder, knowledge=domain_knowledge,
                     arch_sem_path=arch_sem_file)  #领域知识加在这里
        if not os.path.exists(code_sem_file) or not os.path.exists(arch_sem_file):
            return jsonify({"error": "Failed to generate semantic files"}), 500

    # 运行聚类功能
    stopwords_path = 'stopwords.txt'
    pattern_file_path = os.path.join(result_dir, project_name, f'{project_name}_ArchSem.json')
    llm_file_path = os.path.join(result_dir, project_name, f'{project_name}_CodeSem.json')

    # 在调用 cluster_project 函数之前处理 project_folder
    # if os.path.exists(os.path.join(project_folder, "test")):
    # test_folder_path = os.path.join(project_folder, "test")
    # print(f"发现 'test' 文件夹，正在删除: {test_folder_path}")
    # shutil.rmtree(test_folder_path)  # 删除 'test' 文件夹及其内容
    # print("'test' 文件夹已删除")
    # try:
    # 调用 cluster_project 函数执行聚类操作
    cluster_project(
        data_paths=[project_folder],
        gt_json_paths=None,
        resolution=1.2,
        result_folder_name=None,
        cache_dir='./cache',
        save_to_csvfile=True,
        stopword_files=[stopwords_path],
        generate_figures=True,
        pattern_file=[pattern_file_path],
        llm_file=[llm_file_path]
    )

    def remove_empty_clusters(cluster_result_path):
        # 加载 cluster_result.json
        with open(cluster_result_path, 'r', encoding='utf-8') as f:
            cluster_result = json.load(f)

        new_cluster = {
            "@schemaVersion": "1.0",
            "name": "clustering",
            "structure": []
        }
        # 找到空簇的编号
        empty_clusters = [
            int(group["name"]) for group in cluster_result["structure"]
            if group["@type"] == "group" and not group["nested"]
        ]

        print(f"Empty clusters found: {empty_clusters}")  # 调试信息

        # 加载 cluster_result_named.json
        # with open(named_cluster_path, 'r', encoding='utf-8') as f:
        #     named_clusters = json.load(f)

        # 过滤掉空簇
        new_cluster["structure"] = [
            module for module in cluster_result["structure"]
            if int(module["name"]) not in empty_clusters
        ]

        # 保存更新后的 cluster_result_named.json
        with open(cluster_result_path, 'w', encoding='utf-8') as f:
            json.dump(new_cluster, f, indent=4, ensure_ascii=False)

        print("Empty clusters removed from named clusters.")

    # 新增步骤：移除空簇
    remove_empty_clusters(
        os.path.join(result_dir, project_name, f'cluster_result.json'),
    )

    #模块命名
    print("———————————————————————————————————————开始模块命名———————————————————————————————————————————————————————")
    module_names=os.path.join(result_dir, project_name, f'cluster_result_named.json')
    global named_cluster_path_v1
    global cluster_component_path_v1
    # named_cluster_path_v1,cluster_component_path_v1=module_naming(result_dir,project_name,os.path.join(result_dir, project_name, f'cluster_result.json'), llm_file_path,knowledge=domain_knowledge)  #领域知识加在这里
    # 目录结构做模块不需要模块命名
    module_names=os.path.join(result_dir, project_name, f'cluster_result_named.json')
    global named_cluster_path_v1
    global cluster_component_path_v1
    named_cluster_path_v1,cluster_component_path_v1=module_naming_dict(result_dir,project_name,os.path.join(result_dir, project_name, f'cluster_result_pkg.json'), llm_file_path,knowledge=domain_knowledge)  #领域知识加在这里

    #合并组件-模块和模块-文件json
    final_json_path = os.path.join(result_dir, project_name, f"{project_name}_Final.json")
    if not os.path.exists(final_json_path):
        merge_json_files(cluster_component_path_v1, named_cluster_path_v1, final_json_path)

    #生成新的graph id
    graph_id_path = os.path.join(result_dir, project_name, f'{project_name}_GraphID.json')
    if not os.path.exists(graph_id_path):
        graph_json(final_json_path, graph_id_path)

    #添加functionality
    component_sum_path = os.path.join(result_dir, project_name, f'{project_name}_ComponentSum.json')
    if not os.path.exists(component_sum_path):
        convert_component_to_sum(pattern_file_path, component_sum_path)
    # 添加生成 ModuleSum.json 的逻辑
    module_sum_path = os.path.join(result_dir, project_name, f'{project_name}_ModuleSum.json')
    if not os.path.exists(module_sum_path):
        convert_module_to_sum(module_names, module_sum_path)

    graph_id_func_path = os.path.join(result_dir, project_name, f'{project_name}_GraphIDFunc.json')  # 可视化json文件

    if not os.path.exists(graph_id_func_path):
        merge_functionality_with_clusters(graph_id_path, llm_file_path, graph_id_func_path, module_sum_path)
        merge_functionality_with_clusters(graph_id_func_path, component_sum_path, graph_id_func_path, module_sum_path)

    json_file_path = os.path.join(os.path.join(result_dir, project_name, f'{project_name}_GraphIDFunc.json'))
    rsf_version1 = json_to_rsf(
        os.path.join(os.path.join(result_dir, project_name, f'{project_name}_NamedClusters.json')),
        os.path.join(os.path.join(result_dir, project_name, f'{project_name}_rsf.rsf')))
    version1_path = os.path.join(os.path.join(result_dir, project_name, f'{project_name}'))
    print("run_clustering_modify中version1_path", version1_path)
    if os.path.exists(json_file_path):
        print("json_file_path")
        print(json_file_path)
        print("project_name")
        print(project_name)
        # 读取JSON文件内容
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            file_content = json.load(json_file)
        with open(json_file_path, 'r', encoding='utf-8') as f:
            reverse_layer_graph = json.load(f)
            # print(reverse_layer_graph)
        # 返回JSON文件内容作为响应
        return {
            "sharedFile": file_content,
            "reverse_layer_graph": reverse_layer_graph
        }
    else:
        return {"error": "File not found"}


@app.route("/get_git_refs", methods=["POST"])
def get_git_refs():
    """获取 Git 仓库的分支和 Tag 列表"""
    global global_repo_url
    global repo_clone_local_path
    global clone_url_no_version
    data = request.json
    repo_url = data.get("repo_url")
    global_repo_url = repo_url
    project_name = repo_url.split('/')[-1].replace('.git', '')
    print(project_name)
    clone_dir = os.path.abspath(project_name)
    clone_url_no_version = clone_dir
    repo_clone_local_path = clone_dir
    print("clone_dir:")
    print(clone_dir)
    if not repo_url:
        return jsonify({"error": "缺少仓库 URL"}), 400

    # 判断是否为 Chromium
    if "chromium" in repo_url:
        depot_tools_dir = os.path.abspath("depot_tools")
        if not os.path.exists(depot_tools_dir):
            subprocess.run([
                "git", "clone", "https://chromium.googlesource.com/chromium/tools/depot_tools.git", depot_tools_dir
            ], check=True)
        env = os.environ.copy()
        env["PATH"] = depot_tools_dir + env["PATH"]
        chromium_dir = os.path.abspath("chromium")
        repo_clone_local_path = chromium_dir
        if not os.path.exists(chromium_dir):
            subprocess.run(["fetch", "chromium"], cwd=os.path.dirname(chromium_dir), check=True)
        # 获取分支和 tag
        result = subprocess.run(['git', '-C', chromium_dir, 'ls-remote', '--refs'], capture_output=True, text=True,
                                check=True)
    else:
        project_name = repo_url.split('/')[-1].replace('.git', '')
        clone_dir = os.path.abspath(project_name)
        repo_clone_local_path = clone_dir
        if os.path.exists(clone_dir) and len(os.listdir(clone_dir)) > 5:
            subprocess.run(["git", "-C", clone_dir, "fetch", "--all"], check=True)
        else:
            subprocess.run(["git", "clone", "--bare", "--depth", "1", repo_url, clone_dir], check=True)
        result = subprocess.run(['git', '-C', clone_dir, 'ls-remote', '--refs'], capture_output=True, text=True,
                                check=True)
    # if not repo_url:
    #     return jsonify({"error": "缺少仓库 URL"}), 400
    #
    # try:
    #     if os.path.exists(clone_dir) and len(os.listdir(clone_dir)) > 5:
    #         # 如果目录已存在，进入目录并更新
    #         print(f"目录 {clone_dir} 已存在，尝试更新仓库...")
    #         subprocess.run(["git", "-C", clone_dir, "fetch", "--all"], check=True, stdout=subprocess.PIPE,
    #                        stderr=subprocess.PIPE)
    #     elif os.path.exists(clone_dir) and len(os.listdir(clone_dir)) <= 5:
    #         print(f"目录 {clone_dir} 已存在，但内容过少，重新克隆。")
    #         shutil.rmtree(clone_dir, ignore_errors=True)  # 使用 shutil.rmtree 删除目录
    #         subprocess.run(["git", "clone", "--bare", repo_url, clone_dir], check=True, stdout=subprocess.PIPE,
    #                        stderr=subprocess.PIPE)
    #         print(f"仓库已成功克隆到 {clone_dir}")
    #     else:
    #         # 如果目录不存在，克隆仓库
    #         print(f"正在克隆仓库 {repo_url} 到 {clone_dir}...")
    #         subprocess.run(["git", "clone", "--bare", repo_url, clone_dir], check=True, stdout=subprocess.PIPE,
    #                        stderr=subprocess.PIPE)

    # 获取分支和标签
    result = subprocess.run(['git', '-C', clone_dir, 'ls-remote', '--refs'], capture_output=True, text=True,
                            check=True)
    branches = []
    tags = []
    for line in result.stdout.split("\n"):
        if not line.strip():
            continue
        ref_hash, ref_name = line.split("\t")
        if ref_name.startswith("refs/heads/"):
            branches.append(ref_name.replace("refs/heads/", ""))
        elif ref_name.startswith("refs/tags/"):
            tags.append(ref_name.replace("refs/tags/", ""))

    return jsonify({"branches": branches, "tags": tags})

    # except subprocess.CalledProcessError as e:
    #     return jsonify({"error": f"无法获取仓库信息: {e.stderr.decode('utf-8')}"}), 500


@app.route("/select_version", methods=["POST"])
def select_version():
    global version1_tag
    global whole_project_name
    global analysis_project_language
    run_clustering_modify_json = {}
    """接收用户选择的 Git 版本"""
    data = request.json
    repo_url = data.get("repo_url")
    selected_version = data.get("selected_version")
    domain_knowledge = data.get("domain_knowledge", "")
    version1_tag = selected_version

    if not repo_url or not selected_version:
        return jsonify({"error": "缺少仓库 URL 或版本"}), 400

    try:
        # 获取项目名称
        project_name = repo_url.split('/')[-1].replace('.git', '')
        whole_project_name = project_name
        # 在根目录下创建子目录，命名为 "项目名称-版本号"
        clone_dir_version = selected_version.replace("/", "")
        clone_dir = os.path.abspath(f"{project_name}-{clone_dir_version}")
        print(f"克隆目录: {clone_dir}")

        # 如果目录已存在，跳过克隆
        if os.path.exists(clone_dir) and len(os.listdir(clone_dir)) > 5:
            print(os.listdir(clone_dir))
            print(f"目录 {clone_dir} 已存在，跳过克隆。")
        elif os.path.exists(clone_dir) and len(os.listdir(clone_dir)) <= 5:
            #删除clone_dir然后克隆
            print(f"目录 {clone_dir} 已存在，但内容过少，重新克隆。")
            # subprocess.run(["rm", "-rf", clone_dir], check=True, text=True) # 删除目录
            #windows下删除目录
            shutil.rmtree(clone_dir)  # 删除目录  
            # subprocess.run(["git", "clone", "--branch", selected_version, "--depth", "1", repo_url, clone_dir], check=True, text=True)
            clone_repo_with_retry(repo_url=repo_url, selected_version=selected_version, clone_dir=clone_dir)

        else:
            # 使用 --branch 克隆指定版本到子目录
            # print(f"正在克隆仓库 {repo_url} 的 {selected_version} 版本到 {clone_dir}...")
            # subprocess.run(
            #     ["git", "clone", "--branch", selected_version, "--depth", "1", repo_url, clone_dir],
            #     check=True,
            #     text=True
            # )
            # print(f"仓库已成功克隆到 {clone_dir}")
            clone_repo_with_retry(repo_url=repo_url, selected_version=selected_version, clone_dir=clone_dir)
        # 验证标签是否存在
        # def tag_exists(tag, repo_dir):
        #     result = subprocess.run(
        #         ["git", "-C", repo_dir, "rev-parse", "--verify", tag],
        #         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        #     )
        #     return result.returncode == 0

        # if not tag_exists(selected_version, clone_dir):
        #     return jsonify({"error": f"Tag {selected_version} 不存在"}), 400

        # 拉取完整历史
        if os.path.exists(os.path.join(clone_dir, ".git", "shallow")):
            subprocess.run(["git", "-C", clone_dir, "fetch", "--unshallow"], check=True, text=True)
        else:
            subprocess.run(["git", "-C", clone_dir, "fetch", "--all"], check=True, text=True)

        analysis_project_language = utils.utils.get_prj_lang(clone_dir)
        # 调用后续处理逻辑
        run_clustering_modify_json = run_clustering_modify(clone_dir, domain_knowledge)
        # print("版本一：run_clustering_modify_json", run_clustering_modify_json)

    except subprocess.CalledProcessError as e:
        print(f"Git 克隆失败: {e}")
        return jsonify({"error": f"Git 克隆失败: {e}"}), 500

    return {
        "message": "版本1逆向完成",
        "repo_url": repo_url,
        "selected_version": selected_version,
        "run_clustering_modify_json": run_clustering_modify_json.get('reverse_layer_graph', {})
    }, 200


@app.route("/select_version_right", methods=["POST"])
def select_version_right():
    global version1_tag
    global version2_tag
    global repo_clone_local_path
    global clone_url_no_version
    """接收用户选择的 Git 版本"""
    data = request.json
    repo_url = data.get("repo_url")
    selected_version = data.get("selected_version")
    domain_knowledge = data.get("domain_knowledge", "")
    version2_tag = selected_version
    project_name = repo_url.split('/')[-1].replace('.git', '')
    project_result_dir = os.path.abspath(os.path.join("results"))
    print("version2_tag_select_version", version2_tag)
    os.makedirs(os.path.join(os.path.join("results"), f"{project_name}-{version1_tag}{version2_tag}"),
                exist_ok=True)  # 确保目录存在
    commit_log_dir = os.path.abspath(
        os.path.join("results", f'{project_name}-{version1_tag}{version2_tag}', f"{project_name}_log.txt"))
    log_json_dir = os.path.abspath(
        os.path.join("results", f'{project_name}-{version1_tag}{version2_tag}', f"{project_name}_log.json"))
    commit_log_module = os.path.abspath(
        os.path.join("results", f'{project_name}-{version1_tag}{version2_tag}', f"{project_name}_log_module.json"))
    recovered_result = os.path.abspath(os.path.join("results"))
    if not repo_url or not selected_version:
        return jsonify({"error": "缺少仓库 URL 或版本"}), 400

    try:
        # 获取项目名称
        project_name = repo_url.split('/')[-1].replace('.git', '')
        # 在根目录下创建子目录，命名为 "项目名称-版本号"
        clone_dir_version = selected_version.replace("/", "")
        clone_dir = os.path.abspath(f"{project_name}-{clone_dir_version}")
        # clone_dir = os.path.abspath(f"{project_name}-{selected_version}")
        log_dir = commit_log_dir

        print(f"克隆目录: {clone_dir}")
        print(f"日志目录: {log_dir}")

        # 如果目录已存在，跳过克隆
        if os.path.exists(clone_dir) and len(os.listdir(clone_dir)) > 5:
            print(f"目录 {clone_dir} 已存在，跳过克隆。")
        elif os.path.exists(clone_dir) and len(os.listdir(clone_dir)) <= 5:
            #删除clone_dir然后克隆
            # print(f"目录 {clone_dir} 已存在，但内容过少，重新克隆。")
            # subprocess.run(["rm", "-rf", clone_dir], check=True, text=True) # 删除目录  
            # clone_repo_with_retry(repo_url=repo_url,selected_version=selected_version,clone_dir=clone_dir)
            print(f"目录 {clone_dir} 已存在，但内容过少，重新克隆。")
            shutil.rmtree(clone_dir, ignore_errors=True)  # 使用 shutil.rmtree 删除目录
            clone_repo_with_retry(repo_url=repo_url, selected_version=selected_version, clone_dir=clone_dir)
        else:
            # 使用 --branch 克隆指定版本到子目录
            print(f"正在克隆仓库 {repo_url} 的 {selected_version} 版本到 {clone_dir}...")
            # subprocess.run(
            #     ["git", "clone", "--branch", selected_version, "--depth", "1", repo_url, clone_dir],
            #     check=True,
            #     text=True
            # )
            # print(f"仓库已成功克隆到 {clone_dir}")
            clone_repo_with_retry(repo_url=repo_url, selected_version=selected_version, clone_dir=clone_dir)

        # 调用后续处理逻辑
        run_clustering_right_modify_json = run_clustering_modify_right(clone_dir, domain_knowledge)
        print("版本二：run_clustering_right_modify_json", run_clustering_right_modify_json)

    except subprocess.CalledProcessError as e:
        print(f"Git 克隆失败: {e}")
        return jsonify({"error": f"Git 克隆失败: {e}"}), 500

    # 验证标签是否存在
    # def tag_exists(tag, repo_dir):
    #     result = subprocess.run(
    #         ["git", "-C", repo_dir, "rev-parse", "--verify", tag],
    #         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    #     )
    #     return result.returncode == 0

    # if not tag_exists(version1_tag, clone_dir):
    #     return jsonify({"error": f"Tag {version1_tag} 不存在"}), 400
    # if not tag_exists(version2_tag, clone_dir):
    #     return jsonify({"error": f"Tag {version2_tag} 不存在"}), 400

    # # 拉取完整历史
    # if os.path.exists(os.path.join(clone_dir, ".git", "shallow")):
    #     subprocess.run(["git", "-C", clone_dir, "fetch", "--unshallow"], check=True, text=True)
    # else:
    #     subprocess.run(["git", "-C", clone_dir, "fetch", "--all"], check=True, text=True)

    # # 提取提交日志
    # with open(log_dir, "w", encoding="utf-8") as f:
    #     subprocess.run(
    #         [
    #             "git", "-C", clone_dir, "log", f"{version1_tag}..{version2_tag}",
    #             "--pretty=format:commit %H%n%ad, %s%n",
    #             "--date=format:%Y.%m.%d",
    #             "--numstat"
    #         ],
    #         stdout=f,
    #         check=True,
    #         text=True
    #     )
    #     print(f"commit log 已成功保存到 {log_dir}")

    # # 调用后续处理逻辑
    # analyze_commit_log2(commit_log_dir, log_json_dir)
    # generate_architecture_change_reports(project_name, version1_tag, version2_tag, log_json_dir, commit_log_module, recovered_result)

    # Step 2. 提取提交日志
    try:
        # 进入克隆后的仓库目录
        original_dir = os.getcwd()
        # os.chdir(clone_dir)
        os.chdir(clone_url_no_version)
        print(f"切换到仓库目录: {os.getcwd()}")

        # 检查 tag 是否存在
        # def tag_exists(tag):
        #     result = subprocess.run(
        #         ["git", "rev-parse", "--verify", tag],
        #         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        #     )
        #     return result.returncode == 0

        # if not tag_exists(version1_tag):
        #     print(f"Tag {version1_tag} 不存在")
        #     raise Exception(f"Tag {version1_tag} 不存在")

        # if not tag_exists(version2_tag):
        #     print(f"Tag {version2_tag} 不存在")
        #     raise Exception(f"Tag {version2_tag} 不存在")

        # 拉取完整历史
        # if os.path.exists(".git/shallow"):
        #     subprocess.run(["git", "fetch", "--unshallow"], check=True, text=True)
        # else:
        #     subprocess.run(["git", "fetch"], check=True, text=True)

        # 提取 commit log
        with open(log_dir, "w", encoding="utf-8") as f:
            try:
                subprocess.run(
                    [
                        "git", "log", f"{version1_tag}..{version2_tag}",
                        "--pretty=format:commit %H%n%ad, %s%n",
                        "--date=format:%Y.%m.%d",
                        "--numstat",
                        "--"
                    ],
                    stdout=f,
                    check=True,
                    text=True
                )
                print(f"commit log 已成功保存到 {log_dir}")
            except subprocess.CalledProcessError as e:
                print(f"git log 执行失败: {e}")
                f.write(f"\ngit log 执行失败: {e}\n")
                raise

        check = os.path.join(project_result_dir, f'{project_name}-{version1_tag}{version2_tag}',
                             f"{project_name}_full_report.md")
        print(f'文件夹:{check}')
        if os.path.exists(check):
            print(f"文件夹存在: {check}")
        else:
            analyze_commit_log2(commit_log_dir, log_json_dir)
            # generate_architecture_change_reports(project_name, version1_tag, version2_tag, log_json_dir,
            #                                      commit_log_module, recovered_result)
    finally:
        os.chdir(original_dir)
        print(f"返回到原目录: {original_dir}")

    return {
        "message": "版本2逆向完成",
        "repo_url": repo_url,
        "selected_version": selected_version,
        "run_clustering_right_modify_json": run_clustering_right_modify_json.get('reverse_layer_graph', {})
    }, 200


@app.route('/generate_code_changes', methods=['POST'])
def generate_code_changes():
    global global_repo_url
    global version1_tag
    global version2_tag
    global whole_project_name
    global repo_clone_local_path
    global code_changes_root_path
    print("generate_code_changes中的 global_repo_url", global_repo_url)
    version1_modify_tag = version1_tag.replace("/", "")
    version2_modify_tag = version2_tag.replace("/", "")
    code_change_store_path = os.path.join(result_dir,
                                          f'{whole_project_name}-{version1_modify_tag}{version2_modify_tag}',
                                          "code_changes")
    code_analysis_input = AnalysisInput(global_repo_url, version1_tag, version2_tag, code_change_store_path,
                                        repo_clone_local_path)
    analyzer = SemanticChangeAnalyzer(code_analysis_input)
    analyzer.run_analysis()  # 不再返回实体数值
    # 获取 changes_root_path
    # changes_root_path = analyzer.changes_root_path
    code_changes_root_path = analyzer.changes_root_path
    print("code_changes中的changes_root_path ", code_changes_root_path)
    # print("select_version_right中的changes_root_path ", changes_root_path) :D:\backend\semarc_backend\results\libuv-v1.44.2v1.48.0\code_changes/libuv-0c1fa696aa502eb749c2c4735005f41ba00a27b8-e9f29cb984231524e3931aa0ae2c5dae1a32884e
    # print("num_entities ",num_entities)

    # 把 code_changes_root_path 存储到数据库中
    data = request.get_json(silent=True) or {}
    aid = data.get('analysisId')
    if not aid:
        return jsonify({"error": "缺少 analysisId"}), 400

    rec = analysis_records_col.find_one({'_id': ObjectId(aid)})
    if not rec:
        return jsonify({"error": "记录不存在"}), 404

    # 更新记录中的变量
    update_fields = {
        'code_changes_root_path': code_changes_root_path,
        'repo_clone_local_path': repo_clone_local_path
    }
    analysis_records_col.update_one(
        {"_id": ObjectId(aid)},
        {"$set": update_fields}
    )

    #代码变更分析后调用报告生成
    log_json_dir = os.path.join(result_dir, f'{whole_project_name}-{version1_modify_tag}{version2_modify_tag}',
                                f"{whole_project_name}_log.json")
    commit_log_module = os.path.join(result_dir, f'{whole_project_name}-{version1_modify_tag}{version2_modify_tag}',
                                     f"{whole_project_name}_log_module.json")
    generate_architecture_change_reports(whole_project_name, version1_tag, version2_tag, log_json_dir,
                                         commit_log_module, result_dir, repo_clone_local_path)

    return {
        "message": "代码变更分析完成",
        "status": "success",
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=8000, debug=True)
