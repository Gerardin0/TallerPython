# ============================================================
#  app.py  –  Archivo principal de la aplicación Flask
#  Proyecto: Lista de Tareas (To-Do List)
# ============================================================
#
#  CONCEPTOS QUE CUBRE ESTE ARCHIVO:
#   6. Definir rutas que responden con texto o HTML
#   7. Ejecutar el servidor y ver la respuesta en el navegador
#   8. Modificar la respuesta y observar el cambio en tiempo real
#  13. Recibir datos de un formulario y mostrarlos
# ============================================================

from flask import Flask, render_template, request, redirect, url_for

# ----------------------------------------------------------
# 1. Crear la aplicación Flask
# ----------------------------------------------------------
app = Flask(__name__)

# ----------------------------------------------------------
# 2. "Base de datos" temporal en memoria (lista de diccionarios)
#    En un proyecto real, esto se reemplazaría por SQLite.
#    Cada tarea tiene: id, título, descripción y estado.
# ----------------------------------------------------------
tareas = [
    {"id": 1, "titulo": "Aprender Flask",       "descripcion": "Estudiar rutas y plantillas", "completada": False},
    {"id": 2, "titulo": "Crear un proyecto",    "descripcion": "Aplicar lo aprendido",        "completada": False},
    {"id": 3, "titulo": "Conectar SQLite",       "descripcion": "Persistir datos en disco",   "completada": False},
]

# Contador global para asignar IDs únicos a cada tarea nueva
siguiente_id = 4


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
    total      = len(tareas)
    completadas = sum(1 for t in tareas if t["completada"])
    pendientes  = total - completadas

    # Pasamos datos dinámicos a la plantilla (concepto 12)
    return render_template(
        "index.html",
        tareas=tareas,
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

        if titulo:                          # Validación mínima
            tarea_nueva = {
                "id":          siguiente_id,
                "titulo":      titulo,
                "descripcion": descripcion,
                "completada":  False,
            }
            tareas.append(tarea_nueva)
            siguiente_id += 1

        return redirect(url_for("lista_tareas"))

    # Si es GET, solo mostramos el formulario
    return render_template("nueva_tarea.html")


# ----------------------------------------------------------
# RUTA 4 – Marcar tarea como completada  (GET /tareas/<id>/completar)
# ----------------------------------------------------------
@app.route("/tareas/<int:tarea_id>/completar")
def completar_tarea(tarea_id):
    for tarea in tareas:
        if tarea["id"] == tarea_id:
            tarea["completada"] = not tarea["completada"]   # Toggle
            break
    return redirect(url_for("lista_tareas"))


# ----------------------------------------------------------
# RUTA 5 – Eliminar tarea  (GET /tareas/<id>/eliminar)
# ----------------------------------------------------------
@app.route("/tareas/<int:tarea_id>/eliminar")
def eliminar_tarea(tarea_id):
    global tareas
    tareas = [t for t in tareas if t["id"] != tarea_id]
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
    app.run(debug=True)
