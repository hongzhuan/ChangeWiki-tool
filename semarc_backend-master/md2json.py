import re
import json
import shutil

def correct_json_format(json_str):
    """
    尝试修复 JSON 字符串中的常见问题：
    - 修复无效的转义字符
    - 添加缺失的双引号
    - 移除多余的逗号
    """
    # 修复无效的转义字符
    json_str = re.sub(r'\\([^"\\/bfnrtu])', r'\\\\\1', json_str)
    
    # 添加缺失的双引号
    json_str = re.sub(r'(?<!")(\b[a-zA-Z_][a-zA-Z0-9_]*\b)(?=\s*:)', r'"\1"', json_str)
    
    # 移除多余的逗号
    json_str = re.sub(r',\s*}', '}', json_str)
    json_str = re.sub(r',\s*]', ']', json_str)
    
    return json_str

def force_extract_json_candidates(md_content):
    # 粗暴抽取所有可能的json大块
    pattern = r'\{[\s\S]+?\}'
    return [m.group(0) for m in re.finditer(pattern, md_content)]

def fix_common_json_issues(json_str):
    # 修复常见json格式问题
    # 1. 大括号数量不匹配，尝试补齐
    lcount, rcount = json_str.count("{"), json_str.count("}")
    if lcount > rcount:
        json_str = json_str + "}" * (lcount - rcount)
    elif rcount > lcount:
        json_str = "{" * (rcount - lcount) + json_str

    # 2. 替换非标准引号、删除奇怪的标点
    json_str = json_str.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    # 3. 删除可能出现的多余逗号
    json_str = re.sub(r',\s*([\]}])', r'\1', json_str)
    # 4. json字段前加引号
    json_str = re.sub(r'(?<=\{|\[|,)\s*([a-zA-Z_][a-zA-Z0-9_ ]*)\s*:', lambda m: '"' + m.group(1).strip().replace(' ', '_') + '":', json_str)
    return json_str

def robust_extract_json_blocks_from_markdown(md_content):
    """
    最健壮的提取方式：先正则找```json块，解析失败则强行找大括号，再修补
    """
    # 1. 优先找markdown格式```json...```块
    pattern = r'```json(.*?)```'
    matches = re.findall(pattern, md_content, re.DOTALL)
    candidates = matches if matches else []
    # 2. 若无候选，再全局找大括号
    if not candidates:
        candidates = force_extract_json_candidates(md_content)
    json_blocks = []
    for candidate in candidates:
        candidate = candidate.strip()
        # 多轮修正与尝试解析
        for _ in range(3):
            try:
                json_data = json.loads(candidate)
                json_blocks.append(json_data)
                break
            except Exception as e:
                # 尝试自动修复
                candidate = fix_common_json_issues(candidate)
    return json_blocks

def extract_json_blocks_from_markdown(md_content):
    # 定义匹配JSON数据的正则表达式
    pattern = r'```json(.*?)```'
    
    # 使用re.DOTALL标志以匹配多行内容
    matches = re.finditer(pattern, md_content, re.DOTALL)
    
    json_blocks = []
    
    for match in matches:
        # 获取匹配到的JSON字符串
        json_str = match.group(1)
        
        try:
            # 尝试直接解析
            json_data = json.loads(json_str)
            json_blocks.append(json_data)
        except json.JSONDecodeError:
            # 如果解析失败，尝试修复格式
            corrected_json_str = correct_json_format(json_str)
            try:
                json_data = json.loads(corrected_json_str)
                json_blocks.append(json_data)
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
                print(f"原始JSON字符串: {json_str}")
                print(f"修复后JSON字符串: {corrected_json_str}")

    if not json_blocks:
        print("未找到匹配的JSON数据块")
    
    return json_blocks

def extract_json_blocks_from_markdown_file(md_file_path):
    # 读取Markdown文件内容
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 调用提取JSON数据的函数
    return extract_json_blocks_from_markdown(md_content)

def save_json_blocks_to_file(json_blocks, json_file_path):
    # 将所有JSON数据合并到一个summary中
    combined_summary = []
    for block in json_blocks:
        if isinstance(block, dict) and "summary" in block:
            combined_summary.extend(block["summary"])
    
    # 创建最终的JSON结构
    final_json = {
        "summary": combined_summary
    }

    # 将JSON数据写入JSON文件
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(final_json, json_file, ensure_ascii=False, indent=4)

