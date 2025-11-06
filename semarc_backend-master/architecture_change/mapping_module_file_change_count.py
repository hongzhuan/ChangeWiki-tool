import sys
import os
import subprocess
import sys
from collections import defaultdict
import shutil
import json

def clone_and_diff(git_repo_url, version1, version2, output_diff_file):
    """
        克隆Git仓库并生成版本差异报告

        参数：
        git_repo_url: Git仓库地址（支持HTTP/SSH）
        version1: 基准版本（commit hash/tag/branch）
        version2: 目标版本（commit hash/tag/branch）
        output_diff_file: 生成的差异文件路径
        """
    try:
        # 获取项目名称（处理.git结尾的情况）
        project_name = git_repo_url.split('/')[-1].replace('.git', '')
        clone_dir = os.path.abspath(project_name)
        print("clone_dir",clone_dir)
        # 克隆或更新仓库
        if not os.path.exists(clone_dir):
            print(f"Cloning repository: {git_repo_url}")
            subprocess.run(
                ['git', 'clone', git_repo_url, clone_dir],
                check=True,
                capture_output=True,
                text=True
            )
        else:
            print(f"Using existing repository: {clone_dir}")
            # 进入目录前保存当前路径
            # original_dir = os.getcwd()
            # os.chdir(clone_dir)
            # # 拉取最新更新
            # subprocess.run(
            #     ['git', 'fetch', '--all', '--tags'],
            #     check=True,
            #     capture_output=True,
            #     text=True
            # )
            # os.chdir(original_dir)

        # 准备环境变量（解决终端宽度限制）
        env = os.environ.copy()
        env['COLUMNS'] = '200'

        # 执行差异分析
        print(f"Analyzing differences between {version1} and {version2}...")
        result = subprocess.run(
            ['git', '-C', clone_dir, 'diff', '--numstat', version1, version2],
            env=env,
            capture_output=True,
            text=True,
            check=True
        )
        # 处理 diff 输出并写入文件
        with open(output_diff_file, 'w', encoding='utf-8') as diff_file:
            for line in result.stdout.strip().split('\n'):
                if not line.strip():
                    continue
                parts = line.strip().split('\t')
                if len(parts) == 3:
                    added, deleted, filename = parts
                    try:
                        total_changes = int(added) + int(deleted)
                        diff_file.write(f"{total_changes} {filename}\n")
                    except ValueError:
                        continue  # 忽略二进制文件或特殊情况
        # with open(output_diff_file, 'r', encoding='utf-8') as f:
        #     print(f"Total changed files: {len(f.readlines())}")

        # os.chdir('..')
    except subprocess.CalledProcessError as e:
        print(f"错误：Git操作失败\n命令：{e.cmd}\n错误信息：{e.stderr}")
        # 清理不完整的克隆
        if os.path.exists(clone_dir) and not os.listdir(clone_dir):
            shutil.rmtree(clone_dir)
        raise
    except Exception as e:
        print(f"未预期的错误：{str(e)}")
        raise
    return output_diff_file
def read_file_changes(file_path):
    """读取第一个参数 txt 文件，返回文件修改次数字典"""
    file_changes = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                count, filename = parts
                file_changes[filename] = int(count)
    return file_changes


def read_rsf(file_path):
    """读取 rsf 文件，返回模块到文件的映射"""
    module_files = defaultdict(set)
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                _, module, filename = parts
                module_files[module].add(filename)
    # print("module_files",module_files)
    # print(module_files)
    return module_files


def read_module_mapping(file_path):
    """读取模块映射文件"""
    mapping = []
    a2a_mapping_weight = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # parts = line.strip().split(',')
            parts = line.strip().split('#')
            if len(parts) == 3:
                old_module, new_module, a2a_weight = parts
                mapping.append((old_module, new_module))
                a2a_mapping_weight[f"{old_module},{new_module}"] = float(a2a_weight)
    print("mapping",mapping)
    return mapping,a2a_mapping_weight


