from fastapi import FastAPI

from app.routers import posts, users

app = FastAPI()

app.include_router(users.router, tags=["Users"], prefix="/api")
app.include_router(posts.router, tags=["Posts"], prefix="/api")
