"""
test_contents_io.py
----------------------------------------
python test_contents_io.py /absolute/path/to/results/libuv-v1.44.2v1.48.0
"""
import sys
from pathlib import Path
from bson import ObjectId

# ↓ 引入刚才写好的封装
from database.contents import save_contents, get_content_by_path

# ***** 配置部分 *****
ANALYSIS_ID = ObjectId("6891fd9e0f29e140f9bdf467")   # 对应 analysis_records 的 _id
# ************************

def main():
    path = r"D:\Huawei\new\semarc_backend\results\cef-57356834"
    folder = Path(path).expanduser().resolve()
    if not folder.exists():
        print(f"[ERROR] 路径不存在: {folder}")
        sys.exit(1)

    # 1️⃣ 写入
    print(f"[save_contents] 扫描并写入: {folder}")
    save_contents(ANALYSIS_ID, str(folder))
    print("写入完成！\n")

    # 2️⃣ 列出刚才写入的前 5 个文档的 Path，供手动测试
    from database.db import analysis_contents_col
    sample_paths = analysis_contents_col.find(
        {"analysisId": ANALYSIS_ID},
        {"Path": 1}
    ).limit(5)
    print("示例 Path（任取一个用于查询）：")
    for doc in sample_paths:
        print("  -", doc["Path"])

    # 3️⃣ 交互式查询
    rel_path = input("\n请输入要查看的 Path（如上列表中的一条）> ").strip()
    if not rel_path:
        print("未输入，退出。")
        return

    text = get_content_by_path(str(ANALYSIS_ID), rel_path)
    if text is None:
        print("没有找到对应文档")
    else:
        print(f"\n====== 内容（前 500 字）======\n{text[:500]}")

if __name__ == "__main__":
    main()
