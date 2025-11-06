import sys
import os
import json


# 解析RSF文件，返回一个字典，模块名 -> 文件列表
def parse_rsf(rsf_file):
    file_map = {}
    f = open(rsf_file, "r", encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        templist = line.strip().split(" ")
        # print templist
        if len(templist) < 3:
            continue
        first_field = templist[0]
        file_path = templist[-1]
        # print(file_path)
        module_name = ' '.join(templist[1:-1])
        # print(module_name)
        if module_name not in file_map:
            file_map[module_name] = set()
        file_map[module_name].add(file_path)
    print("file_map:")
    print(file_map)
    return file_map


# 读取rsf文件，返回一个字典，键是模块名，值是该模块包含的文件集合



# 找到新增、删除、移动的文件
def compare_files(rsf1_map, rsf2_map, res):
    added = []
    removed = []
    moved = []
    file_operation_change = {
        "file_information": []
    }
    cluster_contain_file_info = {
        "cluster1_information": [],
        "cluster2_information": []
    }
    # print(type(rsf1_map.values()))
    # print(rsf1_map.values())
    rsf1_all_file = set()
    rsf2_all_file = set()
    # for item in rsf1_map.values():
    #     rsf1_all_file.update(item)
    # for item in rsf2_map.values():
    #     rsf2_all_file.update(item)
    for module1, files in rsf1_map.items():
        cluster_contain_file_info['cluster1_information'].append({
            "module_name": module1,
            "total_file_number": len(files),
            "change_file_number": 0
        })
        rsf1_all_file.update(files)
    # print("rsf1_all_file:")
    # print(len(rsf1_all_file))
    for module2, files in rsf2_map.items():
        cluster_contain_file_info['cluster2_information'].append({
            "module_name": module2,
            "total_file_number": len(files),
            "change_file_number": 0
        })
        rsf2_all_file.update(files)
    # print("rsf2_all_file:")
    # print(len(rsf2_all_file))
    added_files = rsf2_all_file - rsf1_all_file  # rsf2中有而rsf1中没有的文件
    removed_files = rsf1_all_file - rsf2_all_file  # rsf1中有而rsf2中没有的文件
    moved_files = set()
    # print(rsf2_map)
    for file in added_files:
        for module2, files in rsf2_map.items():
            if file in files:
                added.append((file,"none" ,module2))
                file_operation_change['file_information'].append({
                    "file_name": file,
                    "file_operation": "add",
                    "first_version_module_name":'none',
                    "second_version_module_name": module2
                })
                for cluster in cluster_contain_file_info['cluster2_information']:
                    if cluster['module_name'] == module2:
                        cluster['change_file_number'] += 1
                break;
    for file in removed_files:
        for module1, files in rsf1_map.items():
            if file in files:
                removed.append((file,module1,'none'))
                file_operation_change['file_information'].append({
                    "file_name": file,
                    "file_operation": "remove",
                    "first_version_module_name": module1,
                    "second_version_module_name":'none'
                })
                for cluster in cluster_contain_file_info['cluster1_information']:
                    if cluster['module_name'] == module1:
                        cluster['change_file_number'] += 1
                break;
    # 移动操作
    for module2, files2 in rsf2_map.items():
        # 找到对应的模块映射关系
        module1 = -1
        for key in res.keys():
            if module2 == key[1]:
                module1 = key[0]
                break
        if module1 != -1:
            for file_item in files2:
                if file_item not in rsf1_map[module1]:
                    first_version_module = -1
                    for first_module, files in rsf1_map.items():
                        if file_item in files:
                            first_version_module = first_module
                    moved.append((file_item, first_version_module, module2))
                    file_operation_change['file_information'].append({
                        "file_name": file_item,
                        "file_operation": "move",
                        "first_version_module_name": first_version_module,
                        "second_version_module_name": module2
                    })
                    moved_files.add(file_item)
                    for cluster in cluster_contain_file_info['cluster2_information']:
                        if cluster['module_name'] == module2:
                            cluster['change_file_number'] += 1
                    for cluster in cluster_contain_file_info['cluster1_information']:
                        if cluster['module_name'] == first_version_module:
                            cluster['change_file_number'] += 1
        # else:
        #     for file_item in files2:
        #         for first_module, files in rsf1_map.items():
        #             if file_item in files:
        #                 moved.append((file_item, first_module, module2))
        #                 moved_files.add(file_item)
    print("cluster_contain_file_info['cluster1_information']的长度:")
    print(len(cluster_contain_file_info['cluster1_information']))
    print("cluster_contain_file_info['cluster2_information']的长度:")
    print(len(cluster_contain_file_info['cluster2_information']))
    return added, removed, moved, added_files, removed_files, moved_files, file_operation_change,cluster_contain_file_info


# def file_operation_change(rsf_version1,rsf_version2,res,added_files,removed_files,moved_files):
#     pass


# 打印结果
def print_results(added, removed, moved):
    print("新增文件:")
    for file, module in added:
        print(f"文件: {file}, 模块: {module}")

    print("\n删除文件:")
    for file, module in removed:
        print(f"文件: {file}, 模块: {module}")

    print("\n移动文件:")
    for file, from_module, to_module in moved:
        print(f"文件: {file}, 从模块: {from_module} 移动到模块: {to_module}")


# 主程序
def file_change(rsf1_path, rsf2_path, res,cluster_contain_file_info_path,file_unit_operation_change_path):


    # 解析RSF文件
    if not os.path.exists(rsf1_path) or not os.path.exists(rsf2_path):
        print(f"RSF 文件路径错误: {rsf1_path} 或 {rsf2_path} 不存在")
        return

    rsf1_map = parse_rsf(rsf1_path)
    rsf2_map = parse_rsf(rsf2_path)

    # 比较文件并获取新增、删除和移动文件
    added, removed, moved ,added_files, removed_files, moved_files, file_unit_operation_change, cluster_contain_file_info=compare_files(rsf1_map, rsf2_map, res)
    save_json(cluster_contain_file_info, cluster_contain_file_info_path)
    save_json(file_unit_operation_change,  file_unit_operation_change_path)
    return added, removed, moved, added_files, removed_files, moved_files,file_unit_operation_change
    # 输出结果
    # print_results(added, removed, moved)

def save_json(updated_data, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, indent=4)
        print(f"已成功保存更新的JSON到 {output_file}")
    except Exception as e:
        print(f"保存JSON文件时出错: {e}")

# 脚本入口
# if __name__ == "__main__":
#     if len(sys.argv) != 4:
#         print("用法: python compare_files.py <rsf1文件路径> <rsf2文件路径> <模块映射文件路径>")
#     else:
#         rsf1_path = sys.argv[1]
#         rsf2_path = sys.argv[2]
#         res_json = sys.argv[3]
#         main(rsf1_path, rsf2_path, res_json)
