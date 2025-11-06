from flask import request, jsonify
from database.db import users_col


def register_user():
    """注册接口：username + password + email；密码 ≥ 6 位；用户名唯一"""
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    email    = data.get("email", "").strip()

    # 基本校验
    if not username or not password or not email:
        return jsonify({"message": "所有字段不能为空"}), 400
    if len(password) < 6:
        return jsonify({"message": "密码长度不能少于6位"}), 400
    if users_col.find_one({"username": username}):
        return jsonify({"message": "用户名已存在"}), 409

    users_col.insert_one({
        "username": username,
        "password": password,   # 明文存储
        "email":    email,
        "is_admin": False
    })
    return jsonify({"message": "注册成功，请登录"}), 201


def login_user():
    """登录接口"""
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"message": "用户名和密码不能为空"}), 400

    user = users_col.find_one({"username": username})
    if not user or user["password"] != password:
        return jsonify({"message": "用户名或密码错误"}), 401

    return jsonify({
        "message":  "登录成功",
        "username": username,
        "uid": str(user["_id"]),
        "is_admin": user["is_admin"]
    }), 200
