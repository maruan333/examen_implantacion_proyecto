from domain.modelos.Estudiante import Estudiante, EstudianteCreate, EstudianteUpdate
from datetime import date, datetime


class EstudianteRepository:
    def get_all(self, db):
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre_completo, dni, email, fecha_nacimiento, titulacion FROM estudiantes ORDER BY nombre_completo")
        rows = cursor.fetchall()
        cursor.close()
        estudiantes = []
        for r in rows:
            fn = r[4]
            if fn is not None and not isinstance(fn, str):
                # convertir date/datetime a string ISO
                try:
                    fn = fn.isoformat()
                except Exception:
                    fn = str(fn)
            estudiantes.append(Estudiante(id=r[0], nombre_completo=r[1], dni=r[2], email=r[3], fecha_nacimiento=fn, titulacion=r[5]))
        return estudiantes

    def get_by_id(self, db, id: int):
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre_completo, dni, email, fecha_nacimiento, titulacion FROM estudiantes WHERE id = %s", (id,))
        r = cursor.fetchone()
        cursor.close()
        if not r:
            return None
        fn = r[4]
        if fn is not None and not isinstance(fn, str):
            try:
                fn = fn.isoformat()
            except Exception:
                fn = str(fn)
        return Estudiante(id=r[0], nombre_completo=r[1], dni=r[2], email=r[3], fecha_nacimiento=fn, titulacion=r[5])

    def create(self, db, estudiante: EstudianteCreate):
        cursor = db.cursor()
        cursor.execute("INSERT INTO estudiantes (nombre_completo, dni, email, fecha_nacimiento, titulacion) VALUES (%s,%s,%s,%s,%s)", (estudiante.nombre_completo, estudiante.dni, estudiante.email, estudiante.fecha_nacimiento, estudiante.titulacion))
        db.commit()
        cursor.close()

    def update(self, db, id: int, estudiante: EstudianteUpdate):
        cursor = db.cursor()
        cursor.execute("UPDATE estudiantes SET nombre_completo=%s, dni=%s, email=%s, fecha_nacimiento=%s, titulacion=%s WHERE id=%s", (estudiante.nombre_completo, estudiante.dni, estudiante.email, estudiante.fecha_nacimiento, estudiante.titulacion, id))
        db.commit()
        cursor.close()

    def delete(self, db, id: int):
        cursor = db.cursor()
        cursor.execute("DELETE FROM estudiantes WHERE id = %s", (id,))
        db.commit()
        cursor.close()
