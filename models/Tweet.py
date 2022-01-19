# Python
from datetime import datetime
from typing import Optional
from uuid import UUID
# Pydantic
from pydantic import BaseModel, Field


class Tweet(BaseModel):
    tweet_id: Optional[UUID] = Field(None)
    content: str = Field(..., max_length=280)
    created_datetime: datetime = Field(None)
    created_timezone: str = Field(None)
    by: str = Field(None)

    class Config:
        schema_extra = {
            "example": {
                "content": "Lorem Ipsum"
            }
        }