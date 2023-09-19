from fastapi import FastAPI, Response,status, HTTPException, Depends
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from . import models, schemas
from . database import engine,get_db

models.Base.metadata.create_all(bind=engine)




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

    



@app.get('/') 
async def root():
    return{"message": "Hello from root"}


# Post Endpoint
@app.get("/posts", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # posts = cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int,db: Session = Depends(get_db)):
    # cursor.execute("""
    # SELECT * 
    # FROM posts 
    # WHERE id = %s""",(id,))
    # post = db.execute(select(models.Post).where(models.Post.id == id))()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    # post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def post_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.publish))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
   # cursor.execute("""
   # DELETE from posts
   # WHERE id = %s returning *""", (id,))
   # deleted_post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} not found")
    #conn.commit()
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""
    # UPDATE posts
    # SET title = %s, content = %s, published = %s RETURNING *""", (post.title, post.content, post.publish))
    # updated_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    # conn.commit()
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    print(updated_post)
    return post_query.first()
