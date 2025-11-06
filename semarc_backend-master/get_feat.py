import json

def filter_feat_commits(input_filepath, output_filepath):
    """
    筛选出 type 为 feat 和 fix 的提交，并按照类型排序：
    feat 类型在前，fix 类型在后。
    """
    with open(input_filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # 筛选出 feat 和 fix 类型的提交
    feat_commits = [commit for commit in data.get("summary", []) if commit.get("type") == "feat"]
    fix_commits = [commit for commit in data.get("summary", []) if commit.get("type") == "fix"]
    
    # 按顺序合并 feat 和 fix 提交
    sorted_commits = feat_commits + fix_commits
    
    # 构造输出数据
    filtered_data = {"summary": sorted_commits}
    
    # 保存到输出文件
    with open(output_filepath, 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, ensure_ascii=False, indent=4)

def split_commits_by_type(input_filepath, feat_output_filepath, other_output_filepath):
    """
    将 commit_log JSON 文件拆分为两个 JSON 文件：
    一个包含 type 为 feat 的提交，另一个包含其他类型的提交。
    """
    with open(input_filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # 筛选出 type 为 feat 的提交
    feat_commits = [commit for commit in data.get("summary", []) if commit.get("type") == "feat"]
    
    # 筛选出其他类型的提交
    other_commits = [commit for commit in data.get("summary", []) if commit.get("type") != "feat"]
    
    # 保存 feat 提交到文件
    with open(feat_output_filepath, 'w', encoding='utf-8') as file:
        json.dump({"feat": feat_commits}, file, ensure_ascii=False, indent=4)
    
    # 保存其他类型的提交到文件
    with open(other_output_filepath, 'w', encoding='utf-8') as file:
        json.dump({"other": other_commits}, file, ensure_ascii=False, indent=4)

    print(f"Feat commits saved to {feat_output_filepath}")
    print(f"Other commits saved to {other_output_filepath}")

if __name__ == "__main__":
    input_filepath = "D:\\semantic_analysis\\results\\cef\\cef_log.json"
    feat_output_filepath = "D:\\semantic_analysis\\results\\cef\\cef_featfix_log.json"
    other_output_filepath = "D:\\semantic_analysis\\results\\cef\\cef_other_log.json"
    
    # split_commits_by_type(input_filepath, feat_output_filepath, other_output_filepath)
    filter_feat_commits(input_filepath, feat_output_filepath)