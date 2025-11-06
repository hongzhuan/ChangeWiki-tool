import os
import json

def merge_json_files(directory):
    merged_data = {"summary": []}

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                merged_data["summary"].extend(data.get("summary", []))

    return merged_data

def save_merged_json(data, output_filepath):
    with open(output_filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    input_directory = "e:\\XJTU\\胡杨林基金\\双周例会\\0320\\cef\\split_logs"
    output_filepath = "e:\\XJTU\\胡杨林基金\\双周例会\\0320\\cef\\cef_log.json"

    merged_data = merge_json_files(input_directory)
    save_merged_json(merged_data, output_filepath)

    print(f"Merged JSON saved to {output_filepath}")