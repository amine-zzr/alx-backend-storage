#!/usr/bin/env python3
"""
Returns a list of schools having a specific topic.
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns a list of schools that have the specified topic.

    Args:
        mongo_collection: The pymongo collection object.
        topic (str): The topic to search for.

    Returns:
        A list of schools (documents) that include the topic.
    """
    return list(mongo_collection.find({"topics": topic}))
