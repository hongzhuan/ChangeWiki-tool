import json

def get_code_diff(entity_name, entity_file_name, json_path):
    before_code = ""
    after_code = ""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for item in data:
        if item.get('entity_name') == entity_name and item.get('entity_file_name') == entity_file_name:
            before_code = item.get('before_code')
            after_code = item.get('after_code')
    return before_code, after_code