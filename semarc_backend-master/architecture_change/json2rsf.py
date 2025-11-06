import json
import sys
import string
def json_to_rsf(json_file, rsf_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(rsf_file, 'w', encoding='utf-8') as f:
        for group in data['structure']:
            group_name = str(group['name'])
            for item in group['nested']:
                item_name = item['name']
                f.write(f"contain {group_name} {item_name}\n")
    return rsf_file
def format_name(name):
    """将空格替换为 '-'，确保 PlantUML 可以正确解析"""
    name =  name.replace(" ", "_")  # 将空格替换为 '-'
    name = name.replace("/", "_")
    return name.replace("-", "_")
#
# if len(sys.argv) !=3:
#     print("Usage: python json2rsf.py <input_reverse_json_file> <output_rsf_file>")
#     exit(0)
# reverse_json_file = sys.argv[1]
# out_json_file = sys.argv[2]
if __name__ == '__main__':
    # 使用示例
    json_file = 'D:\\SemArc_backend\\results\\libuv-v1.44.2\\libuv-v1.44.2_NamedClusters.json'
    rsf_file = 'D:\\SemArc_backend\\architecture_change\\libuv_144_rsf.rsf'
    reverse_json_file = json_file
    out_json_file = rsf_file
    json_to_rsf(reverse_json_file, out_json_file)