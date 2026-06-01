from database import get_database_connection
from repositorios.AsignaturaRepository import AsignaturaRepository


class AsignaturaService:
    def __init__(self):
        self.repo = AsignaturaRepository()

    def get_all(self):
        db = get_database_connection()
        res = self.repo.get_all(db)
        db.close()
        return res

    def create(self, asignatura):
        db = get_database_connection()
        try:
            self.repo.create(db, asignatura)
        finally:
            db.close()

    def get_by_id(self, id: int):
        db = get_database_connection()
        res = self.repo.get_by_id(db, id)
        db.close()
        return res

    def update(self, id: int, asignatura):
        db = get_database_connection()
        try:
            self.repo.update(db, id, asignatura)
        finally:
            db.close()

    def delete(self, id: int):
        db = get_database_connection()
        try:
            self.repo.delete(db, id)
        finally:
            db.close()
