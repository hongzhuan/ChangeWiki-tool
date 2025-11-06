import json
import sys

# 读取文件内容并返回文件列表
def read_file(file_path):
    try:
        with open(file_path, 'r',encoding='utf-8') as f:
            # 假设每行是一个文件路径
            return set(f.read().splitlines())
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return set()

# 更新JSON数据，检查是否需要添加color字段或删除项
def update_json(json_file, output_file,add_files, remove_files, moved_files):
    updated_data = {
    "architecture_pattern": '',
        "structure": []
    }
    try:
        # 读取原始JSON文件
        with open(json_file, 'r',encoding='utf-8') as f:
            json_data = json.load(f)
    except Exception as e:
        print(f"加载JSON文件时出错: {e}")
        sys.exit(1)
    updated_data['architecture_pattern'] = json_data['architecture_pattern']
    for item in json_data['structure']:
        if item['category'] == 'item':  # 仅处理 category 为 item 的项
            if item['name'] in add_files:
                item['color'] = 'red'  #    新增文件 红色
            elif item['name'] in remove_files:
                item['color'] = 'yellow'  # 删除文件 黄色
            elif item['name'] in moved_files:
                item['color'] = 'green'  #  移动文件 绿色
            else:
                item['color'] = 'blue'  #  其他文件 蓝色
            updated_data['structure'].append(item)
            continue  # 跳过不在文件列表中的项
        else:
            item['color'] = 'blue'
            updated_data['structure'].append(item)
    # output_file = 'C:\\Users\\23100\\Desktop\\backend\\semarc_backend\\architecture_change\\updated_structure.json'
    save_json(updated_data, output_file)
    return updated_data

# 保存更新后的JSON数据
def save_json(updated_data, output_file):
    try:
        with open(output_file, 'w',encoding='utf-8') as f:
            json.dump(updated_data, f, indent=4)
        print(f"已成功保存更新的JSON到 {output_file}")
    except Exception as e:
        print(f"保存JSON文件时出错: {e}")

# 主程序
# def main():
#     if len(sys.argv) != 5:
#         print("用法: python script.py <json文件> <add_file> <remove_file> <moved_file>")
#         sys.exit(1)
#
#     json_file = sys.argv[1]
#     add_file = sys.argv[2]
#     remove_file = sys.argv[3]
#     moved_file = sys.argv[4]
#
#     try:
#         # 读取原始JSON文件
#         with open(json_file, 'r') as f:
#             json_data = json.load(f)
#     except Exception as e:
#         print(f"加载JSON文件时出错: {e}")
#         sys.exit(1)
#
#     # 读取文件列表
#     add_files = read_file(add_file)
#     remove_files = read_file(remove_file)
#     moved_files = read_file(moved_file)
#
#     # 更新JSON数据
#     updated_data = update_json(json_data, add_files, remove_files, moved_files)
#
#     # 保存更新后的数据到新文件
#     save_json(updated_data, 'updated_' + json_file)
#
# # 脚本入口
# if __name__ == "__main__":
#     main()
