import os
from pymongo import MongoClient
import gridfs

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "semarc_db")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

# GridFS 实例
fs = gridfs.GridFS(db)

# 用户集合
users_col = db["users"]

# 保证用户名唯一
users_col.create_index("username", unique=True)

# 分析历史记录
analysis_records_col = db["analysis_records"]

# 分析历史记录的内容
analysis_contents_col = db["analysis_contents"]
