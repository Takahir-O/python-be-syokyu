from sqlalchemy.orm import Session

from app.const import TodoItemStatusCode
from app.models.item_model import ItemModel
from app.schemas.item_schema import NewTodoItem,UpdateTodoItem
from fastapi import HTTPException

def get_todo_item(db:Session,todo_list_id:int,todo_item_id:int):
    return db.query(ItemModel).filter(ItemModel.id == todo_item_id, ItemModel.todo_list_id == todo_list_id).first()


def create_todo_item(db:Session,todo_item:NewTodoItem):
    db_todo_item = ItemModel(
        title=todo_item.title,
        description=todo_item.description,
        status_code=TodoItemStatusCode.NOT_COMPLETED.value,
        due_at=todo_item.due_at
    )
    db.add(db_todo_item)
    db.commit()
    db.refresh(db_todo_item)
    return db_todo_item

def update_todo_item(db:Session,todo_item_id:int,update_todo_item:UpdateTodoItem):
    db_todo_item = get_todo_item(db,todo_item_id=todo_item_id)
    if db_todo_item is None:
        raise HTTPException(status_code=404,detail="Todo Item not found")
    db_todo_item.title = update_todo_item.title
    db_todo_item.description = update_todo_item.description
    db_todo_item.due_at = update_todo_item.due_at
    db.commit()
    db.refresh(db_todo_item)
    return db_todo_item

def delete_todo_item(db:Session,todo_item_id:int):
    db_todo_item = get_todo_item(db,todo_item_id=todo_item_id)
    if db_todo_item is None:
        raise HTTPException(status_code=404,detail="Todo Item not found")
    db.delete(db_todo_item)
    db.commit()
    return True


