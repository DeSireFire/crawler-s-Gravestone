#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/5/17
# CreatTIME : 11:34
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
import copy
import json
import time
import random
import uvicorn
import logging
import requests
from redis import Redis
from pprint import pprint
from typing import Optional
from pydantic import BaseModel
from urllib.parse import parse_qs
from pydantic.main import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

fake_users_db = {
    "johndoe": {
        "username": "admin",
        "hashed_password": "123qwe",
        "disabled": False,
    },
    "alice": {
        "username": "test",
        "hashed_password": "test",
        "disabled": True,
    },
}

def fake_hash_password(password: str):
    return "fakehashed" + password

def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    return User(
        username=token + "fakedecoded", password="fakepassword"
    )

async def get_user(username: str):
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)

async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not fake_hash_password(password) == user.hashed_password:
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user



if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 6701
    uvicorn.run(app, host=HOST, port=PORT)
