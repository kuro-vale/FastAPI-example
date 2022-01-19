# Python
import json
from typing import List
import uuid
# Models
from models.Login import Login
from models.User import User
from models.Tweet import Tweet
# FastAPI
from starlette.responses import RedirectResponse
from fastapi import FastAPI, status, Body, HTTPException

app = FastAPI()


# Path Operations
@app.get("/", tags=["Home"])
def home():
    return RedirectResponse("/tweets", status_code=status.HTTP_307_TEMPORARY_REDIRECT)


# Auth Paths
@app.post("/auth/signup", response_model=User, response_model_exclude={"password"}, status_code=status.HTTP_201_CREATED,
          tags=["Auth"])
def sign_up(user: User = Body(...)):
    user.user_id = uuid.uuid4()
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.load(f)
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        json.dump(results, f)
        return user


@app.post("/auth/login", tags=["Auth"])
def log_in(user: Login = Body(...)):
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.load(f)
        for dictionary in results:
            if user.username == dictionary["username"] and user.password == dictionary["password"]:
                return {user.username: "Login Successfully!"}
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")


# Users Paths
@app.get("/users", response_model=List[User], response_model_exclude={"password"}, tags=["Users"])
def show_all_users():
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.load(f)
        return results


@app.get("/users/{user_id}", response_model=User, response_model_exclude={"password"}, tags=["Users"])
def show_user():
    pass


@app.delete("/users/{user_id}", response_model=User, response_model_exclude={"password"},
            tags=["Users"],)  # status_code=status.HTTP_204_NO_CONTENT)
def delete_user():
    pass


@app.put("/users/{user_id}", response_model=User, response_model_exclude={"password"}, tags=["Users"])
def update_user():
    pass


# Tweets Paths
@app.get("/tweets", response_model=List[Tweet], response_model_exclude={"by"}, tags=["Tweets"])
def show_all_tweets():
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.load(f)
        return results


@app.post("/tweets", response_model=Tweet, tags=["Tweets"], status_code=status.HTTP_201_CREATED)
def post_tweet(tweet: Tweet = Body(...)):
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.load(f)
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_datetime"] = str(tweet_dict["created_datetime"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
        results.append(tweet_dict)
        f.seek(0)
        json.dump(results, f)
        return tweet


@app.get("/tweets/{tweet_id}", response_model=Tweet, tags=["Tweets"])
def show_tweet():
    pass


@app.delete("/tweets/{tweet_id}", response_model=Tweet, tags=["Tweets"],)  # status_code=status.HTTP_204_NO_CONTENT)
def delete_tweet():
    pass
