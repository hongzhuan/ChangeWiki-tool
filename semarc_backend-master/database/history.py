# database/history.py

from flask import request, jsonify
from bson.objectid import ObjectId
from datetime import datetime, timedelta, timezone
from database.db import users_col, analysis_records_col

# 定义北京时间时区（UTC+8）
beijing_tz = timezone(timedelta(hours=8))


def _to_beijing(dt):
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(beijing_tz)


def get_history(username: str):
    """
    返回带 projectName, analysisFolder 的历史列表
    """
    user = users_col.find_one({"username": username})
    if not user:
        return jsonify([])

    records = analysis_records_col.find(
        {"userId": user["_id"]}
    ).sort("createdAt", -1)

    data = []
    for r in records:
        # 从记录中读取新字段
        project_name = r.get("projectName", r["projectUrl"].split("/")[-1])
        analysis_folder = r.get("analysisFolder",
                                f"{project_name}-{r['version1']}{r['version2']}")

        # title = f"{project_name}  {r['version1']} → {r['version2']}"
        title = f'{r["projectUrl"]}  {r["version1"]} -> {r["version2"]}'
        ts = _to_beijing(r["createdAt"]).strftime("%Y-%m-%d %H:%M")

        data.append({
            "id": str(r["_id"]),
            "projectName": project_name,
            "analysisFolder": analysis_folder,
            "title": title,
            "time": ts
        })

    return jsonify(data)


def add_history():
    """
    新增分析记录，写入 projectName 和 analysisFolder
    前端 JSON = { username, projectUrl, version1, version2, domainKnowledge }
    """
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    user = users_col.find_one({"username": username})
    if not user:
        return jsonify({"message": "用户不存在"}), 404

    project_url = data.get("projectUrl", "")
    project_name = project_url.rstrip("/").split("/")[-1].replace(".git", "")
    v1 = data.get("version1", "")
    v2 = data.get("version2", "")

    doc = {
        "userId": user["_id"],
        "projectUrl": project_url,
        "projectName": project_name,
        "version1": v1,
        "version2": v2,
        "domainKnowledge": data.get("domainKnowledge", ""),
        "createdAt": datetime.now(beijing_tz)
    }
    res = analysis_records_col.insert_one(doc)

    # title = f"{project_name}  {v1} → {v2}"
    title = f'{doc["projectUrl"]}  {doc["version1"]} -> {doc["version2"]}'
    ts = doc["createdAt"].strftime("%Y-%m-%d %H:%M")

    return jsonify({
        "id": str(res.inserted_id),
        "projectName": project_name,
        "title": title,
        "time": ts
    }), 201

def get_history_by_id(record_id: str):
    rec = analysis_records_col.find_one({"_id": ObjectId(record_id)})
    if not rec:
        return jsonify({"error": "记录不存在"}), 404

    # 将原本Object类型的_id转换为字符串，将createdAt类型的时间转换为北京时间
    rec["id"] = str(rec["_id"])
    rec.pop("_id")

    rec["userId"] = str(rec["userId"])

    rec["time"] = _to_beijing(rec["createdAt"]).strftime("%Y-%m-%d %H:%M")
    rec.pop("createdAt")

    # 返回rec中的所有字段
    return jsonify(rec), 200
    # return rec

if __name__ == "__main__":
    results = get_history_by_id('688b2b6a8d9e68157f06ea36')
    print(results["userId"])
