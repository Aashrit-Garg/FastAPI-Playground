from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": "These are your posts"}

@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"data": "Successfully created posts"}