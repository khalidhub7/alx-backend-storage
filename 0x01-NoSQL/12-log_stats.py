#!/usr/bin/env python3
"""Log stats"""
import pymongo


if __name__ == "__main__":
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    count_logs = nginx_collection.count_documents({})
    print(f"{count_logs} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        method_count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    status_check_count = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")
