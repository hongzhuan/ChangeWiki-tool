def component_cluster_add_color(version1, version2, mapping_file_path):
    """
    比较两个版本的 component 和 cluster，并根据映射关系更新 color 字段。
    """
    #读取json文件

    def parse_cluster_mapping(path):
        mapping = {}
        with open(path, 'r') as f:
            for line in f:
                # v1, v2, _ = line.strip().split(',')
                v1, v2, _ = line.strip().split('#')
                if v1 != '-1':
                    mapping[v1] = v2 if v2 != '-1' else None
        return mapping

    cluster_mapping = parse_cluster_mapping(mapping_file_path)

    v1_components = {item['id']: item for item in version1["structure"] if item['category'] == 'component'}
    v2_components = {item['id']: item for item in version2["structure"] if item['category'] == 'component'}

    v1_clusters = {item['name']: item for item in version1["structure"] if item['category'] == 'cluster'}
    v2_clusters = {item['name']: item for item in version2["structure"] if item['category'] == 'cluster'}

    # 1. Component comparison
    v1_comp_names = {comp['name'] for comp in v1_components.values()}
    v2_comp_names = {comp['name'] for comp in v2_components.values()}
    all_comp_names = v1_comp_names | v2_comp_names

    for comp_name in all_comp_names:
        in_v1 = any(c['name'] == comp_name for c in v1_components.values())
        in_v2 = any(c['name'] == comp_name for c in v2_components.values())
        if in_v1 and not in_v2:
            for c in v1_components.values():
                if c['name'] == comp_name:
                    c['color'] = 'red'
        elif in_v2 and not in_v1:
            for c in v2_components.values():
                if c['name'] == comp_name:
                    c['color'] = 'green'
        # both: no change

    # 2. Cluster -> Component name
    def get_cluster_to_component_name(structure, components_by_id):
        return {
            item['name']: components_by_id[item['parentId']]['name']
            for item in structure if item['category'] == 'cluster' and item['parentId'] in components_by_id
        }

    v1_cluster_to_comp = get_cluster_to_component_name(version1['structure'], v1_components)
    v2_cluster_to_comp = get_cluster_to_component_name(version2['structure'], v2_components)

    marked_clusters_v1 = set()
    marked_clusters_v2 = set()

    # 3. Compare clusters from version1
    for cluster_name, v1_cluster in v1_clusters.items():
        mapped = cluster_mapping.get(cluster_name)
        if mapped is None or mapped not in v2_clusters:
            v1_cluster['color'] = 'red'
            marked_clusters_v1.add(cluster_name)
        else:
            v2_cluster = v2_clusters[mapped]
            comp1 = v1_cluster_to_comp.get(cluster_name)
            comp2 = v2_cluster_to_comp.get(mapped)
            if comp1 == comp2:
                v1_cluster['color'] = 'blue'
                v2_cluster['color'] = 'blue'
            else:
                v1_cluster['color'] = 'yellow'
                v2_cluster['color'] = 'yellow'
            marked_clusters_v1.add(cluster_name)
            marked_clusters_v2.add(mapped)

    # 4. Mark unmarked version2 clusters as green (新增)
    for cluster_name, v2_cluster in v2_clusters.items():
        if cluster_name not in marked_clusters_v2:
            v2_cluster['color'] = 'green'

    # 5. Mark unmarked version1 clusters as blue (默认保留)
    for cluster_name, v1_cluster in v1_clusters.items():
        if cluster_name not in marked_clusters_v1:
            v1_cluster['color'] = 'blue'

    return version1, version2

#测试该函数
def main():
    version1 = {
        "architecture_pattern": "pattern1",
        "structure": [
            {"id": "c1", "name": "Component1", "category": "component"},
            {"id": "c2", "name": "Component2", "category": "component"},
            {"name": "Cluster1", "category": "cluster", "parentId": "c1"},
            {"name": "Cluster2", "category": "cluster", "parentId": "c2"}
        ]
    }

    version2 = {
        "architecture_pattern": "pattern2",
        "structure": [
            {"id": "c1", "name": "Component1", "category": "component"},
            {"id": "c3", "name": "Component3", "category": "component"},
            {"name": "Cluster1", "category": "cluster", "parentId": "c1"},
            {"name": "Cluster3", "category": "cluster", "parentId": "c3"}
        ]
    }

    mapping_file_path = 'D:\\backend\\semarc_backend\\results\\jianshi-v1.0\\jianshi-v1.0_v1.0_v2.0_a2a_mapping_weight.txt'  # 假设映射文件路径
    #version1和version2是两个版本的JSON文件路径





    updated_v1, updated_v2 = component_cluster_add_color(version1, version2, mapping_file_path)
    print(updated_v1)
    print(updated_v2)
