from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List

# Using SQL
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# Using ORM
import models, schemas
from database import engine, get_db
from sqlalchemy.orm import Session

# Using SQL
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi",
#             user="postgres",
#             password="#2Strongpostgres",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("Database connection is successful!")
#         break
#     except Exception as error:
#         print("Database connection failed! Retrying in 5 seconds...")
#         print("Error: ", error)
#         time.sleep(5)

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model = List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):

    # Using SQL
    # cursor.execute("""SELECT * from posts""")
    # posts = cursor.fetchall()
    # return {"data": posts}

    # Using ORM
    posts = db.query(models.Post).all()
    return posts



@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):

    # Using SQL
    # # This approach of string interpolation protects database from SQL injection
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()

    # Using ORM
    # Below line converts post into a dict and unpacks it to fit directly into the model
    # Alternative approach to manually providing key/value pairs
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model = schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):


    # Using SQL
    # cursor.execute("""SELECT * from posts WHERE id= %s """, (str(id),))
    # post = cursor.fetchone()

    # Using ORM
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # Using SQL
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # post = cursor.fetchone()
    # conn.commit()

    # Using ORM
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model = schemas.Post)
def update_posts(post: schemas.PostCreate, id: int, db: Session = Depends(get_db)):

    # Using SQL
    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.published, str(id)),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    # Using ORM
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()