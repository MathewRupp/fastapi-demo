from fastapi import FastAPI, Response,status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

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
    

my_posts = []

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def del_post(id):
    for p in my_posts:
        if p["id"] == id:
            my_posts.remove(p)
            print(f"item with id: {id} was deleted")
            return
    return

def find_post_by_id(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i
    return None

@app.get('/') 
async def root():
    return{"message": "Hello from root"}

# Post Endpoint
@app.get("/posts")
def get_posts():
    posts = cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return{"data": posts}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    
    post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def post_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    del_post(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    post_index = find_post_by_id(id)

    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[post_index] = post_dict 
    print(post)
    return {'data': post_dict}
