from domain.modelos.Estudiante import Estudiante
from domain.modelos.Asignatura import Asignatura


class MatriculaRepository:
    def get_asignaturas_de_estudiante(self, db, estudiante_id: int):
        cursor = db.cursor()
        cursor.execute(
            "SELECT a.id, a.nombre, a.codigo, a.creditos, a.departamento, a.cuatrimestre FROM matriculas m JOIN asignaturas a ON m.asignatura_id = a.id WHERE m.estudiante_id = %s ORDER BY a.nombre",
            (estudiante_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
        return [Asignatura(id=r[0], nombre=r[1], codigo=r[2], creditos=r[3], departamento=r[4], cuatrimestre=r[5]) for r in rows]

    def get_estudiantes_de_asignatura(self, db, asignatura_id: int):
        cursor = db.cursor()
        cursor.execute(
            "SELECT e.id, e.nombre_completo, e.dni, e.email, e.fecha_nacimiento, e.titulacion FROM matriculas m JOIN estudiantes e ON m.estudiante_id = e.id WHERE m.asignatura_id = %s ORDER BY e.nombre_completo",
            (asignatura_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
        estudiantes = []
        for r in rows:
            fn = r[4]
            if fn is not None and not isinstance(fn, str):
                try:
                    fn = fn.isoformat()
                except Exception:
                    fn = str(fn)
            estudiantes.append(Estudiante(id=r[0], nombre_completo=r[1], dni=r[2], email=r[3], fecha_nacimiento=fn, titulacion=r[5]))
        return estudiantes

    def asignar(self, db, estudiante_id: int, asignatura_id: int, anio_academico: str = None):
        cursor = db.cursor()
        cursor.execute("INSERT IGNORE INTO matriculas (estudiante_id, asignatura_id, anio_academico) VALUES (%s,%s,%s)", (estudiante_id, asignatura_id, anio_academico))
        db.commit()
        cursor.close()

    def quitar(self, db, estudiante_id: int, asignatura_id: int):
        cursor = db.cursor()
        cursor.execute("DELETE FROM matriculas WHERE estudiante_id=%s AND asignatura_id=%s", (estudiante_id, asignatura_id))
        db.commit()
        cursor.close()

    def existe_matricula(self, db, estudiante_id: int, asignatura_id: int) -> bool:
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM matriculas WHERE estudiante_id=%s AND asignatura_id=%s", (estudiante_id, asignatura_id))
        count = cursor.fetchone()[0]
        cursor.close()
        return count > 0

    def get_all(self, db):
        """Devuelve todas las matriculas con datos de estudiante y asignatura"""
        cursor = db.cursor()
        cursor.execute(
            """
            SELECT m.estudiante_id, e.nombre_completo, m.asignatura_id, a.nombre, m.anio_academico, m.nota_final, m.fecha_matricula
            FROM matriculas m
            JOIN estudiantes e ON m.estudiante_id = e.id
            JOIN asignaturas a ON m.asignatura_id = a.id
            ORDER BY m.fecha_matricula DESC
            """,
        )
        rows = cursor.fetchall()
        cursor.close()
        result = []
        for r in rows:
            result.append({
                'estudiante_id': r[0],
                'estudiante_nombre': r[1],
                'asignatura_id': r[2],
                'asignatura_nombre': r[3],
                'anio_academico': r[4],
                'nota_final': r[5],
                'fecha_matricula': r[6],
            })
        return result
