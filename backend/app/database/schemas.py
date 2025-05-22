from pydantic import BaseModel, EmailStr

# ------------------------------------------------------------------------------------------------
# Usuario

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr


class UsuarioCreate(UsuarioBase):
    senha: str


class UsuarioSchema(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

# ------------------------------------------------------------------------------------------------
# Token

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None