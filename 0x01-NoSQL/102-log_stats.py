#!/usr/bin/env python3
"""
Python script that provides some stats
about Nginx logs stored in MongoDB
"""

import pymongo
from collections import Counter

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
    print("IPs:")

    mydocs = mycol.find()
    counting_dict = {}
    for key in mydocs:
        ip = key["ip"]
        if ip in counting_dict:
            continue
        counting_dict[ip] = mycol.count_documents({"ip": ip})

    val_to_key = {}
    for key, val in counting_dict.items():
        val_to_key[val] = key
    myKeys = list(val_to_key.keys())
    myKeys.sort(reverse=True)

    for i in range(10):
        print(f"\t{val_to_key[myKeys[i]]}: {myKeys[i]}")
