from flask import Flask, jsonify, request, send_file
from psycopg2 import connect, extras
from psycopg2.errors import UniqueViolation
import os


app = Flask(__name__)


def get_connection():

    if os.environ.get("DATABASE_URL", None):
        print(os.environ.get("DATABASE_URL"))
        return connect(os.environ.get("DATABASE_URL"))

    return connect(
        host=os.environ.get("DB_HOST", "cac_postgres"),
        port=int(os.environ.get("DB_PORT", "5432")),
        database=os.environ.get("DB_NAME", "cac_app"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "password"),
    )


@app.get("/api/movies")
def get_movies():

    # conectar a la bbdd
    conn = get_connection()
    # crear un cursor -- se encarga de ejecutar las queries
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

    # ejecutar la query para obtener registros
    cursor.execute("SELECT * FROM peliculas")
    movies = cursor.fetchall()

    # cerrar el cursor y la conexión
    cursor.close()
    conn.close()

    # retornar los resultados
    return jsonify(movies)


@app.post("/api/movies")
def create_movie():

    movie_data = request.get_json()

    # conectar a la bbdd
    try:
        conn = get_connection()
    except:
        return jsonify({"message": "Error de conexión a la base de datos"}), 500

    # crear un cursor -- se encarga de ejecutar las queries
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

    # ejecutar la query para obtener registros
    query = """
    INSERT INTO peliculas (titulo, sinopsis, url_pelicula, ano_extreno, duracion, categoria, actor, director)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING *
    """

    try:
        cursor.execute(
            query=query,
            vars=(
                movie_data["titulo"],
                movie_data["sinopsis"],
                movie_data["url_pelicula"],
                movie_data["ano_extreno"],
                movie_data["duracion"],
                movie_data["categoria"],
                movie_data["actor"],
                movie_data["director"],
            ),
        )
        movie = cursor.fetchone()
        conn.commit()

        if movie is None:
            return jsonify({"message": "Película NO creada..."}), 400

        # retornar los resultados
        return jsonify(movie), 201
    except UniqueViolation as err:
        return jsonify({"message": "La película YA existe..."}), 409

    finally:
        # cerrar el cursor y la conexión
        cursor.close()
        conn.close()


@app.get("/api/movies/<id_pelicula>")
def get_movie(id_pelicula):
    # conectar a la bbdd
    conn = get_connection()
    # crear un cursor -- se encarga de ejecutar las queries
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

    # ejecutar la query para obtener registros
    cursor.execute(
        query="SELECT * FROM peliculas WHERE id_pelicula = %s", vars=(id_pelicula,)
    )
    movie = cursor.fetchone()
    # cerrar el cursor y la conexión
    cursor.close()
    conn.close()

    if movie is None:
        return jsonify({"message": "Película NO encontrada..."}), 404

    # retornar los resultados
    return jsonify(movie)


@app.delete("/api/movies/<id_pelicula>")
def delete_movie(id_pelicula):
    # conectar a la bbdd
    conn = get_connection()
    # crear un cursor -- se encarga de ejecutar las queries
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

    # ejecutar la query para obtener registros
    cursor.execute(
        query="DELETE FROM peliculas WHERE id_pelicula = %s RETURNING *",
        vars=(id_pelicula,),
    )
    movie = cursor.fetchone()
    conn.commit()
    # cerrar el cursor y la conexión
    cursor.close()
    conn.close()

    if movie is None:
        return jsonify({"message": "Película NO encontrada..."}), 404

    # retornar los resultados
    return jsonify(movie)


# PUT / PATCH
@app.patch("/api/movies/<id_pelicula>")
def update_movie(id_pelicula):
    return {"title": "Spiderman 2", "year": 2002, "id": id_pelicula}


@app.put("/api/movies/<id_pelicula>")
def update_movie_put(id_pelicula):

    movie_data = request.get_json()

    # conectar a la bbdd
    conn = get_connection()
    # crear un cursor -- se encarga de ejecutar las queries
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

    # ejecutar la query para obtener registros
    query = """
    UPDATE peliculas
    SET
        titulo = %s,
        sinopsis = %s,
        url_pelicula = %s,
        ano_extreno = %s,
        duracion = %s,
        categoria = %s,
        actor = %s,
        director = %s
    WHERE id_pelicula = %s
    RETURNING *
    """
    cursor.execute(
        query=query,
        vars=(
            movie_data["titulo"],
            movie_data["sinopsis"],
            movie_data["url_pelicula"],
            movie_data["ano_extreno"],
            movie_data["duracion"],
            movie_data["categoria"],
            movie_data["actor"],
            movie_data["director"],
            id_pelicula,
        ),
    )
    movie = cursor.fetchone()
    conn.commit()

    # cerrar el cursor y la conexión
    cursor.close()
    conn.close()

    if movie is None:
        return jsonify({"message": "Película NO encontrada..."}), 404

    # retornar los resultados
    return jsonify(movie)


@app.get("/")
def home():
    return send_file("templates/index.html")


# VER BIEN DE ACA HACIA ABAJO
@app.route("/images", methods=["GET", "POST"])
def images():

    if request.method == "GET":
        return send_file("static/images.html")

    if request.method == "POST":
        file = request.files["image"]
        file.save(f'static/uploads/{file.name}.{file.filename.split(".")[-1]}')
        return jsonify({"message": "Ok"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
