from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.item_schema import NewTodoItem, ResponseTodoItem, UpdateTodoItem
from app.crud import item_crud

router = APIRouter(
    prefix="/lists/{todo_list_id}/items",
    tags=["Todo項目"],
)


@router.post("/", response_model=ResponseTodoItem, status_code=status.HTTP_201_CREATED)
def post_todo_item(todo_list_id: int, todo_item: NewTodoItem, db: Session = Depends(get_db)):
    """TODO項目を作成する."""
    return item_crud.create_todo_item(db, todo_list_id=todo_list_id, new_todo_item=todo_item)


@router.get("/{todo_item_id}", response_model=ResponseTodoItem)
def get_todo_item(todo_list_id: int, todo_item_id: int, db: Session = Depends(get_db)):
    """TODO項目をIDで取得する."""
    db_todo_item = item_crud.get_todo_item(db, todo_list_id=todo_list_id, todo_item_id=todo_item_id)
    if db_todo_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo Item not found")
    return db_todo_item


@router.put("/{todo_item_id}", response_model=ResponseTodoItem)
def put_todo_item(todo_list_id: int, todo_item_id: int, todo_item: UpdateTodoItem, db: Session = Depends(get_db)):
    """TODO項目を更新する."""
    db_todo_item = item_crud.update_todo_item(
        db, todo_list_id=todo_list_id, todo_item_id=todo_item_id, update_todo_item=todo_item
    )
    if db_todo_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo Item not found")
    return db_todo_item


@router.delete("/{todo_item_id}")
def delete_todo_item(todo_list_id: int, todo_item_id: int, db: Session = Depends(get_db)):
    """TODO項目を削除する."""
    if not item_crud.delete_todo_item(db, todo_list_id=todo_list_id, todo_item_id=todo_item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo Item not found")
    return {"message": "Todo Item deleted successfully"}
