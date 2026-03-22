# ============================================================
#  app.py  –  Archivo principal de la aplicación Flask
#  Proyecto: Lista de Tareas (To-Do List)
# ============================================================

from flask import Flask, render_template, request, redirect, url_for
#importamos sqlite3 para manejar la base de datos
import sqlite3
# ----------------------------------------------------------
# 1. Crear la aplicación Flask
# ----------------------------------------------------------
app = Flask(__name__)

def obtener_conexion():
    conn = sqlite3.connect('tareas.db')
    # Esto permite acceder a las columnas por nombre 
    # Hace que se comporte igual que tu lista de diccionarios anterior
    conn.row_factory = sqlite3.Row 
    return conn


## Funcion que crea la tabla, verifica si existe y si no la crea, se llama al iniciar la app

def inicializar_bd():
    conn = obtener_conexion()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            completada BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Contador global para asignar IDs únicos a cada tarea nueva
siguiente_id = 0


# ===========================================================
#  RUTAS DE LA APLICACIÓN
# ===========================================================

# ----------------------------------------------------------
# RUTA 1 – Página de inicio  (GET /)
#  - Redirige al listado de tareas
# ----------------------------------------------------------
@app.route("/")
def inicio():
    return redirect(url_for("lista_tareas"))


# ----------------------------------------------------------
# RUTA 2 – Listar tareas  (GET /tareas)
#  Muestra todas las tareas y un contador dinámico
# ----------------------------------------------------------
@app.route("/tareas")
def lista_tareas():
    ## obtenemos una conexión a la base de datos y obtenemos las tareas guardadas
    conn = obtener_conexion()
    # Obtenemos todas las tareas de la base de datos
    
    # se guarda la lista de tareas como un array de diccionarios.
    # ferchall() devuelve una lista de filas, cada fila es un diccionario gracias a row_factory
    # row_factory es una función que le dice a SQLite cómo formatear los resultados de las consultas.
    tareas_bd = conn.execute('SELECT * FROM tareas').fetchall()
    # se cierra la conexion para liberar recursos
    conn.close()
    total      = len(tareas_bd)
    completadas = sum(1 for t in tareas_bd if t["completada"])
    pendientes  = total - completadas

    # Pasamos datos dinámicos a la plantilla (concepto 12)
    return render_template(
        "index.html",
        tareas=tareas_bd,
        total=total,
        completadas=completadas,
        pendientes=pendientes,
    )


# ----------------------------------------------------------
# RUTA 3 – Crear tarea  (GET y POST /tareas/nueva)
#  GET  → muestra el formulario vacío
#  POST → procesa el formulario y guarda la tarea (concepto 13)
# ----------------------------------------------------------
@app.route("/tareas/nueva", methods=["GET", "POST"])
def nueva_tarea():
    global siguiente_id

    if request.method == "POST":
        # Leemos los datos enviados por el formulario
        titulo      = request.form.get("titulo", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        if titulo:
            conn = obtener_conexion()
            # los ?  son marcadores por posicion
            conn.execute(
                'INSERT INTO tareas (titulo, descripcion, completada) VALUES (?, ?, ?)',
                (titulo, descripcion, False)
            )
            conn.commit()
            conn.close()

        return redirect(url_for("lista_tareas"))

    # Si es GET, solo mostramos el formulario
    return render_template("nueva_tarea.html")


# ----------------------------------------------------------
# RUTA 4 – Marcar tarea como completada  (GET /tareas/<id>/completar)
# ----------------------------------------------------------
@app.route("/tareas/<int:tarea_id>/completar")
def completar_tarea(tarea_id):
    conn = obtener_conexion()
    conn.execute('UPDATE tareas SET completada = NOT completada WHERE id = ?', (tarea_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("lista_tareas"))
    


# ----------------------------------------------------------
# RUTA 5 – Eliminar tarea  (GET /tareas/<id>/eliminar)
# ----------------------------------------------------------
@app.route("/tareas/<int:tarea_id>/eliminar")
def eliminar_tarea(tarea_id):
    conn = obtener_conexion()
    conn.execute('DELETE FROM tareas WHERE id = ?', (tarea_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("lista_tareas"))


# ----------------------------------------------------------
# RUTA 6 – Página "Acerca de"  (GET /acerca)
#  Muestra información del proyecto (segunda página)
# ----------------------------------------------------------
@app.route("/acerca")
def acerca():
    info = {
        "nombre":    "Lista de Tareas Flask",
        "version":   "1.0",
        "autor":     "Estudiante Python",
        "tecnologias": ["Python", "Flask", "Jinja2", "HTML/CSS"],
    }
    return render_template("acerca.html", info=info)


# ===========================================================
#  PUNTO DE ENTRADA
#  debug=True → recarga automática al guardar (concepto 8)
# ===========================================================
if __name__ == "__main__":
    inicializar_bd() # llamamos al iniciar la app para asegurarnos que la tabla exista  
    app.run(debug=True)
