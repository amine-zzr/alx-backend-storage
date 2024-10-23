#!/usr/bin/env python3
""" 101-students """

from pymongo import MongoClient

def top_students(mongo_collection):
    """Returns a list of students sorted by average score.

    Args:
        mongo_collection: The pymongo collection object.

    Returns:
        A list of dictionaries containing students' names and their average scores.
    """
    # Aggregate the scores for each student and calculate the average
    pipeline = [
        {
            '$project': {
                'name': 1,
                'averageScore': {
                    '$avg': '$topics.score'
                }
            }
        },
        {
            '$sort': {
                'averageScore': -1  # Sort by average score in descending order
            }
        }
    ]
    
    return list(mongo_collection.aggregate(pipeline))
