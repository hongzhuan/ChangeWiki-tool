import json
def replace_plantuml_color_from_graphIDfunc_component_cluster(version1, version2, target_json):
    """
    将 version1 和 version2 中 cluster 的颜色同步到 target_json 中的 elements。
    """
    with open(version1) as f1, open(version2) as f2:
        version1 = json.load(f1)
        version2 = json.load(f2)
    
    # 1. 提取 cluster 颜色映射（两个版本可能都有）
    cluster_color_map = {}

    for item in version1.get("structure", []):
        if item.get("category") == "cluster":
            cluster_color_map[item["name"]] = item.get("color")

    for item in version2.get("structure", []):
        if item.get("category") == "cluster":
            cluster_color_map[item["name"]] = item.get("color")

    # 2. 更新 target_json 中 elements 的颜色
    for component in target_json.get("components", []):
        for element in component.get("elements", []):
            cluster_name = element.get("name")
            if cluster_name in cluster_color_map:
                element["color"] = cluster_color_map[cluster_name]

    return target_json
