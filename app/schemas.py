from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated


# schemas to define structure of the request pydantic to perform validation on the fields and data type: tell exactly what we need for
# response
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

# response model
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True



# request
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]

