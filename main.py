from fastapi import FastAPI, HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# Schema Validation with Pydantic
class Post(BaseModel):
    title : str
    content : str
    published : bool = True  
    
@app.get("/")
def read_root():
    return {"Message": "Welcome to FastAPI"}

# @app.get("/posts")
# def get_posts():
#     return {"data": "All posts"}

# @app.get("/posts/latest")
# def get_latest_post():
#     return {"Message":"Latest Post"}

# @app.get("/posts/{id}")
# def get_post(id: int):
#     return {"post_id": id}

# @app.post("/posts")
# def create_post(post : Post):
#     return {
#         "Data": post
#     }

my_posts = [
    {"title": "Post 1", "content": "Content 1", "id": 1},
    {"title": "Food", "content": "Biryani", "id": 2},
    {"title": "Python", "content": "FastAPI", "published": True, "id": 45678},
]  
def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

# CRUD Operations
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)

    return {"data": post_dict}

@app.get("/posts")
def get_post():
    return {
        "data" : my_posts
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
