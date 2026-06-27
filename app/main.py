from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# Schema Validation with Pydantic
class Post(BaseModel):
    title : str
    content : str
    published : bool = True 

while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='NewPassword123',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful!")
        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)


@app.get("/")
def read_root():
    return {"Message": "Welcome to FastAPI"}

my_posts = [
    {"title": "Post 1", "content": "Content 1", "id": 1},
    {"title": "Food", "content": "Biryani", "id": 2},
    {"title": "Python", "content": "FastAPI", "published": True, "id": 45678},
]  

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
        
def find_index_post(id):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i             

# CRUD Operations
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)

    return {"data": post_dict}

@app.get("/posts")
def get_posts():
    cursor.execute('SELECT * FROM "Posts"')
    posts = cursor.fetchall()
    return {
        "data" : posts
    }

@app.get("/posts/latest")
def get_latest_post():
    return {"data": my_posts[-1]}

# Retrieve one post
@app.get("/posts/{id}")
def get_post(id : int):
    post = find_post(id)

    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id {id} not found"
        )
    
    return {
        "data" : post
    }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            my_posts.pop(index)
            return
        
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = f"Post with id {id} not found"
    )    

@app.put("/posts/{id}")
def update_post(id: int, post : Post):
    index = find_index_post(id)

    if index is None:
        raise HTTPException (
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id {id} not found"
        )
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict

    return {
        "data":post_dict
    }

