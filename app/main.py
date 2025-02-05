import os
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.routers import item_router, list_router

from fastapi import Depends, HTTPException
from .dependencies import get_db
from sqlalchemy.orm import Session


DEBUG = os.environ.get("DEBUG", "") == "true"

app = FastAPI(
    title="Python Backend Stations",
    debug=DEBUG,
)

app.include_router(list_router.router)
app.include_router(item_router.router)

if DEBUG:
    from debug_toolbar.middleware import DebugToolbarMiddleware


    # panelsに追加で表示するパネルを指定できる
    app.add_middleware(
        DebugToolbarMiddleware,
        panels=["app.database.SQLAlchemyPanel"],
    )



@app.get("/echo")
def get_echo(message: str, name: str):
    return {"Message": f"{message} {name}!"}

@app.get("/health")
def get_health():
    return {"status": "ok"}
