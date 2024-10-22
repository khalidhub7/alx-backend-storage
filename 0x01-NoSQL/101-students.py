#!/usr/bin/env python3
"""List all documents in Python """
import pymongo


def top_students(mongo_collection):
    """averageScore"""
    stus = mongo_collection.find()
    sorted_stud = []
    for s in stus:
        sum = 0
        average = {}
        average = s
        for t in s["topics"]:
            sum += t["score"]
        average["averageScore"] = sum / len(s["topics"])
        sorted_stud.append(average)
    return sorted(sorted_stud, key=lambda x: x["averageScore"], reverse=True)
