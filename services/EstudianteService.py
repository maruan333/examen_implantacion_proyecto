from database import get_database_connection
from repositorios.EstudianteRepository import EstudianteRepository


class EstudianteService:
    def __init__(self):
        self.repo = EstudianteRepository()

    def get_all(self):
        db = get_database_connection()
        res = self.repo.get_all(db)
        db.close()
        return res

    def create(self, estudiante):
        db = get_database_connection()
        try:
            self.repo.create(db, estudiante)
        finally:
            db.close()

    def get_by_id(self, id: int):
        db = get_database_connection()
        res = self.repo.get_by_id(db, id)
        db.close()
        return res

    def update(self, id: int, estudiante):
        db = get_database_connection()
        try:
            self.repo.update(db, id, estudiante)
        finally:
            db.close()

    def delete(self, id: int):
        db = get_database_connection()
        try:
            self.repo.delete(db, id)
        finally:
            db.close()
