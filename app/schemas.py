from pydantic import BaseModel

#Pydantic Post Model
class Post(BaseModel):
    title: str
    content: str
    published: bool = False

class PostBase(BaseModel):
    title:str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


