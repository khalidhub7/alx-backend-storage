#!/usr/bin/env python3
""" pymongo basics """


def insert_school(
        mongo_collection, **kwargs):
    """
insert one document in a collection
    """
    result = mongo_collection.insert_one(
        kwargs)
    return result.inserted_id
