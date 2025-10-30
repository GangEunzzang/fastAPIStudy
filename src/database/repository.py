from sqlalchemy import select
from sqlalchemy.orm import Session

from database.orm import Todo


def find_all(session: Session) -> list[Todo]:
  return list(session.scalars(select(Todo)))


def find_by_id(session: Session, todo_id: int) -> Todo | None:  # Python 3.9 이하 호환
  return session.scalar(
      select(Todo).where(Todo.id == todo_id)
  )


def save(session: Session, todo: Todo) -> Todo:
  session.add(instance=todo)
  session.commit()
  session.refresh(instance=todo)
  return todo

def update(session: Session, todo: Todo):
  session.add(instance=todo)
  session.commit()
  session.refresh(instance=todo)
  return todo

def delete(session: Session, todo_id: int) -> bool:
  todo = find_by_id(session, todo_id)
  if todo:
    session.delete(todo)
    session.commit()
    return True
  return False