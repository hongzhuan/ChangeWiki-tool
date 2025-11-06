import json
import os
import re
from typing import List

from changes.code_change_expr import ChangeHierGroup, FileHierarchyChange
from changes.entity import Entity



class CodeChangeInput:
    def __init__(self, root_save_path: str, change_hier_group: 'ChangeHierGroup', repo_name: str, before_version: str,
                 after_version: str, changes_root_path: str, language: str):
        # 初始化类的属性
        self.root_save_path = root_save_path
        self.change_hier_group = change_hier_group
        self.repo_name = repo_name
        self.before_version = before_version
        self.after_version = after_version
        self.changes_root_path = changes_root_path
        self.language = language

        self.url = ""
        self.isCommit = True
        self.commitMessage = ""


        # 当前的粒度和文件、类、函数信息
        self.current_mst_granularity = None
        self.current_file = None
        self.current_class = None
        self.current_class_declaration = None
        self.current_function = None
        self.current_function_internal = None

    def read_changes_info(self):
        self.change_hier_group.language = self.language
        self.read_changed_entities()
        self.read_file_changes()
        print('test')

    def read_changed_entities(self):
        # print(self.changes_root_path)
        with open(self.changes_root_path.replace("\\", "/") + '/changesEntities.json', 'r', encoding='utf-8') as f:
            changes_entities_data = json.load(f)
        # 所有文件遍历，创建文件变更层级结构
        for item in changes_entities_data:
            entity = Entity(item)
            if entity.entity_granularity == 'File':
                self.change_hier_group.file_hierarchy_change_dict[entity] = FileHierarchyChange(entity)
                self.change_hier_group.file_name_dict[entity.file_name] = entity
                current_file_hier_change = self.change_hier_group.file_hierarchy_change_dict[entity]
                current_file_hier_change.integer_entity_map[entity.entity_id] = entity
                current_file_hier_change.string_entity_map[entity.node_string_info] = entity

        # 所有实体遍历，存入文件变更层级结构
        for item in changes_entities_data:
            entity = Entity(item)
            if entity.entity_granularity == 'File':
                continue
            file_name = entity.file_name
            file_entity = self.change_hier_group.file_name_dict[file_name]
            if file_entity in self.change_hier_group.file_hierarchy_change_dict:
                current_file_hier_change = self.change_hier_group.file_hierarchy_change_dict[file_entity]
                current_file_hier_change.integer_entity_map[entity.entity_id] = entity
                current_file_hier_change.string_entity_map[entity.node_string_info] = entity
            else:
                print("error")
        # 构建实体树
        for item in changes_entities_data:
            temp_entity = Entity(item)

            if temp_entity.entity_granularity == 'File':
                continue
            file_name = temp_entity.file_name
            file_entity = self.change_hier_group.file_name_dict[file_name]
            current_file_hier_change = self.change_hier_group.file_hierarchy_change_dict[file_entity]
            parent_entity = current_file_hier_change.integer_entity_map[temp_entity.parent_id]
            entity  = current_file_hier_change.integer_entity_map[temp_entity.entity_id]
            current_file_hier_change.changed_child_entities[parent_entity].append(entity)

    @staticmethod
    def sanitize_file_name(name: str):
        if name is None:
            return ""
        # print(name)
        return (re.sub(r'[:<>|?*]', '__', name).replace("::", "__").
                replace("~","-"))

    def path_synthesis(self):
        try:
            # 确保根路径存在
            if not hasattr(self, 'changes_root_path') or not self.changes_root_path:
                return "error_path: changes_root_path not set"

            # 创建带长路径前缀的基础路径
            base_path = f"\\\\?\\{self.changes_root_path}".replace('/', '\\')

            if self.change_hier_group.language == "c":
                file_part = self.sanitize_file_name(self.current_file)
                if not file_part:
                    return "error_path: invalid file name"

                if self.current_mst_granularity == "File":
                    return f"{base_path}\\{file_part}"
                elif self.current_mst_granularity == "Function":
                    func_part = self.sanitize_file_name(self.current_function)
                    if not func_part:
                        return "error_path: invalid function name"
                    return f"{base_path}\\{file_part}\\{func_part}"
                elif self.current_mst_granularity == "Function_Internal":
                    func_part = self.sanitize_file_name(self.current_function)
                    internal_part = self.sanitize_file_name(self.current_function_internal)
                    if not func_part or not internal_part:
                        return "error_path: invalid function/internal name"
                    return f"{base_path}\\{file_part}\\{func_part}\\{internal_part}"

            elif self.change_hier_group.language == "c++":
                file_part = self.sanitize_file_name(self.current_file)
                if not file_part:
                    return "error_path: invalid file name"

                path_builder = f"{base_path}\\{file_part}"

                if self.current_mst_granularity == "File":
                    return path_builder

                elif self.current_mst_granularity == "Class":
                    class_part = self.sanitize_file_name(self.current_class)
                    if class_part:
                        path_builder += f"\\class--{class_part}"
                    return path_builder

                elif self.current_mst_granularity == "ClassDeclaration":
                    classDecl_part = self.sanitize_file_name(self.current_class_declaration)
                    if classDecl_part:
                        path_builder += f"\\classDecl--{classDecl_part}"
                    return path_builder

                elif self.current_mst_granularity == "Function":
                    class_part = self.sanitize_file_name(self.current_class)
                    if class_part:
                        path_builder += f"\\class--{class_part}"

                    func_part = self.sanitize_file_name(self.current_function)
                    if not func_part:
                        return "error_path: invalid function name"
                    return f"{path_builder}\\func--{func_part}"

                elif self.current_mst_granularity == "Function_Internal":
                    class_part = self.sanitize_file_name(self.current_class)
                    if class_part:
                        path_builder += f"\\class--{class_part}"

                    func_part = self.sanitize_file_name(self.current_function)
                    if not func_part:
                        return "error_path: invalid function name"
                    path_builder += f"\\func--{func_part}"

                    internal_part = self.sanitize_file_name(self.current_function_internal)
                    if internal_part:
                        path_builder += f"\\{internal_part}"
                    return path_builder

            return "error_path: unsupported granularity or language"

        except Exception as e:
            return f"error_path: {str(e)}"

    def get_func_path_string(self, func_entity: Entity):
        return func_entity.entity_name + "-(" + func_entity.before_begin_line + "," + func_entity.after_begin_line + ")"

    def set_current(self, changed_entity: Entity):
        granularity = changed_entity.entity_granularity

        if granularity == "Class":
            self.current_class = changed_entity.entity_name
        elif granularity == "ClassDeclaration":
            self.current_class_declaration = changed_entity.local_name
        elif granularity == "Function":
            self.current_function = self.get_func_path_string(changed_entity)
        elif granularity == "Function_Internal":
            self.current_function_internal = changed_entity.entity_name

        self.current_mst_granularity = granularity

    def clear_current_entity(self, changed_entity: Entity):
        granularity = changed_entity.entity_granularity

        if granularity == "Class":
            self.current_class = None
        elif granularity == "ClassDeclaration":
            self.current_class_declaration = None
        elif granularity == "Function":
            self.current_function = None
        elif granularity == "Function_Internal":
            self.current_function_internal = None



    def clear_current(self):
        self.current_class = None
        self.current_class_declaration = None
        self.current_function = None
        self.current_function_internal = None
        self.current_mst_granularity = None

    def read_file_changes(self):
        for changed_file in self.change_hier_group.file_hierarchy_change_dict.keys():
            self.clear_current()
            file_hierarchy_change = self.change_hier_group.file_hierarchy_change_dict.get(changed_file)

            self.current_file = changed_file.file_name.replace("/", "----")
            self.current_mst_granularity = "File"
            current_path = self.path_synthesis()
            file_hierarchy_change.hierarchical_cst_change_results[changed_file] = current_path
            if self.change_hier_group.language== "c":
                self.read_hier_changes(changed_file, file_hierarchy_change)
            elif self.change_hier_group.language == "c++":
                self.read_hier_changes(changed_file, file_hierarchy_change)

    def read_hier_changes(self, changed_parent_entity: 'Entity', file_hierarchy_change: 'FileHierarchyChange'):
        if changed_parent_entity not in file_hierarchy_change.changed_child_entities or \
                not file_hierarchy_change.changed_child_entities[changed_parent_entity]:
            return
        for item in file_hierarchy_change.changed_child_entities[changed_parent_entity]:
            self.set_current(item)
            if self.current_mst_granularity == "Function_Internal":
                path = self.path_synthesis()
                file_hierarchy_change.hierarchical_mst_change_results[item] = self.path_synthesis()
                file_hierarchy_change.entity_has_changed[item] = self.is_exist_changes_json(path)
            else:
                path = self.path_synthesis()
                file_hierarchy_change.hierarchical_cst_change_results[item] = self.path_synthesis()
                file_hierarchy_change.entity_has_changed[item] = self.is_exist_changes_json(path)
                self.read_hier_changes(item, file_hierarchy_change)
            self.clear_current_entity(item)

    @staticmethod
    def is_exist_changes_json(path):
        return os.path.isfile(path + "/changes.json") or os.path.isfile(path + "/changes.txt")











# 测试用
def main():
    # code_change_input = CodeChangeInput('D:/my/intern/mlccd/changeHierOut/rapid2',
    #                                   ChangeHierGroup('c'), 'libuv', '6d0d4a3',
    #                                   '8f32a14',
    #                                   'D:/my/intern/mlccd/changeHierOut/rapid2/libuv-6d0d4a3-8f32a14',
    #                                   'c')
    code_change_input = CodeChangeInput('D:/my/intern/mlccd/changeHierOut/rapid1',
                                        ChangeHierGroup('c++'), 'skia', '20164f3',
                                        '84d9fd6',
                                        'D:/my/intern/mlccd/changeHierOut/rapid1/skia-20164f3-84d9fd6',
                                        'c++')
    code_change_input.read_changes_info()
if __name__ == '__main__':
    main()


