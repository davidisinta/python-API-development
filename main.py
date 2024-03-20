from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from random import randint

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    rating: Optional[int] = None

my_posts = [{"title":"My first post","content":"", "id":1},
            {"title":"My second post","content":"This is my second post","id":2}, {""}]

def find_posts(id):
    for post in my_posts:
        if post["id"] == id:
            return post

@app.get("/posts")
async def root():
    return {"data": my_posts}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/posts")
def create_post(post: Post):
    # we want a title, and content, so we define a pydantic class that does that
    post_dict = post.dict()
    post_dict["id"] = randint(1, 100000000)
    my_posts.append(post_dict)
    return {"post": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):
    return {"post": find_posts(id)}
