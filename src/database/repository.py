from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.orm import Todo


def get_todos(session: Session) -> List[Todo]:
  return list(session.scalars(select(Todo)))


def get_todo_by_todo_id(  session: Session,todo_id: int) -> Optional[Todo]:  # Python 3.9 이하 호환
  return session.scalar(
      select(Todo).where(Todo.id == todo_id)
  )


def create_todo(session: Session, todo: Todo):
  session.add(instance=todo)
  session.commit()
  session.refresh(instance=todo)
  return todo
