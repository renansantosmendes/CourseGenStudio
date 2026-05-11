from typing import Annotated
from operator import add
from pydantic import BaseModel


class AgentState(BaseModel):
    user_input: str = ""
    category: str = ""
    thinking: Annotated[list[str], add] = []
    response: str = ""
