# ✅ TodoFlask — Proyecto educativo de Flask

Aplicación de lista de tareas construida con **Python + Flask** para
aprender los conceptos fundamentales del desarrollo web backend.

---

## 🗂 Estructura del proyecto

```text
todo_app/
├── app.py                 ← Punto de entrada y rutas (lógica principal)
├── requirements.txt       ← Dependencias del proyecto
├── README.md              ← Este archivo
├── tareas.db              ← Base de datos SQLite (se genera automáticamente)
├── templates/
│   ├── base.html          ← Plantilla base (navbar, footer)
│   ├── index.html         ← Lista de tareas
│   ├── nueva_tarea.html   ← Formulario para crear tareas
│   └── acerca.html        ← Información del proyecto
└── static/
    ├── css/
    │   └── estilos.css    ← Hoja de estilos
    └── js/
        └── (vacío — para código JavaScript futuro)

```

---

## 🚀 Cómo ejecutar el proyecto

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Iniciar el servidor de desarrollo
python app.py

# 3. Abrir en el navegador
http://127.0.0.1:5000
```

> **Tip:** Con `debug=True` el servidor se recarga automáticamente cada
> vez que guardas `app.py`. ¡Modifica una respuesta y observa el cambio!




## ➡️ Conexión a SQLite (Base de Datos)

El proyecto utiliza el módulo nativo sqlite3 de Python para persistir las tareas en disco, reemplazando las listas temporales en memoria.

La base de datos se inicializa automáticamente al arrancar la aplicación con esta estructura:

```python
import sqlite3

def obtener_conexion():
    conn = sqlite3.connect("tareas.db")
    # row_factory permite acceder a las columnas por su nombre (ej. fila['titulo'])
    conn.row_factory = sqlite3.Row   
    return conn

def inicializar_bd():
    conn = obtener_conexion()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo      TEXT    NOT NULL,
            descripcion TEXT,
            completada  BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
```


