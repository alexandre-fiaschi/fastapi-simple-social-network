from fastapi import FastAPI
from app import models
from .database import engine
from .routers import post, user, auth, vote

# YT https://youtu.be/0sOvCWFmrtA?t=38030   alembic


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
