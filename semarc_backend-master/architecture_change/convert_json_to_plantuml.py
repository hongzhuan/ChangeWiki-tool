import json
import sys
import random

def format_name(name):
    """将空格替换为 '-'，确保 PlantUML 可以正确解析"""
    name =  name.replace(" ", "_")  # 将空格替换为 '-'
    name = name.replace("/", "_")
    return name.replace("-", "_")

def convert_json_to_plantuml(json_data,output_file):
    plantuml_data = {
        "direction": "top to bottom",
        "components": [],
        "connections": []
    }
    all_elements = {}  # 存储所有组件的 elements
    try:
        # 读取原始JSON文件
        with open(json_data, 'r',encoding='utf-8') as f:
            json_data = json.load(f)
    except Exception as e:
        print(f"加载JSON文件时出错: {e}")
        sys.exit(1)
        # 解析 JSON 结构



    for component in json_data.get("structure", []):
        if component.get("@type") == "component":
            component_name = format_name(component["name"])  # 处理名称（加双引号）
            elements = [{"name": format_name(cluster["name"]), "color": "lightblue"}
                        for cluster in component.get("nested", [])
                        if cluster.get("@type") == "cluster"]

            # 存储当前组件的 elements
            all_elements[component_name] = [e["name"] for e in elements]

            # 组件加入 components
            plantuml_data["components"].append({"name": component_name, "elements": elements})

        # 生成 connections（不同组件之间的 element 连接）
    component_names = list(all_elements.keys())

    for i, comp_name in enumerate(component_names):
        if not all_elements[comp_name]:  # 如果当前组件没有 elements，跳过
            continue

        caller = random.choice(all_elements[comp_name])  # 当前组件的某个 element 作为调用者

        # 选择一个不同的组件
        other_components = [c for c in component_names if c != comp_name and all_elements[c]]
        if not other_components:
            continue  # 如果没有可用的其他组件，跳过

        target_comp = random.choice(other_components)  # 选一个不同的组件
        callee = random.choice(all_elements[target_comp])  # 选一个目标组件的 element 作为被调用者

        plantuml_data["connections"].append({"from": caller, "to": callee,  "hidden":True})
    print("plantuml_data:")
    print(plantuml_data)
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(plantuml_data, f, indent=4)
        print(f"已成功保存更新的JSON到 {output_file}")
    except Exception as e:
        print(f"保存JSON文件时出错: {e}")
    return plantuml_data


# 示例 JSON 数据
# json_input = {
#     "@schemaVersion": "1.0",
#     "name": "clustering",
#     "structure": [
#         {
#             "@type": "component",
#             "name": "Event Loop",
#             "nested": [
#                 {"@type": "cluster", "name": "libuv_new-core"},
#                 {"@type": "cluster", "name": "libuv_new Core Functionality and Platform-Specific Tests"},
#                 {"@type": "cluster", "name": "Cross-Platform Test Execution Framework"}
#             ]
#         }
#     ]
# }
#
# 运行转换
# plantuml_output = convert_json_to_plantuml(json_input)
#
# # 输出结果
# print(json.dumps(plantuml_output, indent=4, ensure_ascii=False))
