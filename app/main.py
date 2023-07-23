from fastapi import FastAPI
from app.routers import users
from app.routers import posts


app = FastAPI()

app.include_router(users.router, tags=["Users"], prefix="/api")
app.include_router(posts.router, tags=["Posts"], prefix="/api")
