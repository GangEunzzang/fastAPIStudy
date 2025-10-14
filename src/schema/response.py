from typing import List

from pydantic import BaseModel, ConfigDict


class ToDoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool

    model_config = ConfigDict(from_attributes=True)


class ToDoListSchema(BaseModel):
    todos: List[ToDoSchema]