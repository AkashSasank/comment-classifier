from typing import List

from pydantic import BaseModel, Field


class Comment(BaseModel):
    """Comment object"""
    id: int
    username: str
    text: str
    created_at: int


class CommentInfo(BaseModel):
    """Contain basic fields of a comment, and it's classification."""
    id: int = Field(description="ID of the comment",
                    examples=['1'])
    comment: str = Field(description="Content of the comment.",
                         examples=["I upgraded pydantic from v1 to v2, which "
                                   "brings a lot of problems."])
    score: float = Field(description="The polarity score of comment. Vales in range [0, 1]",
                         examples=[0.99, 0.75])
    classification: str = Field(description="Classification of comment sentiment.",
                                examples=["POSITIVE", "NEGATIVE"])


class CommentsResponse(BaseModel):
    """Comments response schema."""
    subfeddit_id: int = Field(...,
                              description="ID of the subfeddit, to which the"
                                          " comments belong.",
                              examples=[1, 2])
    limit: int = Field(10,
                       description="Max number of returning comments.",
                       examples=[10])
    skip: int = Field(0,
                      description="Number of comments to skip.",
                      examples=[0])
    comments: List[CommentInfo] = Field(...,
                                        description="Comments in this subfeddit.")
