import time
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(..., max_length=280)
    created_datetime: datetime = Field(default=datetime.now())
    created_timezone: str = Field(default=time.tzname[0])
    by: str = Field(..., max_length=20)