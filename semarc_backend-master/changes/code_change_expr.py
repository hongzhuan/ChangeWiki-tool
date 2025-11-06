from collections import defaultdict
from typing import List, Dict

from changes.entity import Entity


class FileHierarchyChange:
    def __init__(self, file: 'Entity'):
        # 初始化类的属性
        self.changed_child_entities: Dict['Entity', List['Entity']] = defaultdict(list)
        self.hierarchical_mst_change_results: Dict['Entity', str] = {}
        self.hierarchical_cst_change_results: Dict['Entity', str] = {}
        self.entity_has_changed: Dict['Entity', bool] = {}
        self.integer_entity_map: Dict[int, 'Entity'] = {}
        self.string_entity_map: Dict[str, 'Entity'] = {}
        self.file = file


class ChangeHierGroup:
    def __init__(self, language: str):
        self.language = language
        self.file_hierarchy_change_dict: Dict['Entity', 'FileHierarchyChange'] = {}
        self.file_name_dict: Dict[str, 'Entity'] = {}
