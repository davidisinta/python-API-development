from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hey thereeee, fullstack mern"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/createposts")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"message": "gooda gooda"}
