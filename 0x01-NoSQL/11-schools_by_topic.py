#!/usr/bin/env python3
""" pymongo basics """


def schools_by_topic(mongo_collection, topic):
    """ find by toobic """

    return list(mongo_collection.find(
        {'topics': {'$in': [topic]}}
    ))
