from pydantic import BaseModel
from datetime import datetime
#Pydantic Post Model
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = False

class PostBase(BaseModel):
    title:str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime 
    class Config:
        from_attributes = True
