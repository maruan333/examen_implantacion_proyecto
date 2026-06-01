import bcrypt
from domain.modelos.Usuario import Usuario, UsuarioCreate


class UsuarioRepository:
    def crear_usuario(self, db, usuario: UsuarioCreate) -> int:
        cursor = db.cursor()
        password_hash = bcrypt.hashpw(usuario.password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO usuarios (username, password_hash, es_admin) VALUES (%s, %s, %s)",
            (usuario.username, password_hash, usuario.es_admin),
        )
        db.commit()
        uid = cursor.lastrowid
        cursor.close()
        return uid

    def get_by_username(self, db, username: str):
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, username, password_hash, es_admin FROM usuarios WHERE username = %s", (username,))
        row = cursor.fetchone()
        cursor.close()
        return row

    def verificar_password(self, plain: str, password_hash) -> bool:
        if isinstance(password_hash, bytearray):
            password_hash = bytes(password_hash)
        return bcrypt.checkpw(plain.encode('utf-8'), password_hash)

    def get_by_id(self, db, user_id: int):
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, username, es_admin FROM usuarios WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        cursor.close()
        if not row:
            return None
        return Usuario(**row)
