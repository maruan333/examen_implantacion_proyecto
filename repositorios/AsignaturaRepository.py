from domain.modelos.Asignatura import Asignatura, AsignaturaCreate, AsignaturaUpdate


class AsignaturaRepository:
    def get_all(self, db):
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, codigo, creditos, departamento, cuatrimestre FROM asignaturas ORDER BY nombre")
        rows = cursor.fetchall()
        cursor.close()
        return [Asignatura(id=r[0], nombre=r[1], codigo=r[2], creditos=r[3], departamento=r[4], cuatrimestre=r[5]) for r in rows]

    def get_by_id(self, db, id: int):
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, codigo, creditos, departamento, cuatrimestre FROM asignaturas WHERE id = %s", (id,))
        r = cursor.fetchone()
        cursor.close()
        if not r:
            return None
        return Asignatura(id=r[0], nombre=r[1], codigo=r[2], creditos=r[3], departamento=r[4], cuatrimestre=r[5])

    def create(self, db, asignatura: AsignaturaCreate):
        cursor = db.cursor()
        cursor.execute("INSERT INTO asignaturas (nombre, codigo, creditos, departamento, cuatrimestre) VALUES (%s,%s,%s,%s,%s)", (asignatura.nombre, asignatura.codigo, asignatura.creditos, asignatura.departamento, asignatura.cuatrimestre))
        db.commit()
        cursor.close()

    def update(self, db, id: int, asignatura: AsignaturaUpdate):
        cursor = db.cursor()
        cursor.execute("UPDATE asignaturas SET nombre=%s, codigo=%s, creditos=%s, departamento=%s, cuatrimestre=%s WHERE id=%s", (asignatura.nombre, asignatura.codigo, asignatura.creditos, asignatura.departamento, asignatura.cuatrimestre, id))
        db.commit()
        cursor.close()

    def delete(self, db, id: int):
        cursor = db.cursor()
        cursor.execute("DELETE FROM asignaturas WHERE id = %s", (id,))
        db.commit()
        cursor.close()