def a2a_commit_weight_combine(file_change_path, rsf_v1_path, rsf_v2_path, module_mapping_path,output_path):
    output_json_data = {
        "structure": []
    }
    file_changes = read_file_changes(file_change_path)
    modules_v1 = read_rsf(rsf_v1_path)
    modules_v2 = read_rsf(rsf_v2_path)
    module_mappings , a2a_mapping_weight = read_module_mapping(module_mapping_path)

    module_change_counts = {}

    for old_module, new_module in module_mappings:
        mapping_name = f"{old_module},{new_module}"

        files_v1 = modules_v1.get(old_module, set()) if old_module != "-1" else set()
        files_v2 = modules_v2.get(new_module, set()) if new_module != "-1" else set()
        print("file_v1",files_v1)
        # 取并集，避免重复文件双算
        all_files = files_v1.union(files_v2)

        total_changes = sum(file_changes.get(file, 0) for file in all_files)
        module_change_counts[mapping_name] = total_changes

    total = sum(module_change_counts.values())
    normalized_weights = {k: (v / total if total else 0) for k, v in module_change_counts.items()}

    # print("模块映射\t修改总数\ta2a权重\tcommit归一化权重")
    # for mapping in module_change_counts:
    #     print(f"{mapping}\t{module_change_counts[mapping]}\t{a2a_mapping_weight[mapping]:.5f}\t{normalized_weights[mapping]:.5f}")

    with open(output_path, 'w', encoding='utf-8') as f:
        # f.write("模块映射\ta2a权重\tcommit归一化权重\n")
        for mapping in module_change_counts:
            f.write(f"{mapping},{a2a_mapping_weight[mapping]:.5f},{normalized_weights[mapping]:.5f}\n")
    # with open(output_path, 'r', encoding='utf-8') as json_file:
    #     loaded_data = json.load(json_file)
    for mapping in module_change_counts:
        version1,version2 = mapping.split(',')
        if version1 == '-1':
            version1 = '无映射模块'
        if version2 == '-1':
            version2 = '无映射模块'
        structure_entry = {
            "version1":version1,
            "version2":version2,
            "a2a_weight": a2a_mapping_weight[mapping],
            "LOC":module_change_counts[mapping],
            "commit_weight": normalized_weights[mapping]
        }
        output_json_data["structure"].append(structure_entry)
    return output_json_data


def combine_method(git_repo_url,version1,version2,file_change_path,rsf_v1_path, rsf_v2_path, module_mapping_path,outputpath):
    #file_change_path----两个版本中commit各个文件的修改量
    clone_and_diff(git_repo_url, version1, version2, file_change_path)
    json_data = a2a_commit_weight_combine(file_change_path, rsf_v1_path, rsf_v2_path, module_mapping_path,outputpath)
    return json_data


def combine_method_add_file_numbers_info(json_data,file_json_path):
    # print("combine_method_add_file_numbers_info_:json_data")
    # print(json_data)
    with open(file_json_path, 'r', encoding='utf-8') as json_file:
        loaded_data = json.load(json_file)

    # print("combine_method_add_file_numbers_info_:loaded_data")
    # print(loaded_data)

    for module_version1 in json_data["structure"]:
        module_version1["version1_total_file_number"] = 0
        module_version1["version1_change_file_number"] = 0
        module_version1["version2_total_file_number"] = 0
        module_version1["version2_change_file_number"] = 0
        for module in loaded_data["cluster1_information"]:
            if module_version1["version1"] == module["module_name"]:
                module_version1["version1_total_file_number"] = module["total_file_number"]
                module_version1["version1_change_file_number"] = module["change_file_number"]
                break;
        for module in loaded_data["cluster2_information"]:
            # print(f'第二个if外：{module_version1["version2"]}----{module["module_name"]}')
            if module_version1["version2"] == module["module_name"]:
                # print(f'第二个if内：{module_version1["version2"]}----{module["module_name"]}')
                # print('total_file_number',module["total_file_number"])
                module_version1["version2_total_file_number"] = module["total_file_number"]
                module_version1["version2_change_file_number"] = module["change_file_number"]
                break;

    print("combine_method_add_file_numbers_info_json_data:")
    print(json_data)

    return json_data



    # 读取文件内容

# if __name__ == "__main__":
#     if len(sys.argv) != 8:
#         print("用法: python script.py <git_repo_url> <version1> <version2> <file_changes.txt> <version1.rsf> <version2.rsf> <module_mapping.txt>")
#         sys.exit(1)
#     git_repo_url = sys.argv[1]
#     version1 = sys.argv[2]
#     version2 = sys.argv[3]
#     file_change_path = sys.argv[4]
#     file_change_path = clone_and_diff(git_repo_url,version1,version2,file_change_path)
#     rsf_v1_path = sys.argv[5]
#     rsf_v2_path = sys.argv[6]
#     module_mapping_path = sys.argv[7]
#     a2a_commit_weight_combine(file_change_path, rsf_v1_path, rsf_v2_path, module_mapping_path)
