import pytest
from unittest.mock import Mock
from ..src.schemas.classifier import Comment, CommentInfo


@pytest.fixture
def feddit_comments_json():
    return {
        "subfeddit_id": 1,
        "limit": 10,
        "skip": 0,
        "comments": [
            {
                "id": 1,
                "username": "user_0",
                "text": "It looks great!",
                "created_at": 1711190769
            },
            {
                "id": 2,
                "username": "user_1",
                "text": "Love it.",
                "created_at": 1711187169
            },
            {
                "id": 3,
                "username": "user_2",
                "text": "Awesome.",
                "created_at": 1711183569
            },
            {
                "id": 4,
                "username": "user_3",
                "text": "Well done!",
                "created_at": 1711179969
            },
            {
                "id": 5,
                "username": "user_4",
                "text": "Looks decent.",
                "created_at": 1711176369
            },
            {
                "id": 6,
                "username": "user_5",
                "text": "What you did was right.",
                "created_at": 1711172769
            },
            {
                "id": 7,
                "username": "user_6",
                "text": "Thumbs up.",
                "created_at": 1711169169
            },
            {
                "id": 8,
                "username": "user_7",
                "text": "Like it a lot!",
                "created_at": 1711165569
            },
            {
                "id": 9,
                "username": "user_8",
                "text": "Good work.",
                "created_at": 1711161969
            },
            {
                "id": 10,
                "username": "user_9",
                "text": "Luckily you did it.",
                "created_at": 1711158369
            }
        ]
    }


@pytest.fixture
def feddit_comments_classification_json():
    return {
        "subfeddit_id": 1,
        "limit": 10,
        "skip": 0,
        "comments": [
            {
                "id": 1,
                "comment": "It looks great!",
                "score": 0.9999,
                "classification": "POSITIVE"
            },
            {
                "id": 2,
                "comment": "Love it.",
                "score": 0.9999,
                "classification": "POSITIVE"
            },
            {
                "id": 3,
                "comment": "Awesome.",
                "score": 0.9999,
                "classification": "POSITIVE"
            },
            {
                "id": 4,
                "comment": "Well done!",
                "score": 0.9998,
                "classification": "POSITIVE"
            },
            {
                "id": 5,
                "comment": "Looks decent.",
                "score": 0.9998,
                "classification": "POSITIVE"
            },
            {
                "id": 6,
                "comment": "What you did was right.",
                "score": 0.9998,
                "classification": "POSITIVE"
            },
            {
                "id": 7,
                "comment": "Thumbs up.",
                "score": 0.9997,
                "classification": "POSITIVE"
            },
            {
                "id": 8,
                "comment": "Like it a lot!",
                "score": 0.9998,
                "classification": "POSITIVE"
            },
            {
                "id": 9,
                "comment": "Good work.",
                "score": 0.9998,
                "classification": "POSITIVE"
            },
            {
                "id": 10,
                "comment": "Luckily you did it.",
                "score": 0.9991,
                "classification": "POSITIVE"
            }
        ]
    }


@pytest.fixture
def feddit_comments_objects(feddit_comments_json):
    comments = [Comment(id=i["id"], username=i["username"], text=i["text"], created_at=i["created_at"]) for i in
                feddit_comments_json["comments"]]
    return comments


@pytest.fixture
def feddit_comments_classification_objects(feddit_comments_classification_json):
    comments = [CommentInfo(id=i["id"], score="{:.4f}".format(i["score"]), comment=i["comment"],
                            classification=i["classification"]) for i in
                feddit_comments_classification_json["comments"]]
    return comments


@pytest.fixture
def mock_feddit_get(feddit_comments_json):
    mock = Mock()
    mock.return_value.status_code = 200
    mock.return_value.json.return_value = feddit_comments_json
    return mock
