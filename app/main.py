from fastapi import FastAPI
from routers import post, user


import models, schemas, utils
from database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"data": "Hello World"}

# Include Post Routes
app.include_router(post.router)

# Include User Routes
app.include_router(user.router)