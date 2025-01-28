from pydantic import BaseModel, Field
from typing import List

class User(BaseModel):
    id: int
    name: str
    username: str
    email: str
    
class Post(BaseModel):
    id: int
    userId: int
    title: str
    body: str
