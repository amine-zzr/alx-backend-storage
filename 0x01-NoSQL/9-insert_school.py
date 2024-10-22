#!/usr/bin/env python3
"""
Inserts a new document in a MongoDB collection based on kwargs.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document into the given MongoDB collection.

    Args:
        mongo_collection: The pymongo collection object.
        **kwargs: The fields to be included in the new document.

    Returns:
        The new document's _id.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
