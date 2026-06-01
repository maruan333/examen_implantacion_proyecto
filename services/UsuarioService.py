from database import get_database_connection
from repositorios.UsuarioRepository import UsuarioRepository


class UsuarioService:
    def __init__(self):
        self.repo = UsuarioRepository()

    def get_by_username(self, username: str):
        db = get_database_connection()
        u = self.repo.get_by_username(db, username)
        db.close()
        return u

    def get_by_id(self, user_id: int):
        db = get_database_connection()
        u = self.repo.get_by_id(db, user_id)
        db.close()
        return u

    def verificar_password(self, plain: str, password_hash) -> bool:
        return self.repo.verificar_password(plain, password_hash)

    def authenticate(self, username: str, password: str):
        """Devuelve el usuario (dict) si las credenciales son válidas, o None."""
        u = self.get_by_username(username)
        if not u:
            return None
        if not self.verificar_password(password, u['password_hash']):
            return None
        return u
