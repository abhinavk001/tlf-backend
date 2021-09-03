"""
Entrypoint
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.sql.functions import user
from database.database import set_up_database
from database import models
from routers import auth, activity, user


app = FastAPI()

origins = [
    "https://tlf-aswin.netlify.app/",
    "tlf-aswin.netlify.app",
    "https://tlf-aswin.netlify.app"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

models.Base.metadata.create_all(set_up_database())


app.include_router(auth.router)
app.include_router(activity.router)
app.include_router(user.router)
