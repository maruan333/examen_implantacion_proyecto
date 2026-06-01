import os
from database import get_database_connection
import bcrypt

SQL_SCHEMA = open("init.sql","r",encoding='utf-8').read()

if __name__ == '__main__':
    db = get_database_connection()
    cursor = db.cursor()
    for stmt in SQL_SCHEMA.split(';'):
        s = stmt.strip()
        if s:
            cursor.execute(s)
    db.commit()

    # Crear usuarios seed
    admin_pass = b"admin123"
    user_pass = b"user123"
    admin_hash = bcrypt.hashpw(admin_pass, bcrypt.gensalt())
    user_hash = bcrypt.hashpw(user_pass, bcrypt.gensalt())

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO usuarios (username, password_hash, es_admin) VALUES (%s, %s, %s)", ("admin", admin_hash, True))
        cursor.execute("INSERT INTO usuarios (username, password_hash, es_admin) VALUES (%s, %s, %s)", ("usuario", user_hash, False))
        db.commit()
        print('Usuarios seed creados: admin / usuario')
    else:
        print('Usuarios ya existen, saltando seed')

    cursor.close()
    db.close()
