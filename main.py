from fastapi import FastAPI

from auth.router import router as user_router
from auth.auth import router as auth_router
from posts.router import router as posts_router
from posts.like import router as likes_router
from posts.comment import router as comments_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(posts_router)
app.include_router(likes_router)
app.include_router(comments_router)
