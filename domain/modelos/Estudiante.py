from pydantic import BaseModel
from typing import Optional


class EstudianteBase(BaseModel):
    nombre_completo: str
    dni: str
    email: str
    fecha_nacimiento: Optional[str] = None
    titulacion: Optional[str] = None


class EstudianteCreate(EstudianteBase):
    pass


class EstudianteUpdate(EstudianteBase):
    pass


class Estudiante(EstudianteBase):
    id: int
