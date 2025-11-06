from typing import Dict


from changes.entity import Entity
from changes.read_changes_group_info import CodeChangeInput
from llm.input_expr import EntityInput


class EntityOrder:
    def __init__(self, code_change_input: CodeChangeInput):
        self.order = []
        self.code_change_input = code_change_input
        self.current_file_order = []
        self.entity_input_map: Dict['Entity', 'EntityInput'] = {}

    def build_entity_map_order(self):
        self.build_entity_input_map()
        self.build_entity_input_hier_order()

    def build_entity_input_map(self):
        for file_item in self.code_change_input.change_hier_group.file_hierarchy_change_dict.keys():
            print("file: " + file_item.file_name)

            entity_input = EntityInput(file_item)
            entity_input.url = self.code_change_input.url
            entity_input.is_commit = True
            entity_input.entity_path  = self.code_change_input.change_hier_group.file_hierarchy_change_dict.get(file_item).hierarchical_cst_change_results[file_item]

            self.entity_input_map[file_item] = entity_input
            current_file_hier_change = self.code_change_input.change_hier_group.file_hierarchy_change_dict.get(file_item)

            for i in current_file_hier_change.integer_entity_map.keys():
                if current_file_hier_change.integer_entity_map.get(i).entity_granularity == 'Function':

                    sub_entity = current_file_hier_change.integer_entity_map.get(i)
                    print("func: " + sub_entity.entity_name + "aaaaa")
                    # if file_item.file_name == 'tools/sk_app/Window.h' and sub_entity.entity_name == 'visitLayers':
                    #     print("test")
                    self.current_file_order.append(sub_entity)

                    sub_entity_input = EntityInput(sub_entity)
                    sub_entity_input.url = self.code_change_input.url
                    sub_entity_input.is_commit = True
                    sub_entity_input.commitMessage = self.code_change_input.commitMessage
                    sub_entity_input.entity_path = current_file_hier_change.hierarchical_cst_change_results[sub_entity]
                    self.entity_input_map[sub_entity] = sub_entity_input
                    self.order.append(sub_entity)

            self.order.append(file_item)



    def build_entity_input_hier_order(self):
        function_order = []
        classDecl_order = []
        class_order = []
        file_order = []
        for entity in self.order:
            if entity.entity_granularity == 'Function':
                function_order.append(entity)
            elif entity.entity_granularity == 'ClassDeclaration':
                classDecl_order.append(entity)
            elif entity.entity_granularity == 'Class':
                class_order.append(entity)
            elif entity.entity_granularity == 'File':
                file_order.append(entity)
        self.order = []
        self.order = function_order + class_order + file_order




