Proyecto examen - Gestión Académica

Arranque rápido:

1) Crear venv e instalar dependencias

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2) Inicializar la base de datos local (si tienes MySQL corriendo):

```bash
python init_db.py
```

3) Ejecutar la app:

```bash
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

4) Credenciales seed: admin / admin123  (rol admin) ; usuario / user123 (rol normal)
