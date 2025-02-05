from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import list_crud
from app.dependencies import get_db
from app.schemas.list_schema import NewTodoList,UpdateTodoList,ResponseTodoList


router = APIRouter(
    prefix="/lists",
    tags=["Todoリスト"]
)


@router.post("/",response_model=ResponseTodoList)
def post_todo_list(todo_list:NewTodoList,db:Session=Depends(get_db)):
    return list_crud.create_todo_list(db,todo_list)


@router.get("/{todo_list_id}",response_model=ResponseTodoList)
def get_todo_list(todo_list_id:int,db:Session=Depends(get_db)):
    db_todo_list = list_crud.get_todo_list(db,todo_list_id=todo_list_id)
    if db_todo_list is None:
        raise HTTPException(status_code=404,detail="Todo List not found")
    return db_todo_list


@router.put("/{todo_list_id}",response_model=ResponseTodoList)
def put_todo_list(todo_list_id:int,todo_list:UpdateTodoList,db:Session=Depends(get_db)):
    return list_crud.update_todo_list(db,todo_list_id=todo_list_id,todo_list=todo_list)


@router.delete("/{todo_list_id}")
def delete_todo_list(todo_list_id:int,db:Session=Depends(get_db)):
    if not list_crud.delete_todo_list(db,todo_list_id=todo_list_id):
        raise HTTPException(status_code=404,detail="Todo List not found")
    return True








