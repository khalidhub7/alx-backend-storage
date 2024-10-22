#!/usr/bin/env python3
"""update topics where the name == name"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """update topics where the name == name"""
    return mongo_collection.find({"topics": topic})
