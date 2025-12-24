import psycopg2
import os
from flask import Flask, render_template, request, url_for, redirect, session, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "1234")

# ------------------------
# Conexión PostgreSQL
# ------------------------
def get_db_connection():
    return psycopg2.connect(
        os.environ.get("DATABASE_URL"),
        sslmode="require"
    )

# ------------------------
# ADMIN LOGIN
# ------------------------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form.get("password")

        if password == "admin123":  # proyecto
            session["admin"] = True
            return redirect(url_for("foro"))

        return render_template(
            "login_admin.html",
            error="Contraseña incorrecta"
        )

    return render_template("login_admin.html")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("foro"))

# ------------------------
# PÁGINAS
# ------------------------
@app.route("/")
def inicio():
    return render_template("pagina-principal.html")


@app.route("/principal")
def principal():
    enviado = request.args.get("enviado")
    return render_template("pagina-secundaria.html", enviado=enviado)


@app.route("/encuesta")
def encuesta():
    return render_template("encuesta.html")


# ------------------------
# FORO
# ------------------------
@app.route("/foro")
def foro():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, email, comentarios, fecha
        FROM encuesta
        ORDER BY fecha DESC
    """)
    
    filas = cursor.fetchall()
    cursor.close()
    conn.close()

    comentarios = []
    for fila in filas:
        comentarios.append({
            "id": fila[0],
            "nombre": fila[1],
            "email": fila[2],
            "comentarios": fila[3],
            "fecha": fila[4]
        })

    return render_template(
        "foro.html",
        comentarios=comentarios,
        es_admin=session.get("admin", False)
    )


# ------------------------
# GUARDAR ENCUESTA (JS)
# ------------------------
@app.route("/guardar_encuesta", methods=["POST"])
def guardar_encuesta():
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO encuesta (nombre, email, genero, comentarios)
        VALUES (%s, %s, %s, %s)
    """, (
        data["nombre"],
        data["email"],
        data.get("genero"),
        data["comentarios"]
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"success": True})


# ------------------------
# ELIMINAR COMENTARIO (ADMIN)
# ------------------------
@app.route("/eliminar_comentario/<int:id>", methods=["DELETE"])
def eliminar_comentario(id):
    if not session.get("admin"):
        return jsonify({"success": False}), 403

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM encuesta WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"success": True})


# ------------------------
# INSTRUMENTOS
# ------------------------
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


# ------------------------
# RUN (Render)
# ------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
