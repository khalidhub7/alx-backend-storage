#!/usr/bin/env python3
"""Script that provides stats about Nginx logs stored in MongoDB"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError


def log_stats():
    try:
        # Connect to MongoDB with a timeout to ensure we handle connection
        # issues
        client = MongoClient(
            'mongodb://127.0.0.1:27017',
            serverSelectionTimeoutMS=5000)
        client.server_info()  # Force a call to check the connection
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"Unable to connect to the server: {e}")
        return

    # Get the database and collection
    db = client.get_database("logs")
    nginx_collection = db.get_collection("nginx")

    try:
        # Count total number of logs
        log_count = nginx_collection.count_documents({})
        print(f"{log_count} logs")

        # Count for each HTTP method
        print("Methods:")
        methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
        for method in methods:
            method_count = nginx_collection.count_documents({"method": method})
            print(f"\tmethod {method}: {method_count}")

        # Count documents with GET method and path `/status`
        status_count = nginx_collection.count_documents(
            {"method": "GET", "path": "/status"})
        print(f"{status_count} status check")

    except Exception as e:
        print(f"Error while fetching stats from the database: {e}")


if __name__ == "__main__":
    log_stats()
