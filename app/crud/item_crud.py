from sqlalchemy.orm import Session

from app.const import TodoItemStatusCode
from app.models.item_model import ItemModel
from app.schemas.item_schema import NewTodoItem,UpdateTodoItem
from fastapi import HTTPException
from app.models.list_model import ListModel

def get_todo_item(db:Session,todo_list_id:int,todo_item_id:int):
    return db.query(ItemModel).filter(ItemModel.id == todo_item_id, ItemModel.todo_list_id == todo_list_id).first()


def create_todo_item(db:Session,todo_list_id:int,new_todo_item:NewTodoItem):
    # TODOリストの存在チェック
    db_todo_list = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
    if db_todo_list is None:
        raise HTTPException(status_code=404,detail="Todo List not found")
        
    db_todo_item = ItemModel(
        todo_list_id=todo_list_id,
        title=new_todo_item.title,
        description=new_todo_item.description,
        status_code=TodoItemStatusCode.NOT_COMPLETED.value,
        due_at=new_todo_item.due_at
    )
    db.add(db_todo_item)
    db.commit()
    db.refresh(db_todo_item)
    return db_todo_item

def update_todo_item(db:Session,todo_list_id:int,todo_item_id:int,update_todo_item:UpdateTodoItem):
    # 対象のTODO項目を取得（todo_list_id でリストのチェックも行う）

    item = db.query(ItemModel).filter(
        ItemModel.id == todo_item_id,
        ItemModel.todo_list_id == todo_list_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Todo Item not found")
    
    # 更新処理例
    item.title = update_todo_item.title
    item.description = update_todo_item.description
    item.due_at = update_todo_item.due_at
    if hasattr(update_todo_item, 'complete'):
        item.status_code = TodoItemStatusCode.COMPLETED if update_todo_item.complete else TodoItemStatusCode.NOT_COMPLETED
    
    db.commit()
    db.refresh(item)
    return item

def delete_todo_item(db:Session,todo_list_id:int,todo_item_id:int):
    db_todo_item = get_todo_item(db,todo_list_id=todo_list_id,todo_item_id=todo_item_id)
    if db_todo_item is None:
        raise HTTPException(status_code=404,detail="Todo Item not found")


    db.delete(db_todo_item)
    db.commit()
    return True

def get_todo_items(db:Session,todo_list_id:int):
    return db.query(ItemModel).filter(ItemModel.todo_list_id == todo_list_id).all()


