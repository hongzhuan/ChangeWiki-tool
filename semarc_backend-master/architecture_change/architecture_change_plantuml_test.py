import json
from architecture_change.convert_json_to_plantuml import convert_json_to_plantuml
import sys

def load_mapping(mapping_file):
    old_to_new = {}
    new_to_old = {}
    with open(mapping_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 2:
                old, new = parts[0], parts[1]
                if old != '-1' and new != '-1':
                    old_to_new[old] = new
                    new_to_old[new] = old
                elif old == '-1' and new != '-1':
                    new_to_old[new] = None  # 新增
                elif new == '-1' and old != '-1':
                    old_to_new[old] = None  # 删除
    return old_to_new, new_to_old

def load_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def collect_module_component_map(json_data):
    module_to_component = {}
    for comp in json_data.get('components', []):
        comp_name = comp['name']
        for element in comp.get('elements', []):
            module_to_component[element['name']] = comp_name
            print(element['name'], comp_name)
    return module_to_component

def generate_new_json(old_json_path, new_json_path, mapping_file_path, output_path):
    #add---red delete---green  move--yellow  unchange---lightblue
    old_json = load_json(old_json_path)
    new_json = load_json(new_json_path)
    old_to_new, new_to_old = load_mapping(mapping_file_path)

    old_module_to_component = collect_module_component_map(old_json)
    new_module_to_component = collect_module_component_map(new_json)

    old_component_names = {comp['name'] for comp in old_json.get('components', [])}
    new_component_names = {comp['name'] for comp in new_json.get('components', [])}

    result = {"components": [], "connections": new_json.get('connections', [])}

    # 1. 处理新版的组件
    for comp in new_json['components']:
        comp_name = comp['name']
        comp_info = {"name": comp_name, "elements": []}

        # 判断组件颜色
        if comp_name not in old_component_names:
            comp_info["color"] = "red"
        else:
            comp_info["color"] = "lightblue"

        for el in comp.get('elements', []):
            el_name = el['name']

            if el_name not in new_to_old:
                # 完全新增的模块
                color = "red"
            elif new_to_old[el_name] is None:
                # 新增模块（在映射文件里）
                color = "red"
            else:
                mapped_old_module = new_to_old[el_name]
                if mapped_old_module in old_module_to_component:
                    old_comp_of_module = old_module_to_component[mapped_old_module]
                    if old_comp_of_module != comp_name:
                        color = "yellow"  # 移动了
                    else:
                        color = "lightblue"  # 映射正确
                else:
                    color = "yellow"  # 找不到映射到旧模块的组件（也算变化）

            comp_info["elements"].append({"name": el_name, "color": color})

        result["components"].append(comp_info)

    # 2. 处理旧版存在但新版不存在的模块
    deleted_modules = []
    for old_module in old_module_to_component:
        if old_module not in old_to_new:
            # 完全删除
            deleted_modules.append(old_module)
        elif old_to_new[old_module] is None:
            # 删除（在映射文件里）
            deleted_modules.append(old_module)

    deleted_component_to_modules = {}
    for m in deleted_modules:
        comp = old_module_to_component[m]
        deleted_component_to_modules.setdefault(comp, []).append(m)

    for comp_name, modules in deleted_component_to_modules.items():
        comp_info = {
            "name": comp_name,
            "color": "green",
            "elements": [{"name": m, "color": "green"} for m in modules]
        }
        result["components"].append(comp_info)

    # 3. 处理旧版存在但新版完全不存在的组件
    deleted_components = old_component_names - new_component_names
    for comp_name in deleted_components:
        if comp_name not in deleted_component_to_modules:
            # 组件整体删除但没有单独模块删除
            comp_info = {
                "name": comp_name,
                "color": "green",
                "elements": []
            }
            result["components"].append(comp_info)

    # 保存输出
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    

    old_json_path = "D:\\SemArc_backend\\results\\libuv-v1.44.2\\libuv-v1.44.2_Plantuml_json_data.json"
    new_json_path = "D:\\SemArc_backend\\results\\libuv-v1.48.0\\libuv-v1.48.0_Plantuml_json_data.json"
    mapping_file_path = "D:\\SemArc_backend\\results\\libuv-v1.44.2\\libuv-v1.44.2_2.0.12_2.0.13_a2a_mapping_weight.txt"
    output_path = "output_test.json"
    output_path_version1 = "D:\\SemArc_backend\\results\\libuv-v1.44.2\\libuv-v1.44.2_Plantuml_json_data"
    output_path_version2 = "D:\\SemArc_backend\\results\\libuv-v1.48.0\\libuv-v1.48.0_Plantuml_json_data"
    convert_json_to_plantuml(old_json_path,output_path_version1)
    convert_json_to_plantuml(new_json_path, output_path_version2)
    generate_new_json(old_json_path, new_json_path, mapping_file_path, output_path)
