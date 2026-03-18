# ✅ TodoFlask — Proyecto educativo de Flask

Aplicación de lista de tareas construida con **Python + Flask** para
aprender los conceptos fundamentales del desarrollo web backend.

---

## 🗂 Estructura del proyecto

```
todo_app/
├── app.py                 ← Punto de entrada y rutas
├── requirements.txt       ← Dependencias
├── README.md              ← Este archivo
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

---

## 📚 Conceptos cubiertos

| # | Concepto                                | Archivo              |
|---|------------------------------------------|----------------------|
| 6 | Definir rutas con `@app.route()`         | `app.py`             |
| 7 | Ejecutar el servidor y ver en navegador  | `app.py`             |
| 8 | Modificar y observar cambios en tiempo real | `app.py` + `debug=True` |
| 9 | Estructura de carpetas para Flask        | Directorio raíz      |
|10 | Plantilla base con navbar y footer       | `base.html`          |
|11 | Páginas que heredan de la base           | `index.html`, `acerca.html` |
|12 | Mostrar datos dinámicos (lista, contadores) | `index.html`, `acerca.html` |
|13 | Formulario y mostrar lo que el usuario envió | `nueva_tarea.html` |

---

## ➡️ Próximo paso: conectar SQLite

Cuando estés listo, reemplaza la lista `tareas` en `app.py` por una
base de datos real. Aquí una guía rápida:

```python
import sqlite3

def get_db():
    conn = sqlite3.connect("tareas.db")
    conn.row_factory = sqlite3.Row   # Acceso por nombre de columna
    return conn

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo      TEXT    NOT NULL,
            descripcion TEXT,
            completada  INTEGER DEFAULT 0
        )
    """)
    db.commit()
    db.close()
```

Llama a `init_db()` una vez al inicio y luego reemplaza las operaciones
sobre la lista por consultas SQL (`SELECT`, `INSERT`, `UPDATE`, `DELETE`).
