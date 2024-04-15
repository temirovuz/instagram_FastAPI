from fastapi import FastAPI

from auth.router import router as user_router
from auth.auth import router as auth_router
from posts.router import router as posts_router

app = FastAPI()

app.include_router(user_router, prefix="/user")
app.include_router(auth_router, prefix="/auth")
app.include_router(posts_router, prefix='/post')
