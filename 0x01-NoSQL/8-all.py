#!/usr/bin/env python3
""" pymongo basics """


def list_all(mongo_collection):
    """ return all docs from a collection """

    """ client = MongoClient()  # use default host, port
    db = client['test']  # test is default db
    collection = db[mongo_collection]  # my collection """

    return list(mongo_collection.find())  # all docs
