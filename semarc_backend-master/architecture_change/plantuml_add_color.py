import json

def update_plantuml_colors(plantuml_json_path, graph_json_path, output_path):
    # 读取GraphIDFunc_modify.json，建立name到color的映射
    with open(graph_json_path, 'r', encoding='utf-8') as f:
        graph_data = json.load(f)
    name2color = {item['name']: item['color'] for item in graph_data['structure'] if 'color' in item}

    # 读取plantuml_json_data.json，替换color
    with open(plantuml_json_path, 'r', encoding='utf-8') as f:
        plantuml_data = json.load(f)
    for comp in plantuml_data.get('components', []):
        for elem in comp.get('elements', []):
            if elem['name'] in name2color:
                elem['color'] = name2color[elem['name']]

    # 保存结果
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(plantuml_data, f, ensure_ascii=False, indent=2)

# 用法示例
# update_plantuml_colors('D:\\backend\\semarc_backend\\results\\libuv-v1.48.0\\libuv-v1.48.0_Plantuml_json_data.json',
#                        'D:\\backend\\semarc_backend\\results\\libuv-v1.48.0\\libuv-v1.48.0_GraphIDFunc_modify_add_component_cluster_color.json',
#                        'D:\\backend\\semarc_backend\\results\\libuv-v1.48.0\\test.json')