from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from sqlmodel import Field, SQLModel

# ------------------------------------------------------------------------------------------------
# Usuario


class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str
    senha: str


# ------------------------------------------------------------------------------------------------
# Admin





# ------------------------------------------------------------------------------------------------
# Cliente

