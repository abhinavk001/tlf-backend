"""
Entrypoint
"""
from fastapi import FastAPI
from database.database import set_up_database
from database import models
from routers import auth


app = FastAPI()


models.Base.metadata.create_all(set_up_database())


@app.get("/")
def hello():
    """
    Home page
    """
    return {"message": "Hello World"}


app.include_router(auth.router)
