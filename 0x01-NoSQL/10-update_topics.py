#!/usr/bin/env python3
""" pymongo basics """


def update_topics(mongo_collection, name, topics):
    """ update user topics """
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
