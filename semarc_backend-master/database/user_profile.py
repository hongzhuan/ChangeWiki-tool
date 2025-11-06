"""
用户信息读取 / 更新接口
"""
from flask import request, jsonify
from bson.objectid import ObjectId
from database.db import users_col


def get_user(username: str):
    """返回 {username, email}"""
    user = users_col.find_one({"username": username}, {"_id": 0, "username": 1, "email": 1})
    if not user:
        return jsonify({"message": "用户不存在"}), 404
    # 若 email 字段不存在则返回空字符串
    user.setdefault("email", "")
    return jsonify(user)


def update_user(username: str):
    """
    JSON = { newUsername, newPassword, newEmail }
      - newPassword 可为空（代表不修改）
    """
    data = request.get_json(silent=True) or {}
    new_u = data.get("newUsername", "").strip()
    new_p = data.get("newPassword", "").strip()
    new_e = data.get("newEmail", "").strip()

    if not new_u or not new_e:
        return jsonify({"message": "用户名和邮箱不能为空"}), 400

    # 检查邮箱格式（简单正则）
    import re
    if not re.match(r"^[\w\-]+(\.[\w\-]+)*@[\w\-]+(\.[\w\-]+)+$", new_e):
        return jsonify({"message": "邮箱格式不正确"}), 400

    # 查原用户
    user = users_col.find_one({"username": username})
    if not user:
        return jsonify({"message": "用户不存在"}), 404

    # 若改了用户名，检查是否重名
    if new_u != username and users_col.find_one({"username": new_u}):
        return jsonify({"message": "用户名已存在"}), 409

    update_doc = {"username": new_u, "email": new_e}
    if new_p:
        update_doc["password"] = new_p   # 明文存储，与你当前逻辑保持一致

    users_col.update_one({"_id": user["_id"]}, {"$set": update_doc})
    return jsonify({"message": "更新成功"}), 200
