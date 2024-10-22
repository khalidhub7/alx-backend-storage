#!/usr/bin/env python3
""" basics """
from pymongo import MongoClient
client = MongoClient()
db = client.logs
collection = db.nginx
log_count = collection.count_documents({})
print(f"{log_count} logs")
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
print("Methods:")
for method in methods:
    count = collection.count_documents({"method": method})
    print(f"\tmethod {method}: {count}")
status_check = collection.count_documents({"method": "GET", "path": "/status"})
print(f"{status_check} status check")
