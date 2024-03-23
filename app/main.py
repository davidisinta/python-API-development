from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randint
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    rating: Optional[int] = None


## database connection
DB_NAME = "fastapi_db"
DB_USER = "postgres"
DB_PASSWORD = "hardToguess73"
DB_HOST = "localhost"
DB_PORT = "5432"

while True:
    try:
        conn = psycopg2.connect(host = DB_HOST,
                                port = DB_PORT,
                                database = DB_NAME,
                                user = DB_USER,
                                password = DB_PASSWORD,
                                cursor_factory = RealDictCursor)

        cur = conn.cursor()

        print("----------------------------------------------------------------")
        print("Connected to Database successfully!!")
        print("----------------------------------------------------------------")
        break

    except Exception as e:
        print("----------------------------------------------------------------")
        print("Failed to Connect to Database")
        print(e)
        print("----------------------------------------------------------------")
        time.sleep(10)



my_posts = [{"title":"My first post","content":"", "id":1},
            {"title":"My second post","content":"This is my second post","id":2}]

def find_posts(id):
    for post in my_posts:
        if post["id"] == id:
            return post

def find_post_index(id):
    for count, post in enumerate(my_posts):
        if post["id"] == id:
            return count

def delete_a_post(id):
    for post in my_posts:
        if post["id"] == id:
            my_posts.remove(post)
            return True


    return False




@app.get("/posts")
async def root():
    return {"data": my_posts}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # we want a title, and content, so we define a pydantic class that does that
    post_dict = post.dict()
    post_dict["id"] = randint(1, 100000000)
    my_posts.append(post_dict)
    return {"post": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):

    post = find_posts(id)
    if not post:
        print("no post here")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")

    return {"post": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    deleted = delete_a_post(id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post was not found, therefore not deleted")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id:int, post: Post):
    # find index of post in array
    index = find_post_index(id)
    print(index)

    # if not found error msg
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post does not exit")

    # if found update

    post = post.dict()
    post["id"] = id

    my_posts[index] = post


    print(post)
    return {"message": post}
