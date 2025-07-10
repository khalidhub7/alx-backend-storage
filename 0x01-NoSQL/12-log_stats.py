#!/usr/bin/env python3
""" pymongo basics """
from pymongo import MongoClient


def show_logs():
    """ shows nginx logs stats from mongodb """

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
        f"Methods:\n"
        f"\tmethod GET: {methods_count['GET']}\n"
        f"\tmethod POST: {methods_count['POST']}\n"
        f"\tmethod PUT: {methods_count['PUT']}\n"
        f"\tmethod PATCH: {methods_count['PATCH']}\n"
        f"\tmethod DELETE: {methods_count['DELETE']}\n"
        f"{status_check} status check"
    )


if __name__ == "__main__":
    show_logs()
