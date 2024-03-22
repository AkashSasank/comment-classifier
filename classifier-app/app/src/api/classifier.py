"""Endpoints for getting version information."""
import os
from typing import Union, List, Annotated
from urllib.parse import urljoin

import requests
from fastapi import APIRouter, Query
from ..schemas.classifier import CommentsResponse, Comment, CommentInfo
from ..utils.classifier import classifier

api_router = APIRouter()

session = requests.Session()
feddit_host = os.environ.get("FEDDIT_HOST")


@api_router.get("/comments/",
                response_description="Comments and classification.",
                response_model=CommentsResponse)
async def get_comments(subfeddit_id: int,
                       skip: int = 0,
                       limit: int = 10,
                       start_time: Union[None, int] = None,
                       end_time: Union[None, int] = None,
                       order_by: Annotated[list[str] | None, Query()] = None
                       ) -> CommentsResponse:
    """Get top comments and their sentiment.
    Args:
        subfeddit_id (int): ID of the subfeddit for returning.
        skip (int): Number of subfeddits to skip. Default value is 0.
        limit (int): Max number of subfeddits to return. Default value is 10.
        start_time: Timestamp
        end_time:Timestamp
        order_by: Sort key

    Returns:
        CommentsResponse: A json response containing comments and their classification.
    """
    modified_url = urljoin(feddit_host, f"comments/?subfeddit_id={subfeddit_id}&skip={skip}&limit={limit}")
    response = session.get(modified_url).json()
    comments = [Comment(id=i["id"], username=i["username"], text=i["text"], created_at=i["created_at"]) for i in
                response["comments"]]
    filtered_comments = filter_comments(comments, start_time=start_time, end_time=end_time)
    comments = classifier.classify(filtered_comments)
    comments = order_comments(comments, order_by=order_by)

    return CommentsResponse(subfeddit_id=subfeddit_id, skip=skip, limit=limit, comments=comments)


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
