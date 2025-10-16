from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.orm import Todo


def get_todos(session: Session) -> list[Todo]:
  return list(session.scalars(select(Todo)))


def get_todo_by_todo_id(  session: Session,todo_id: int) ->Todo | None:  # Python 3.9 이하 호환
  return session.scalar(
      select(Todo).where(Todo.id == todo_id)
  )


def create_todo(session: Session, todo: Todo) -> Todo:
  session.add(instance=todo)
  session.commit()
  session.refresh(instance=todo)
  return todo

def update_todo(session: Session, todo: Todo):
  session.add(instance=todo)
  session.commit()
  session.refresh(instance=todo)
  return todo

def delete_todo(session: Session, todo_id: int) -> bool:
  todo = get_todo_by_todo_id(session, todo_id)
  if todo:
    session.delete(todo)
    session.commit()
    return True
  return False