from pydantic import BaseModel, EmailStr
from datetime import datetime


# Schema for Creating Post
# Used to validate data sent from user
class PostBase(BaseModel):
    title: str
    content: str
    # Optional Field with default value
    published: bool = True
    # Optional Field with no default value
    # rating: Optional[int] = None


class PostCreate(PostBase):
    pass


# Schema for Post Response
# Used to validate data from backend before sending data back to user
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
