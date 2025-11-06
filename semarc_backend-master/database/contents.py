"""
database/contents.py
------------------------------------------------
把本地 results/... 文件批量写入 analysis_contents，
并提供按 Path 查询 content 的工具函数。
"""
import os
from datetime import datetime, timedelta, timezone

import gridfs
from bson.objectid import ObjectId
from pymongo import InsertOne

from database.db import analysis_contents_col, fs, analysis_records_col

# 北京时区对象
beijing_tz = timezone(timedelta(hours=8))

# 文件大小阈值（15MB）
MAX_DOCUMENT_SIZE = 15 * 1024 * 1024

# 1. 把整个 result_dir 写入 MongoDB
def save_contents(analysis_id: ObjectId, base_folder: str,) -> None:
    """
    遍历 base_folder（如 results/libuv-v1.44.2v1.48.0），
    将所有文件存入 analysis_contents。
    """
    bulk_ops = []

    # 提取 prefix：base_folder 最后一级目录名
    prefix = os.path.basename(base_folder)  # 如 "libuv-v1.44.2v1.48.0"

    # 清理之前的数据（包括GridFS文件）
    _cleanup_analysis_data(analysis_id)

    for root, _, files in os.walk(base_folder):
        for fname in files:
            path_on_disk = os.path.join(root, fname)
            # 相对路径  Path 字段
            # rel_path = os.path.relpath(path_on_disk, os.path.dirname(base_folder))
            # 相对于 results 根目录的路径，保留子目录层级
            rel_path = os.path.relpath(path_on_disk, os.path.dirname(base_folder))

            # 只保存以这个子目录名开头的路径
            if not rel_path.startswith(prefix + os.sep):
                continue

            abs_path = os.path.abspath(path_on_disk)
            # 使用长路径前缀解决 Windows 260 字符限制
            if os.name == 'nt' and len(abs_path) >= 260:
                if not abs_path.startswith('\\\\?\\'):
                    path_on_disk = '\\\\?\\' + abs_path

            # 读取文件内容（按 utf-8 尝试；失败则跳过）
            try:
                with open(path_on_disk, "r", encoding="utf-8") as f:
                    content = f.read()
                    # 在 try-except 块中添加更详细的错误处理
            except UnicodeDecodeError as e:
                print(f"编码错误，跳过文件: {rel_path}, 错误: {e}")
                continue
            except FileNotFoundError as e:
                print(f"文件未找到: {rel_path}, 完整路径: {path_on_disk}, 错误: {e}")
                continue
            except PermissionError as e:
                print(f"权限错误: {rel_path}, 错误: {e}")
                continue
            except Exception as e:
                print(f"读取文件时发生未知错误: {rel_path}, 错误类型: {type(e).__name__}, 错误: {e}")
                continue

            # 检查内容大小
            content_size = len(content.encode('utf-8'))

            if content_size > MAX_DOCUMENT_SIZE:
                # 使用GridFS存储大文件
                file_id = fs.put(
                    content.encode('utf-8'),
                    filename=f"{analysis_id}_{rel_path}",
                    analysisId=analysis_id,
                    originalPath=rel_path,
                    contentType="text/plain"
                )

                bulk_ops.append(
                    InsertOne({
                        "analysisId": ObjectId(analysis_id),
                        "Path": rel_path,
                        "gridfs_file_id": file_id,
                        "storage_type": "gridfs",
                        "file_size": content_size,
                        "content": '',  # GridFS存储时不需要 content 字段
                        "createdAt": datetime.now(beijing_tz)
                    })
                )
            else:
                # 正常存储小文件
                bulk_ops.append(
                    InsertOne({
                        "analysisId": ObjectId(analysis_id),
                        "Path": rel_path,
                        "content": content,
                        "storage_type": "document",
                        "file_size": content_size,
                        "createdAt": datetime.now(beijing_tz)
                    })
                )

    if bulk_ops:
        # analysis_contents_col.delete_many({"analysisId": ObjectId(analysis_id)})
        analysis_contents_col.bulk_write(bulk_ops)
        print(f"[analysis_contents] inserted {len(bulk_ops)} docs for {analysis_id}")

# 2. 根据 analysisId + Path 取 content
def get_content_by_path(analysis_id: str, rel_path: str) -> str | None:
    """
    返回指定 Path 的内容；不存在则返回 None
    支持从GridFS读取大文件
    """
    # doc = analysis_contents_col.find_one(
    #     {"analysisId": ObjectId(analysis_id), "Path": rel_path},
    #     {"content": 1}
    # )
    # return doc["content"] if doc else None
    doc = analysis_contents_col.find_one(
        {"analysisId": ObjectId(analysis_id), "Path": rel_path}
    )

    if not doc:
        return None

    if doc.get("storage_type") == "gridfs":
        # 从GridFS读取
        try:
            gridfs_file = fs.get(doc["gridfs_file_id"])
            return gridfs_file.read().decode('utf-8')
        except gridfs.errors.NoFile:
            return None
    else:
        # 从文档字段读取
        return doc.get("content")


def _cleanup_analysis_data(analysis_id: ObjectId) -> None:
    """清理指定分析ID的所有数据，包括GridFS文件"""
    # 查找所有GridFS文件并删除
    gridfs_docs = analysis_contents_col.find(
        {"analysisId": analysis_id, "storage_type": "gridfs"},
        {"gridfs_file_id": 1}
    )

    for doc in gridfs_docs:
        if "gridfs_file_id" in doc:
            try:
                fs.delete(doc["gridfs_file_id"])
            except gridfs.errors.NoFile:
                pass  # 文件已被删除，忽略错误

    # 删除集合中的记录
    analysis_contents_col.delete_many({"analysisId": ObjectId(analysis_id)})

if __name__ == "__main__":
    # # 测试用例
    test_analysis_id = ObjectId("688c8b4ca574dafc81121440")
    content = get_content_by_path(str(test_analysis_id), "libuv-v1.44.2v1.48.0\libuv_Event Loop Management_component_report.md")
    print(content if content else "未找到内容")

    # aid = ObjectId("688c8b4ca574dafc81121440")
    # rec = analysis_records_col.find_one(
    #     {"_id": ObjectId(aid)},
    #     {"projectName": 1, "version1": 1, "version2": 1}
    # )
    # if not rec:
    #     print(f"未找到分析记录: {aid}")
    #
    # project = rec["projectName"]
    # v1 = rec["version1"]
    # v2 = rec["version2"]
    #
    # base_results = r"D:\xjtu-enre\new\semarc_backend\results"
    #
    # # 只遍历这三条子目录
    # folders = [
    #     f"{project}-{v1}",
    #     f"{project}-{v2}",
    #     f"{project}-{v1}{v2}"
    # ]
    # # 针对每个子目录，都把它写入 db
    # for sub in folders:
    #     full = os.path.join(base_results, sub)
    #     if os.path.isdir(full):
    #         save_contents(aid, full)
    #
    # print("ok")


