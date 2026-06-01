from pydantic import BaseModel


class Usuario(BaseModel):
    id: int
    username: str
    es_admin: bool


class UsuarioCreate(BaseModel):
    username: str
    password: str
    es_admin: bool = False
