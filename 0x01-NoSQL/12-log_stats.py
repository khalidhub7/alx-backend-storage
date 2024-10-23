#!/usr/bin/env python3
"""Script that provides stats about Nginx logs stored in MongoDB"""

from pymongo import MongoClient


def log_stats():
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx

    # Number of logs
    log_count = nginx_collection.count_documents({})
    print(f"{log_count} logs")

    # Count for each method
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        method_count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    # Number of logs for GET /status
    status_count = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{status_count} status check")


if __name__ == "__main__":
    log_stats()
