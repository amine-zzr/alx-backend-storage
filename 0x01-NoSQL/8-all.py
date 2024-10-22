#!/usr/bin/env python3
"""
Lists all documents in a MongoDB collection.
"""


def list_all(mongo_collection):
    """
    Returns a list of all documents in the given collection.
    If no documents exist, returns an empty list.
    
    Args:
        mongo_collection: The pymongo collection object.

    Returns:
        A list of documents in the collection or an empty list if none.
    """
    return list(mongo_collection.find())
