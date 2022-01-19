from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import Field, EmailStr

from models.Login import Login


class User(Login):
    user_id: Optional[UUID] = Field(None)
    birth_date: Optional[date] = Field(None)
    email: EmailStr = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "kurovale",
                "birth_date": "2000-8-21",
                "email": "jsalcedo218@gmail.com",
                "password": "kurovale"
            }
        }