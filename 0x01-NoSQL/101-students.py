#!/usr/bin/env python3
""" pymongo basics """


def top_students(mongo_collection):
    """ students sorted by average score desc """

    result = mongo_collection.aggregate([
        # per document
        {"$project": {
            "averageScore": {"$avg": "$topics.score"},
            "_id": 1, "name": 1, "topics": 1
        }},
        # after all docs are processed
        {'$sort': {'averageScore': -1}}
    ])
    return result
