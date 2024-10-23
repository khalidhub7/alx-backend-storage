#!/usr/bin/env python3
"""
Python script that provides some stats
about Nginx logs stored in MongoDB
"""
import pymongo
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError
if __name__ == "__main__":
    try:
        myclient = pymongo.MongoClient(
            "mongodb://127.0.0.1:27017",
            serverSelectionTimeoutMS=5000)
        mydb = myclient.logs
        mycol = mydb.nginx
        myclient.admin.command('ping')
        print("{} logs".format(mycol.count_documents({})))
        print("Methods:")
        methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
        for m in methods:
            print("\tmethod {}: {}".format(
                m, mycol.count_documents({"method": m})))
        print("{} status check".format(mycol.count_documents(
            {"method": "GET", "path": "/status"})))
    except (ServerSelectionTimeoutError, PyMongoError):
        print("Error: Unable to connect to MongoDB.")
