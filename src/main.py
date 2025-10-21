from typing import List

from fastapi import FastAPI, Body, Depends, HTTPException  # ✅ 수정
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import Todo
from database.repository import get_todos, create_todo, get_todo_by_todo_id, \
    update_todo, delete_todo
from schema.request import CreateTodoRequest
from schema.response import ToDoSchema

app = FastAPI()


@app.get("/")
def health_check_handler():
    return {"ping": "pong"}


@app.get("/todos", response_model=List[ToDoSchema])  # ✅ 수정
def get_todos_handler(session: Session = Depends(get_db)):
    todos: List[Todo] = get_todos(session=session)
    return [ToDoSchema.model_validate(todo) for todo in todos]  # ✅ 수정


@app.get("/todos/{todo_id}", response_model=ToDoSchema, status_code=200)
def get_todo(
        todo_id: int,
        session: Session = Depends(get_db)
):
    todo: Todo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.post("/todos", response_model=ToDoSchema)
def create_todo_handler(
        request: CreateTodoRequest,
        session: Session = Depends(get_db)
):
    todo: Todo = Todo.create(request=request)
    todo: Todo = create_todo(session=session, todo=todo)
    return ToDoSchema.model_validate(todo)


@app.patch("/todos/{todo_id}", response_model=ToDoSchema)
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(..., embed=True),
        session: Session = Depends(get_db)
):
    todo: Todo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.done() if is_done else todo.undone()
    todo: Todo = update_todo(session=session, todo=todo)
    return ToDoSchema.model_validate(todo)


@app.delete("/todos/{todo_id}", status_code=204)  # ✅ 수정
def delete_todo_handler(
        todo_id: int,
        session: Session = Depends(get_db)
):
    todo = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    delete_todo(todo_id=todo_id, session=session)
    return None
