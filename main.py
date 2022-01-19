# Python
import json
import os
import time
from datetime import datetime
from typing import List
import uuid
# Models
from models.Login import Login
from models.User import User
from models.Tweet import Tweet
# FastAPI
from starlette.responses import RedirectResponse
from fastapi import FastAPI, status, Body, HTTPException, Path

app = FastAPI()


# Path Operations
@app.get("/", tags=["Home"])
def home():
    # Redirection to all tweets
    return RedirectResponse("/tweets", status_code=status.HTTP_307_TEMPORARY_REDIRECT)


# Auth Paths
@app.post("/auth/signup", status_code=status.HTTP_201_CREATED, tags=["Auth"])
def sign_up(user: User = Body(...)):
    # Add a User to users.json
    user.user_id = uuid.uuid4()
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.load(f)
        for dictionary in results:
            if user.username == dictionary["username"]:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exist")
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        json.dump(results, f)
        return {user.username: "Created Successfully!"}


@app.post("/auth/login", tags=["Auth"])
def log_in(user: Login = Body(...)):
    # If username and password match which one in users.json, then return a Login Successfully
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.load(f)
        for dictionary in results:
            if user.username == dictionary["username"] and user.password == dictionary["password"]:
                return {user.username: "Login Successfully!"}

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")


# Users Paths
@app.get("/users", response_model=List[Login], response_model_exclude={"password"}, tags=["Users"])
def show_all_users():
    # Show all usernames in users.json
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.load(f)
        return results


@app.get("/users/{username}", response_model=User, response_model_exclude={"password", "user_id"}, tags=["Users"])
def show_user(username: str = Path(..., max_length=20)):
    # Show the info of a user in users.json
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.load(f)
        for dictionary in results:
            if username == dictionary["username"]:
                return dictionary

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user doesn't exist")


@app.delete("/users/{username}", tags=["Users"])
def delete_user(username: str = Path(..., max_length=20), user: Login = Body(...)):
    # Delete a user in users.json
    log_in(user)
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.load(f)
        for dictionary in results:
            if username == dictionary["username"]:
                if user.username != dictionary["username"]:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This user is not yours")
                results.remove(dictionary)
                f.close()
                with open("users.tmp", "w", encoding="utf-8") as t:
                    json.dump(results, t)
                    t.close()
                    os.remove("users.json")
                    os.rename("users.tmp", "users.json")
                    return {username: "Deleted Successfully"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user doesn't exist")


@app.put("/users/{username}", tags=["Users"])
def update_user(username: str = Path(..., max_length=20), new_user: User = Body(...), user: Login = Body(...)):
    # Update user in users.json
    log_in(user)
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.load(f)
        repeated_username = 0
        user_dict = new_user.dict()
        for dictionary in results:  # Find username to be updated
            if username == dictionary["username"]:
                if user.username != dictionary["username"]:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This user is not yours")
                user_dict["user_id"] = str(dictionary["user_id"])  # Keep the same ID
                user_dict["birth_date"] = str(user_dict["birth_date"])
                dictionary.update(user_dict)
        for dictionary in results:   # Prevent duplicates usernames
            if user_dict["username"] == dictionary["username"]:
                repeated_username += 1
        if repeated_username == 1:  # If not duplicates, update the username in users.json
            f.close()
            with open("users.tmp", "w", encoding="utf-8") as t:
                json.dump(results, t)
                t.close()
                os.remove("users.json")
                os.rename("users.tmp", "users.json")
                return {user_dict["username"]: "Updated Successfully"}
        elif repeated_username > 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exist")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user doesn't exist")


# Tweets Paths
@app.get("/tweets", response_model=List[Tweet], response_model_exclude={"tweet_id"}, tags=["Tweets"])
def show_all_tweets():
    # Show all tweets in tweets.json
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.load(f)
        return results


@app.post("/tweets", tags=["Tweets"], status_code=status.HTTP_201_CREATED)
def post_tweet(tweet: Tweet = Body(...), user: Login = Body(...)):
    # Add a tweet in tweets.json
    log_in(user)
    tweet.tweet_id = uuid.uuid4()
    tweet.by = user.username
    tweet.created_datetime = datetime.now()
    tweet.created_timezone = time.tzname[0]
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.load(f)
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_datetime"] = str(tweet_dict["created_datetime"])
        results.append(tweet_dict)
        f.seek(0)
        json.dump(results, f)
        return {"Tweet posted successfully!"}


@app.get("/tweets/{tweet_id}", response_model=Tweet, response_model_exclude={"tweet_id"}, tags=["Tweets"])
def show_tweet(tweet_id: str = Path(...)):
    # Show a specific tweet in tweets.json
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.load(f)
        for dictionary in results:
            if tweet_id == dictionary["tweet_id"]:
                return dictionary

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This tweet doesn't exist")


@app.delete("/tweets/{tweet_id}", tags=["Tweets"],)
def delete_tweet(tweet_id: str = Path(...), user: Login = Body(...)):
    # Delete a tweet in tweets.json
    log_in(user)
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.load(f)
        for dictionary in results:
            if tweet_id == dictionary["tweet_id"]:
                if user.username != dictionary["by"]:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This tweet is not yours")
                results.remove(dictionary)
                f.close()
                with open("tweets.tmp", "w", encoding="utf-8") as t:
                    json.dump(results, t)
                    t.close()
                    os.remove("tweets.json")
                    os.rename("tweets.tmp", "tweets.json")
                    return {"Tweet deleted successfully!"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This tweet doesn't exist")