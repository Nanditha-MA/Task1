from fastapi import FastAPI
from .database import Base, engine
from .routers import auth, tasks, users

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(users.router)
