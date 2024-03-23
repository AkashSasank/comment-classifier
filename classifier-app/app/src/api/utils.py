from typing import Union, List
from ..schemas.classifier import Comment, CommentInfo


def filter_comments(comments: List[Comment],
                    start_time: Union[None, int] = 0,
                    end_time: Union[None, int] = None
                    ) -> List[Comment]:
    """
    Filter comments based on start time and end time
    """
    filtered_comments = comments
    if start_time and end_time:
        start_time, end_time = abs(start_time), abs(end_time)
        if start_time > end_time:
            start_time, end_time = end_time, start_time
    if start_time and end_time:
        filtered_comments = list(filter(lambda x: start_time <= x.created_at <= end_time, comments))
    if start_time and not end_time:
        filtered_comments = list(filter(lambda x: start_time <= x.created_at, comments))
    if not start_time and end_time:
        filtered_comments = list(filter(lambda x: x.created_at <= end_time, comments))
    return filtered_comments


def order_comments(comments: List[CommentInfo],
                   order_by: Union[List, None] = None
                   ) -> List[CommentInfo]:
    """Sort comments"""
    if order_by:
        for i in order_by:
            if i == "score":
                comments.sort(key=lambda x: x.score)
            if i == "-score":
                comments.sort(key=lambda x: x.score, reverse=True)
    return comments
