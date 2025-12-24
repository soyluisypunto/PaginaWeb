import mysql.connector
import os
from flask import Flask, render_template, request, url_for, redirect, session

app = Flask(__name__)

app.secret_key = "1234"
# Conexión con base de datos musica_db
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="musica_db"
        )
    except mysql.connector.Error as e:
        print("Error MySQL:", e)
        return None
#Ruta administrador
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form["password"]

        # contraseña fija (para proyecto)
        if password == "admin123":
            session["admin"] = True
            return redirect(url_for("foro"))
        else:
            return render_template(
                "login_admin.html",
                error="Contraseña incorrecta"
            )
    return render_template("login_admin.html")
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("foro"))

# Portada
@app.route("/")
def inicio():
    return render_template("pagina-principal.html")

# Página principal (instrumentos)
@app.route("/principal")
def principal():
    enviado = request.args.get("enviado")
    return render_template(
        "pagina-secundaria.html",
        enviado=enviado
    )

# Foro
@app.route("/foro")
def foro():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, nombre, email, comentarios, fecha
        FROM encuesta
        ORDER BY fecha DESC
    """)
    comentarios = cursor.fetchall()

    cursor.close()
    conn.close()

    es_admin = session.get("admin", False)

    return render_template(
        "foro.html",
        comentarios=comentarios,
        es_admin=es_admin
    )


# Encuesta
@app.route("/encuesta")
def encuesta():
    return render_template("encuesta.html")

# Eliminar comentario
@app.route("/eliminar_comentario/<int:id>", methods=["DELETE"])
def eliminar_comentario(id):
    if not session.get("admin"):
        return {"success": False}, 403

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM encuesta WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return {"success": True}

# Guardar Encuesta base de datos
@app.route("/guardar_encuesta", methods=["POST"])
def guardar_encuesta():
    nombre = request.form["nombre"]
    email = request.form["email"]
    genero = request.form.get("genero")
    comentarios = request.form["comentarios"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO encuesta (nombre, email, genero, comentarios)
        VALUES (%s, %s, %s, %s)
    """, (nombre, email, genero, comentarios))

    conn.commit()
    cursor.close()
    conn.close()

    return "", 200

# Instrumentos
@app.route("/bateria")
def bateria():
    return render_template("instrumentos/bateria.html")

@app.route("/flauta")
def flauta():
    return render_template("instrumentos/flautatraversa.html")

@app.route("/guitarra")
def guitarra():
    return render_template("instrumentos/guitarra.html")

@app.route("/piano")
def piano():
    return render_template("instrumentos/piano.html")

@app.route("/saxofon")
def saxofon():
    return render_template("instrumentos/saxofon.html")

@app.route("/violin")
def violin():
    return render_template("instrumentos/violin.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)