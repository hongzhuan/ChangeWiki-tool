import json
import sys
def compare_plantuml_json_versions_diff(old_version, new_version):

    # try:
    #     # 读取原始JSON文件
    #     with open(old_version, 'r',encoding='utf-8') as f:
    #         old_version = json.load(f)
    # except Exception as e:
    #     print(f"加载JSON文件时出错: {e}")
    #     sys.exit(1)
    #     # 解析 JSON 结构
    # try:
    #     # 读取原始JSON文件
    #     with open(new_version, 'r',encoding='utf-8') as f:
    #         new_version = json.load(f)
    # except Exception as e:
    #     print(f"加载JSON文件时出错: {e}")
    #     sys.exit(1)
    #     # 解析 JSON 结构
    # print("new_version:")
    # print(new_version)
    # result = {
    #     "direction": "top to bottom",
    #     "components": [], "connections": new_version["connections"]}  # 直接保留最新版本的连接
    #
    # # 构建旧版和新版的组件字典
    # old_components = {comp["name"]: comp for comp in old_version["components"]}
    # new_components = {comp["name"]: comp for comp in new_version["components"]}
    # print(old_components)
    # print(new_components)
    # # 提取所有 components 的名称
    # all_component_names = set(old_components.keys()).union(set(new_components.keys()))
    #
    # # 旧版本所有 elements 对应的 component 名称（用于检测移动）
    # element_to_old_component = {}
    # element_to_new_component = {}
    # for comp_name, comp in old_components.items():
    #     for elem in comp.get("elements", []):
    #         element_to_old_component[elem["name"]] = comp_name
    # for comp_name, comp in new_components.items():
    #     for elem in comp.get("elements", []):
    #         element_to_new_component[elem["name"]] = comp_name
    # print("all_component_names")
    # print(all_component_names)
    # # 处理每个 component
    # for comp_name in all_component_names:
    #     old_elements = {el["name"]: el for el in old_components.get(comp_name, {}).get("elements", [])}
    #     new_elements = {el["name"]: el for el in new_components.get(comp_name, {}).get("elements", [])}
    #     print("old_elements")
    #     print(old_elements)
    #
    #     all_elements_names = set(old_elements.keys()).union(set(new_elements.keys()))
    #     elements_list = []
    #
    #     for elem_name in all_elements_names:
    #         if elem_name in old_elements and elem_name not in new_elements:
    #             # 旧版本有，新版本没有 -> 可能被删除或移动
    #             if elem_name in element_to_new_component:
    #                 elements_list.append({"name": elem_name, "color": "yellow"})  # 先默认标记为删除
    #             else:
    #                 elements_list.append({"name": elem_name, "color": "green"})  # 先默认标记为移动
    #         elif elem_name not in old_elements and elem_name in new_elements:
    #             # 新版本有，旧版本没有 -> 可能是新增或者移动
    #             old_component = element_to_old_component.get(elem_name)
    #             if old_component and old_component != comp_name:
    #                 # 在旧版存在，但从旧的 component 移动到了新的 component -> 标记为移动 (黄色)
    #                 elements_list.append({"name": elem_name, "color": "yellow"})
    #             else:
    #                 # 确实是新元素 -> 标记为新增 (红色)
    #                 elements_list.append({"name": elem_name, "color": "red"})
    #         else:
    #             # 在两个版本都存在 -> 颜色保持不变
    #             elements_list.append({"name": elem_name, "color": new_elements[elem_name]["color"]})
    #
    #     # 组件本身是否新增/删除
    #     if comp_name in old_components and comp_name not in new_components:
    #         # 旧版本有，新版本没有 -> 标记为删除（绿色）
    #         result["components"].append({"name": comp_name, "elements": elements_list, "color": "green"})
    #     elif comp_name not in old_components and comp_name in new_components:
    #         # 新版本有，旧版本没有 -> 标记为新增（红色）
    #         result["components"].append({"name": comp_name, "elements": elements_list, "color": "red"})
    #     else:
    #         # 组件本身没有变化
    #         result["components"].append({"name": comp_name, "elements": elements_list})
    #
    # return result
    with open(old_version, 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    with open(new_version, 'r', encoding='utf-8') as f:
        new_data = json.load(f)

    # 以新版本为基准，复制components
    new_components_dict = {comp['name']: {'name': comp['name'], 'elements': [dict(el) for el in comp.get('elements', [])]} for comp in new_data.get('components', [])}

    # 遍历旧版本，合并非yellow元素
    for old_comp in old_data.get('components', []):
        comp_name = old_comp['name']
        existing_elements = {el['name'] for el in new_components_dict[comp_name]['elements']}
        for el in old_comp.get('elements', []):
            if el['color'] == 'yellow':
                continue
            if el['name'] not in existing_elements:
                new_components_dict[comp_name]['elements'].append({'name': el['name'], 'color': el['color']})
                existing_elements.add(el['name'])

    result = {
        'direction': new_data.get('direction', 'top to bottom'),
        'components': list(new_components_dict.values()),
        'connections': new_data.get('connections', [])
    }
    return result
    # with open(output_path, 'w', encoding='utf-8') as f:
    #     json.dump(result, f, ensure_ascii=False, indent=2)

# 示例 JSON 版本
# old_json = {
#     "direction": "top to bottom",
#     "components": [
#         {
#             "name": "Plugin_System",
#             "elements": [
#                 {
#                     "name": "resource_management",
#                     "color": "lightblue"
#                 },
#                 {
#                     "name": "echo_event_loop",
#                     "color": "lightblue"
#                 },
#                 {
#                     "name": "handle_management",
#                     "color": "lightblue"
#                 }
#             ]
#         },
#         {
#             "name": "Error_Handling_and_Performance_Monitoring",
#             "elements": [
#                 {
#                     "name": "system_network_io",
#                     "color": "lightblue"
#                 },
#                 {
#                     "name": "async_request_handler",
#                     "color": "lightblue"
#                 }
#             ]
#         },
#         {
#             "name": "Thread_Pool_Management",
#             "elements": [
#                 {
#                     "name": "async_io_manager",
#                     "color": "lightblue"
#                 },
#                 {
#                     "name": "libuv_functionality_tests",
#                     "color": "lightblue"
#                 },
#                 {
#                     "name": "file_copy_test",
#                     "color": "lightblue"
#                 }
#             ]
#         },
#         {
#             "name": "Timers_and_Callbacks",
#             "elements": [
#                 {
#                     "name": "network_system_tests",
#                     "color": "lightblue"
#                 },
#                 {
#                     "name": "test_libuv_fork",
#                     "color": "lightblue"
#                 }
#             ]
#         },
#         {
#             "name": "Asynchronous_I_O_Operations",
#             "elements": [
#                 {
#                     "name": "event_loop_watchers",
#                     "color": "lightblue"
#                 }
#             ]
#         },
#         {
#             "name": "Event_Loop_Management",
#             "elements": [
#                 {
#                     "name": "pipe_connection_preparation",
#                     "color": "lightblue"
#                 }
#             ]
#         }
#     ],
#     "connections": [
#         {
#             "from": "resource_management",
#             "to": "system_network_io",
#             "hidden": true
#         },
#         {
#             "from": "async_request_handler",
#             "to": "pipe_connection_preparation",
#             "hidden": true
#         },
#         {
#             "from": "file_copy_test",
#             "to": "async_request_handler",
#             "hidden": true
#         },
#         {
#             "from": "network_system_tests",
#             "to": "echo_event_loop",
#             "hidden": true
#         },
#         {
#             "from": "event_loop_watchers",
#             "to": "test_libuv_fork",
#             "hidden": true
#         },
#         {
#             "from": "pipe_connection_preparation",
#             "to": "libuv_functionality_tests",
#             "hidden": true
#         }
#     ]
# }
#
# new_json = {
#     "components": [
#         {
#             "name": "Event_Loop",
#             "elements": [
#                 {"name": "libuv_new-core", "color": "lightblue"},
#                 {"name": "libuv_Core_Functionality_and_Platform-Specific_Tests", "color": "lightblue"},
#                 {"name": "New-Feature-Module", "color": "lightblue"}  # 新增的元素
#             ]
#         },
#         {
#             "name": "Networking",
#             "elements": [
#                 {"name": "TCP_Connection", "color": "lightblue"},
#                 {"name": "Legacy-Component", "color": "lightblue"}  # 从 "Event_Loop" 移动到这里
#             ]
#         },
#         {
#             "name": "hahha",
#             "elements": [
#                 {"name": "TCPn", "color": "lightblue"},
#                 {"name": "Legaponent", "color": "lightblue"}  # 从 "Event_Loop" 移动到这里
#             ]
#         }
#     ],
#     "connections": [
#         {"from": "libuv_new-core", "to": "TCP_Connection"}
#     ]
# }

# 运行对比
# old_json ="D:\\backend\\semarc_backend\\results\\libuv-v1.44.2\\test.json"
# new_json = "D:\\backend\\semarc_backend\\results\\libuv-v1.48.0\\test.json"
# result_json = compare_plantuml_json_versions_diff(old_json, new_json)
#
# # 输出结果
# print(result_json)
# print(json.dumps(result_json, indent=4, ensure_ascii=False))
