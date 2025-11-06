import json
import sys


def json_to_puml(json_file,write_file):
    sort_data = {}
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data['api_methods']:
            if (item['src_module'],item['dest_module']) not in sort_data.keys():
                sort_data[item['src_module'],item['dest_module']] = item['weight']
            else:
                sort_data[item['src_module'],item['dest_module']] += item['weight']
        sort_data = sorted(sort_data.items(), key=lambda x: x[1], reverse=True)
    with open(write_file, 'w', encoding='utf-8') as f:
        for item in sort_data:
            f.write(f"[{item[0][0]}] --> [{item[0][1]}]: {item[1]}\n")



if len(sys.argv) !=3:
    print("Usage: python json_to_puml.py <input_reverse_json_file> <output_rsf_file>")
    exit(0)
reverse_json_file = sys.argv[1]
out_json_file = sys.argv[2]
# 使用示例
# json_file = 'C:\\Users\\23100\Desktop\论文\胡杨林基金\openharmony\\5.0.1_cluster_result.json'
# rsf_file = 'C:\\Users\\23100\Desktop\论文\胡杨林基金\openharmony\\arkui_5.0.1_out-cluster-result.rsf'
json_to_puml(reverse_json_file, out_json_file)