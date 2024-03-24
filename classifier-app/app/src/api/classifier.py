import os
import requests
from typing import Union, Annotated
from urllib.parse import urljoin
from fastapi import APIRouter, Query
from ..schemas.classifier import CommentsResponse, Comment
from ..utils.classifier import classifier
from .utils import filter_comments, order_comments

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
