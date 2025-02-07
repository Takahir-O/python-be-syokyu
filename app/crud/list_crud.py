from sqlalchemy.orm import Session
from app.models.list_model import ListModel
from app.schemas.list_schema import NewTodoList,UpdateTodoList
from fastapi import HTTPException

def get_todo_list(db:Session,todo_list_id:int):
    return db.query(ListModel).filter(ListModel.id == todo_list_id).first()


def create_todo_list(db:Session,todo_list:NewTodoList):
    db_todo_list = ListModel(
        title=todo_list.title,
        description=todo_list.description
    )
    db.add(db_todo_list)
    db.commit()
    db.refresh(db_todo_list)
    return db_todo_list


def update_todo_list(db:Session,todo_list_id:int,todo_list:UpdateTodoList):
    db_todo_list = get_todo_list(db,todo_list_id=todo_list_id)
    if db_todo_list is None:
        raise HTTPException(status_code=404,detail="Todo List not found")
    db_todo_list.title = todo_list.title
    db_todo_list.description = todo_list.description
    db.commit()
    db.refresh(db_todo_list)
    return db_todo_list


def delete_todo_list(db:Session,todo_list_id:int):
    db_todo_list = get_todo_list(db,todo_list_id=todo_list_id)
    if db_todo_list is None:
        raise HTTPException(status_code=404,detail="Todo List not found")
    db.delete(db_todo_list)
    db.commit()
    return True

# 配列の中に各 TODOリストの Json オブジェクトがセットされる。
def get_todo_lists(db:Session):
    return db.query(ListModel).all()


