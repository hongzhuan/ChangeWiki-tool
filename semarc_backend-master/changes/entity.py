from enum import Enum


class MstGranularity(Enum):
    FILE = "File"
    CLASS = "Class"
    FUNCTION = "Function"
    FUNCTION_INTERNAL = "Function_Internal"


class Entity:

    def __init__(self, data: dict):
        self.entity_id = data["entityId"]
        self.entity_granularity = data["entityGranularity"]
        self.entity_name = data["entityName"]
        self.file_name = data["fileName"]
        self.parent_id = data["parentId"]
        self.internal_group_id = data["internalGroupId"]
        self.node_string_info = data["nodeStringInfo"]
        self.parameters = data["parameters"]
        self.before_begin_line = data["beforeBeginLine"]
        self.after_begin_line = data["afterBeginLine"]
        self.before_end_line = data["beforeEndLine"]
        self.after_end_line = data["afterEndLine"]
        self.local_name = data["localName"]

    def __hash__(self):
        return hash((self.entity_id, self.entity_name))