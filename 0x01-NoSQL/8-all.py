#!/usr/bin/env python3
""" pymongo basics """
from typing import List


def list_all(
        mongo_collection) -> List[dict]:
    """ lists all documents in a collection """
    docs = []
    for i in mongo_collection.find():
        docs.append(i)
    if len(docs) == 0:
        return []
    else:
        return docs
