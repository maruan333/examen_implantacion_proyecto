from database import get_database_connection
from repositorios.MatriculaRepository import MatriculaRepository


class MatriculaService:
    def __init__(self):
        self.repo = MatriculaRepository()

    def get_asignaturas_de_estudiante(self, estudiante_id: int):
        db = get_database_connection()
        res = self.repo.get_asignaturas_de_estudiante(db, estudiante_id)
        db.close()
        return res

    def get_estudiantes_de_asignatura(self, asignatura_id: int):
        db = get_database_connection()
        res = self.repo.get_estudiantes_de_asignatura(db, asignatura_id)
        db.close()
        return res

    def asignar(self, estudiante_id: int, asignatura_id: int, anio_academico: str = None):
        db = get_database_connection()
        try:
            self.repo.asignar(db, estudiante_id, asignatura_id, anio_academico)
        finally:
            db.close()

    def quitar(self, estudiante_id: int, asignatura_id: int):
        db = get_database_connection()
        try:
            self.repo.quitar(db, estudiante_id, asignatura_id)
        finally:
            db.close()

    def existe_matricula(self, estudiante_id: int, asignatura_id: int) -> bool:
        db = get_database_connection()
        res = self.repo.existe_matricula(db, estudiante_id, asignatura_id)
        db.close()
        return res

    def get_all(self):
        db = get_database_connection()
        res = self.repo.get_all(db)
        db.close()
        return res
