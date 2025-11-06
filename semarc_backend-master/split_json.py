import json
import os

def split_json_file(input_filepath, output_directory, group_size=20):
    with open(input_filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    feature_commits = data.get("fix", [])
    total_commits = len(feature_commits)
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for i in range(0, total_commits, group_size):
        split_data = {"fix": feature_commits[i:i + group_size]}
        output_filepath = os.path.join(output_directory, f"libuv_fix_log_part_{i // group_size + 1}.json")
        
        with open(output_filepath, 'w', encoding='utf-8') as output_file:
            json.dump(split_data, output_file, ensure_ascii=False, indent=4)
        
        print(f"Saved {output_filepath}")

if __name__ == "__main__":
    input_filepath = "e:\\XJTU\\胡杨林基金\\双周例会\\0320\\libuv_new\\libuv_fix_log.json"
    output_directory = "e:\\XJTU\\胡杨林基金\\双周例会\\0320\\libuv_new\\split_fix_logs"
    
    split_json_file(input_filepath, output_directory)