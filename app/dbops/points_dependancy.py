"""
Dependancies for calculating points
"""
import math


def reduce_points(points, request):
    """
    Reduce points if request is completed
    """
    if(request.completed_date>request.due_date):
        points = points - 5
    return points


def get_points(request):
    """
    Calculate points for an activity based on the date
    """
    duration = request.due_date - request.assign_date
    weeks = math.ceil(duration.days / 7)
    points = weeks * 5

    if(request.completed_date):
        points = reduce_points(points, request)
        
    return points