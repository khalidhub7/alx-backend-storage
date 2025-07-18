#!/usr/bin/env python3
""" pymongo basics """
from pymongo import MongoClient


def show_logs():
    """ shows nginx logs stats from mongodb """
    # make sure to restore backup
    # mongorestore dump

    # connect to logs.nginx collection
    client = MongoClient()
    db = client['logs']
    collection = db['nginx']

    # count all docs and GET /status logs
    docs_len = collection.count_documents({})
    status_check = collection.count_documents(
        {'path': {'$in': ['/status']}, 'method': 'GET'}
    )

    # count docs per HTTP method
    methods_count = {
        "GET": 0, "POST": 0, "PUT": 0, "PATCH": 0, "DELETE": 0
    }
    for k in methods_count:
        methods_count[k] = collection.count_documents(
            {'method': k}
        )

    # print log counts and method stats
    print(
        f"{docs_len} logs\n"
        f"Methods:"
    )
    for m in methods_count:
        print(f"    method {m}: {methods_count[m]}")
    print(f"{status_check} status check")

    # most present IPs in the collection
    top_ten = collection.aggregate([
        {'$group': {'_id': '$ip', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}}, {'$limit': 10}
    ])
    print('IPs:')
    for i in top_ten:
        print(f"    {i['_id']}: {i['count']}")


if __name__ == "__main__":
    show_logs()