def save_json_blocks_module_names(json_blocks, json_file_path):
    combined_summary = []
    for block in json_blocks:
        if isinstance(block, dict) and "modules" in block:
            combined_summary.extend(block["modules"])
    
    # 创建最终的JSON结构
    final_json = {
        "modules": combined_summary
    }

    # 将JSON数据写入JSON文件
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(final_json, json_file, ensure_ascii=False, indent=4)

def save_json_blocks_no_summary(json_blocks, json_file_path): 
    """
    For JSON files without 'summary' field, extract 'architecture pattern' and 'components'
    and save them into a simplified structure without merging 'indicators'.
    """
    # Create a simplified structure without 'summary'
    simplified_json = []

    for block in json_blocks:
        if isinstance(block, dict):
            architecture_pattern = block.get("architecture pattern", "Unknown")
            components = block.get("components", [])
            components_summary = []
            
            for component in components:
                component_name = component.get("name", "Unnamed")
                nested_indicators = component.get("nested", [])
                components_summary.append({
                    "name": component_name,
                    "nested": nested_indicators  # Keep 'nested' structure intact
                })

            simplified_json.append({
                "architecture_pattern": architecture_pattern,
                "components": components_summary
            })

    # Save the simplified JSON structure to file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        # Write without the outer list
        json.dump(simplified_json[0], json_file, ensure_ascii=False, indent=4)

def md2json_sum(md_file_path, json_file_path):
    json_blocks = extract_json_blocks_from_markdown_file(md_file_path)

    save_json_blocks_to_file(json_blocks, json_file_path)
    print(f"JSON数据（代码语义信息）已保存到文件: {json_file_path}")

    # if json_blocks:
    #     print(json_blocks)
    # else:
    #     print("无法提取或解析JSON数据。")

# def md2json(md_file_path, json_file_path):
#     json_blocks = extract_json_blocks_from_markdown_file(md_file_path)
#     save_json_blocks_no_summary(json_blocks, json_file_path)
#     print(f"JSON数据（架构语言信息）已保存到文件: {json_file_path}")

#     if json_blocks:
#         print(json_blocks)
#     else:
#         print("无法提取或解析JSON数据。")

def md2json(md_file_path, json_file_path):
    # 用增强版robust_extract_json_blocks_from_markdown替代原有逻辑
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    json_blocks = robust_extract_json_blocks_from_markdown(md_content)
    # 依然使用原有的save_json_blocks_no_summary逻辑
    if json_blocks:
        save_json_blocks_no_summary(json_blocks, json_file_path)
        print(f"JSON数据（架构语言信息）已保存到文件: {json_file_path}")
    if not json_blocks:
    # 可以直接copy一份本地预置合规json覆盖，或留空让后续流程兜底
        shutil.copy('.\\arch_pattern_layered.json', json_file_path)
    pass

def md2json_name(md_file_path, json_file_path):
    json_blocks = extract_json_blocks_from_markdown_file(md_file_path)
    save_json_blocks_module_names(json_blocks, json_file_path)
    print(f"JSON数据（架构语言信息）已保存到文件: {json_file_path}")

    if json_blocks:
        print(json_blocks)
    else:
        print("无法提取或解析JSON数据。")

def save_commit_log_json_blocks(json_blocks, json_file_path):
    combined_summary = []
    for block in json_blocks:
        if isinstance(block, dict) and "summary" in block:
            combined_summary.extend(block["summary"])
    
    # 创建最终的JSON结构
    final_json = {
        "summary": combined_summary
    }

    # 将JSON数据写入JSON文件
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(final_json, json_file, ensure_ascii=False, indent=4)

def md2json_commit_log(md_file_path, json_file_path):
    json_blocks = extract_json_blocks_from_markdown_file(md_file_path)
    save_commit_log_json_blocks(json_blocks, json_file_path)
    print(f"JSON数据（commit log）已保存到文件: {json_file_path}")

    if json_blocks:
        print(json_blocks)
    else:
        print("无法提取或解析JSON数据。")

# 用法示例
# json_file_path = "D:\\SemArc\\results\\pandas\\pandas_CodeSem.json"
# md_file_path = "D:\gpt_academic-master\gpt_academic-master\gpt_log\default_user\shared\pandas-ds-v2.md"
# md2json_sum(md_file_path, json_file_path)