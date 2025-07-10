#!/usr/bin/env python3
""" pymongo basics """


def insert_school(mongo_collection, **kwargs):
    """ insert new doc """
    return mongo_collection.insert_one(
        {**kwargs}
    ).inserted_id
