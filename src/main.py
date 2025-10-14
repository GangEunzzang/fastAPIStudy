from http.client import HTTPException
from typing import List

from fastapi import FastAPI, Body, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import Todo
from database.repository import get_todos
from schema.request import CreateTodoRequest
from schema.response import ToDoSchema

app = FastAPI()


@app.get("/")
def health_check_handler():
  return {"ping": "pong"}


todo_date = {
  1: {
    "id": 1,
    "contents": "실전! fastAPI 수강 1",
    "is_done": True
  },
  2: {
    "id": 2,
    "contents": "실전! fastAPI 수강 2",
    "is_done": False
  },
  3: {
    "id": 3,
    "contents": "실전! fastAPI 수강 3",
    "is_done": False
  }
}

@app.get("/todos")
def get_todos1(session: Session = Depends(get_db)):
  todos: List[Todo] = get_todos(session=session)

  ToDoSchema.from_orm(todo)

  return todos

@app.get("/todos2")
def get_todos2():
  sorted1 = sorted(todo_date.values(), key=lambda x: x['id'], reverse=True)
  return sorted1

@app.get("/todos/{todo_id}", status_code=200)
def get_todo(todo_id: int):
    todo = todo_date.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.post("/todos")
def create_todo(request: CreateTodoRequest):
  todo: Todo = Todo.create(request=request)



  todo_date[request.id] = request.model_dump()
  return todo_date[request.id]

@app.patch("/todos/{todo_id}")
def update_todo(
    todo_id: int,
    is_done: bool = Body(..., embed=True),
):
  todo = todo_date.get(todo_id)
  if todo:
    todo["is_done"] = is_done
    return todo
  return {}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
  todo_date.pop(todo_id, None)
  return todo_date

