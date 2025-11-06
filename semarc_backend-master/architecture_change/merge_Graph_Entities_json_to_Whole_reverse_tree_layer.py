import json

def merge_Graph_Entities_json_to_Whole_reverse_tree_layer(entities_file, graph_file, output_file):
    # 文件路径
    # entities_file = 'entites_changes_info.json'
    # graph_file = 'GraphIDFunc_modify_add_component_cluster_color.json'
    # output_file = 'merged_output.json'

    # 读取JSON文件
    with open(entities_file, 'r', encoding='utf-8') as f:
        entities = json.load(f)

    with open(graph_file, 'r', encoding='utf-8') as f:
        graph = json.load(f)

    # 构建文件名到id的映射
    file_name_to_id = {}
    for item in graph['structure']:
        if item.get('category', '').lower() == 'item' and 'name' in item:
            file_name_to_id[item['name']] = item['id']

    # 找到当前最大id
    max_id = max(item['id'] for item in graph['structure'])

    # 整合entities到graph格式
    new_items = []
    for idx, entity in enumerate(entities, start=1):
        if entity.get('entity_granularity') == 'File':
            continue
        file_name = entity.get('entity_file_name', '')
        parent_id = file_name_to_id.get(file_name,-1)  # 如果找不到对应的文件名，则跳过这个item
        if parent_id == -1:
            continue
        new_item = {
            'id': max_id + idx,
            'entity_id': entity.get('entity_id', ''),
            'name': entity.get('entity_name', ''),
            'category': entity.get('entity_granularity', ''),
            'parentId': parent_id,
            'parentName': file_name,
            'qualifiedName': entity.get('entity_name', ''),
            'entity_path': entity.get('entity_path', ''),
            'Functionality': entity.get('entity_path', ''),
            'color': 'yellow',
            'changes_num' : 1 # Functionality的
        }
        new_items.append(new_item)

    # 合并并写入新文件
    merged = {
        "architecture_pattern": graph.get("architecture_pattern"),
        "structure": graph["structure"] + new_items
    }
    #给merged内每个item添加一个新的属性changes_num, Item的值为包含的Functionality的changes_num之和 cluster的为包含items的changes_num之和 component的为包含clusters的changes_num之和
    # 先统计所有 item 的 changes_num
    for item in merged['structure']:
        if item['category'].lower() == 'item':
            item['changes_num'] = sum(
                sub_item.get('changes_num', 0) for sub_item in merged['structure']
                if sub_item.get('parentId') == item['id'] and sub_item['category'].lower() == 'function'
            )

    # 再统计所有 cluster 的 changes_num
    for item in merged['structure']:
        if item['category'].lower() == 'cluster':
            item['changes_num'] = sum(
                sub_item.get('changes_num', 0) for sub_item in merged['structure']
                if sub_item.get('parentId') == item['id'] and sub_item['category'].lower() == 'item'
            )

    # 最后统计所有 component 的 changes_num
    for item in merged['structure']:
        if item['category'].lower() == 'component':
            item['changes_num'] = sum(
                sub_item.get('changes_num', 0) for sub_item in merged['structure']
                if sub_item.get('parentId') == item['id'] and sub_item['category'].lower() == 'cluster'
            )

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    return merged
# 测试该函数
if __name__ == "__main__":
    entities_file = 'D:\\backend\\semarc_backend\\results\\libuv-v1.44.2v1.48.0\\code_changes\\libuv-0c1fa696aa502eb749c2c4735005f41ba00a27b8-e9f29cb984231524e3931aa0ae2c5dae1a32884e\\entities_changes_info.json'
    graph_file = 'D:\\backend\\semarc_backend\\results\\libuv-v1.44.2\\libuv-v1.44.2_GraphIDFunc_modify_add_component_cluster_color.json'
    output_file = 'merged_output.json'

    merged_file = merge_Graph_Entities_json_to_Whole_reverse_tree_layer(entities_file, graph_file, output_file)
    print(f"Merged JSON saved to {merged_file}")