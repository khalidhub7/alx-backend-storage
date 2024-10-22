#!/usr/bin/env python3
"""
Python script that provides some stats
about Nginx logs stored in MongoDB
"""

import pymongo
if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    mydb = myclient.logs
    mycol = mydb.nginx

    print("{} logs".format(mycol.count_documents({})))
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    for m in methods:
        print("\tmethod {}: {}".format(m, mycol.count_documents({"method": m})))

    print("{} status check".format(
        mycol.count_documents({"method": "GET", "path": "/status"})))
