#!/usr/bin/env python3
""" 10-main """
from pymongo import MongoClient
list_all = __import__('8-all').list_all
update_topics = __import__('10-update_topics').update_topics

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school
    update_topics(
        school_collection, "ALX", ["Sys admin", "AI", "Algorithm"]
    )

    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {} {}".format(school.get('_id'),
                                  school.get('name'),
                                  school.get('topics', "")))

    update_topics(school_collection, "ALX", ["iOS"])

    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {} {}".format(school.get('_id'),
                                  school.get('name'),
                                  school.get('topics', "")))
