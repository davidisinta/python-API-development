from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Hey thereeee, fullstack mern"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/posts")
def create_post(post: Post):
    # we want a title, and content, so we define a pydantic class that does that
    print(post.rating)
    print(post.dict())
    return {"message": "gooda gooda"}
