#!/usr/bin/env python3
""" pymongo basics """
import pymongo


def update_topics(
        mongo_collection, name, topics):
    """
changes all topics of a document
based on name
    """
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
