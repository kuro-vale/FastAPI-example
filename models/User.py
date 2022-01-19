import json
from datetime import date
from os import path
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from pydantic import Field, EmailStr, validator

from models.Login import Login


class User(Login):
    user_id: Optional[UUID] = Field(None)
    birth_date: Optional[date] = Field(None)
    email: EmailStr = Field(...)

    @validator("username")
    def not_exist(cls, v):
        with open(path.dirname(__file__) + "/../users.json", "r", encoding="utf-8") as f:
            results = json.load(f)
            found = False
            for dictionary in results:
                if v == dictionary["username"]:
                    found = True
            if found:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Username already exists, please try another one")
            else:
                return v

    class Config:
        schema_extra = {
            "example": {
                "username": "kurovale",
                "birth_date": "2000-8-21",
                "email": "jsalcedo218@gmail.com",
                "password": "kurovale"
            }
        }