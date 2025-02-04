import os
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.const import TodoItemStatusCode

from .models.item_model import ItemModel
from .models.list_model import ListModel

from fastapi import Depends, HTTPException
from .dependencies import get_db
from sqlalchemy.orm import Session


DEBUG = os.environ.get("DEBUG", "") == "true"

app = FastAPI(
    title="Python Backend Stations",
    debug=DEBUG,
)

if DEBUG:
    from debug_toolbar.middleware import DebugToolbarMiddleware

    # panelsに追加で表示するパネルを指定できる
    app.add_middleware(
        DebugToolbarMiddleware,
        panels=["app.database.SQLAlchemyPanel"],
    )


class NewTodoItem(BaseModel):
    """TODO項目新規作成時のスキーマ."""

    title: str = Field(title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    due_at: datetime | None = Field(default=None, title="Todo Item Due")


class UpdateTodoItem(BaseModel):
    """TODO項目更新時のスキーマ."""

    title: str | None = Field(default=None, title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    due_at: datetime | None = Field(default=None, title="Todo Item Due")
    complete: bool | None = Field(default=None, title="Set Todo Item status as completed")


class ResponseTodoItem(BaseModel):
    id: int
    todo_list_id: int
    title: str = Field(title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    status_code: TodoItemStatusCode = Field(title="Todo Status Code")
    due_at: datetime | None = Field(default=None, title="Todo Item Due")
    created_at: datetime = Field(title="datetime that the item was created")
    updated_at: datetime = Field(title="datetime that the item was updated")


class NewTodoList(BaseModel):
    """TODOリスト新規作成時のスキーマ."""

    title: str = Field(title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo List Description", min_length=1, max_length=200)


class UpdateTodoList(BaseModel):
    """TODOリスト更新時のスキーマ."""

    title: str | None = Field(default=None, title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo List Description", min_length=1, max_length=200)


class ResponseTodoList(BaseModel):
    """TODOリストのレスポンススキーマ."""

    id: int
    title: str = Field(title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo List Description", min_length=1, max_length=200)
    created_at: datetime = Field(title="datetime that the item was created")
    updated_at: datetime = Field(title="datetime that the item was updated")


@app.get("/echo")
def get_echo(message: str, name: str):
    return {"Message": f"{message} {name}!"}

@app.get("/health")
def get_health():
    return {"status": "ok"}

@app.get("/lists/{todo_list_id}", tags=["Todoリスト"])
def get_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
    db_item= db.query(ListModel).filter(ListModel.id == todo_list_id).first()
    return db_item

@app.post("/lists", tags=["Todoリスト"])
def post_todo_list(todo_list: NewTodoList, db: Session=Depends(get_db)):
    db_todo_list = ListModel(
        title=todo_list.title,
        description=todo_list.description
    )
    db.add(db_todo_list)
    db.commit()
    db.refresh(db_todo_list)
    return db_todo_list

    
@app.put("/lists/{todo_list_id}", tags=["Todoリスト"])
def put_todo_list(todo_list_id: int, todo_list: UpdateTodoList, db: Session=Depends(get_db)):
    db_todo_list = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
    if db_todo_list is None:
        raise HTTPException(status_code=404, detail="Todo List not found")
    db_todo_list.title = todo_list.title
    db_todo_list.description = todo_list.description
    db.commit()
    db.refresh(db_todo_list)
    return db_todo_list

@app.delete("/lists/{todo_list_id}", tags=["Todoリスト"])
def delete_todo_list(todo_list_id:int,db:Session=Depends(get_db)):
    db_todo_list = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
    if db_todo_list is None:
        raise HTTPException(status_code=404, detail="Todo List not found")
    db.delete(db_todo_list)
    db.commit()
    return {}

# TODOリストに対してTODO項目取得するAPI
@app.get("/lists/{todo_list_id}/items/{todo_item_id}",tags=["Todo項目"])
def get_todo_item(todo_list_id:int,todo_item_id:int,db:Session=Depends(get_db)):
    db_item = db.query(ItemModel).filter(ItemModel.id == todo_item_id, ItemModel.todo_list_id == todo_list_id).first()
    return {
        "id": db_item.id,
        "todo_list_id": db_item.todo_list_id,
        "title": db_item.title,
        "description": db_item.description,
        "status_code": db_item.status_code,
        "due_at": db_item.due_at,
        "created_at": db_item.created_at,
        "updated_at": db_item.updated_at
    }
    
@app.post("/lists/{todo_list_id}/items",tags=["Todo項目"])
def post_todo_item(todo_list_id:int,todo_item:NewTodoItem,db:Session=Depends(get_db)):
    db_todo_item = ItemModel(
        todo_list_id=todo_list_id,
        title=todo_item.title,
        description=todo_item.description,
        status_code=TodoItemStatusCode.NOT_COMPLETED.value,
        due_at=todo_item.due_at
    )
    db.add(db_todo_item)
    db.commit()
    return {
        "id": db_todo_item.id,
        "todo_list_id": db_todo_item.todo_list_id,
        "title": db_todo_item.title,
        "description": db_todo_item.description,
        "status_code": db_todo_item.status_code,
        "due_at": db_todo_item.due_at,
        "created_at": db_todo_item.created_at,
        "updated_at": db_todo_item.updated_at
    }


@app.put("/lists/{todo_list_id}/items/{todo_item_id}",tags=["Todo項目"])
def put_todo_item(todo_list_id:int,todo_item_id:int,todo_item:UpdateTodoItem,db:Session=Depends(get_db)):
    db_todo_item = db.query(ItemModel).filter(ItemModel.id == todo_item_id, ItemModel.todo_list_id == todo_list_id).first()
    if db_todo_item is None:
        raise HTTPException(status_code=404, detail="Todo Item not found")
    db_todo_item.title = todo_item.title
    db_todo_item.description = todo_item.description
    db_todo_item.due_at = todo_item.due_at
    db.commit()
    return {
        "id": db_todo_item.id,
        "todo_list_id": db_todo_item.todo_list_id,
        "title": db_todo_item.title,
        "description": db_todo_item.description,
        "status_code": TodoItemStatusCode.COMPLETED.value if todo_item.complete else TodoItemStatusCode.NOT_COMPLETED.value,
        "due_at": db_todo_item.due_at,
        "created_at": db_todo_item.created_at,
        "updated_at": db_todo_item.updated_at
    }

