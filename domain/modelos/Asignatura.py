from pydantic import BaseModel
from typing import Optional


class AsignaturaBase(BaseModel):
    nombre: str
    codigo: str
    creditos: int
    departamento: Optional[str] = None
    cuatrimestre: Optional[str] = None


class AsignaturaCreate(AsignaturaBase):
    pass


class AsignaturaUpdate(AsignaturaBase):
    pass


class Asignatura(AsignaturaBase):
    id: int
