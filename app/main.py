from fastapi import FastAPI, Response,status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from . import models

from . database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database='fastapi', user='postgres', password='mathew1215', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("DB connection successful")
        break
    except Exception as error:
        print("DB Connection Failed")
        print("Error: ", error)
        time.sleep(2)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    publish: bool = False
    rating: Optional[int] = None
    



@app.get('/') 
async def root():
    return{"message": "Hello from root"}

@app.get("/sqlalchemy") 
def test_posts(db: Session = Depends(get_db)):
    return{"status": "success"}

# Post Endpoint
@app.get("/posts")
def get_posts():
    posts = cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return{"data": posts}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""
    SELECT * 
    FROM posts 
    WHERE id = %s""",(id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def post_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.publish))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""
    DELETE from posts
    WHERE id = %s returning *""", (id,))
    deleted_post = cursor.fetchone()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} not found")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""
    UPDATE posts
    SET title = %s, content = %s, published = %s RETURNING *""", (post.title, post.content, post.publish))
    updated_post = cursor.fetchone()

    if not updated_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    conn.commit()
    print(updated_post)
    return {'data': updated_post}
