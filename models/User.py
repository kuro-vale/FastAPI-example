# Python
import datetime
from datetime import date
from typing import Optional
from uuid import UUID
# Pydantic
from pydantic import Field, EmailStr, validator
# FastAPI
from fastapi import HTTPException, status
# Login model
from models.Login import Login


class User(Login):
    user_id: Optional[UUID] = Field(None)
    birth_date: date = Field(...)
    email: EmailStr = Field(...)

    @validator("birth_date")
    def is_over_eighteen(cls, v):
        today = datetime.datetime.now()
        age = today.year - v.year
        m = today.month - v.month
        if m < 0 or (m == 0 and today.day < v.day):
            age -= 1
        if age >= 18:
            return v
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Age must be over 18")

    class Config:
        schema_extra = {
            "example": {
                "username": "kurovale",
                "birth_date": "2000-8-21",
                "email": "jsalcedo218@gmail.com",
                "password": "kurovale"
            }
        }
