#!/usr/bin/env python3
""" pymongo basics """


def schools_by_topic(mongo_collection, topic):
    """
search by topic
    """
    find = mongo_collection.find(
        {'topics': topic}
    )
    return find
