from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.orm import Todo

def get_todos(session: Session) -> List[Todo]:
  return list(session.scalars(select(Todo)))

def create_todo(session: Session, todo: Todo) :
  session.add(instance=todo)
  session.commit()
  session.refresh(instance=todo)
  return todo