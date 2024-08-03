from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask import send_from_directory

from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "Develoteca"

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'sistema'

# Inicializar MySQL
mysql = MySQL(app)

CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA


#para mostrar la foto de los empleados
@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)



@app.route('/')
def index():
    sql = "SELECT * FROM empleados;"
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(sql)
    
    empleados = cursor.fetchall()
    print(empleados)

    conn.commit()
    cursor.close()
    return render_template('empleados/index.html', empleados = empleados)


@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connection
    cursor = conn.cursor()

    # Seleccionar la foto del empleado antes de eliminar el registro
    cursor.execute("SELECT foto FROM empleados WHERE id=%s", (id,))
    fila = cursor.fetchone()

    # Elimina la foto de la carpeta uploads
    if fila and fila[0]:
        archivo_a_eliminar = os.path.join(app.config['CARPETA'], fila[0])
        if os.path.exists(archivo_a_eliminar):
            os.remove(archivo_a_eliminar)
        else:
            print(f"Archivo a eliminar no encontrado: {archivo_a_eliminar}")

    # Elimina el registro de la tabla
    cursor.execute("DELETE FROM empleados WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    return redirect('/')    #regresa de DONDE VINO



@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id=%s", (id,))
    empleados = cursor.fetchall()

    conn.commit()
    cursor.close()
    return render_template('empleados/edit.html', empleados = empleados)



@app.route('/update', methods=['POST'])
def update():
    # Obtención de Datos del Formulario
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    id = request.form['txtID']

    # Verificar datos recibidos
    #print(f"Datos recibidos: Nombre={_nombre}, Correo={_correo}, Foto={_foto.filename}, ID={id}")

    # Conexión a la base de datos
    conn = mysql.connection
    cursor = conn.cursor()

    # Actualización de Datos en la base de datos SOLO de nombre y correo
    sql = "UPDATE empleados SET nombre = %s, correo = %s WHERE id=%s;"
    datos = (_nombre, _correo, id)
    cursor.execute(sql, datos)
    #print(f"Consulta SQL ejecutada: {cursor.rowcount} filas afectadas")

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    # Guardado de Nueva Foto
    if _foto.filename != '':
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save(os.path.join(app.config['CARPETA'], nuevoNombreFoto))

        cursor.execute("SELECT foto FROM empleados WHERE id=%s", (id,))
        fila = cursor.fetchone()

        if fila and fila[0]:
            archivo_a_eliminar = os.path.join(app.config['CARPETA'], fila[0])
            if os.path.exists(archivo_a_eliminar):
                os.remove(archivo_a_eliminar)
            else:
                print(f"Archivo de foto a eliminar NO encontrado: {archivo_a_eliminar}")

        cursor.execute("UPDATE empleados SET foto=%s WHERE id=%s", (nuevoNombreFoto, id))


    conn.commit()
    cursor.close()
    return redirect('/')




















@app.route('/update', methods = ['POST'])
def update_update_youtube():
    #Obtencion de Datos del Formulario
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    id = request.form['txtID']

    #Actualizacion de Datos en la base de datos
    sql = "UPDATE empleados SET nombre = %s, correo = %s WHERE id=%s;"
    datos = (_nombre, _correo, id)

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(sql, datos)   #chatgpt

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    #Guardado de Nueva Foto
    if _foto.filename != '':
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)

        cursor.execute("SELECT foto FROM empleados WHERE id=%s", (id,))
        fila = cursor.fetchone()
        if fila:
            print(f"Nombre del archivo en la base de datos: {fila[0]}")
        else:
            print("No se encontró el archivo en la base de datos.")

        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE empleados SET foto=%s WHERE id=%s", (nuevoNombreFoto, id))
        conn.commit()

    cursor.execute(sql, datos)
    #conn.commit()
    cursor.close()
    return redirect('/')



@app.route('/create')
def create():
    return render_template('empleados/create.html')



@app.route('/store', methods=['POST'])
def storage():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']

    if _nombre == '' or _correo =='' or _foto == '':
        flash("Recuerda llenar los datos de los campos")
        return redirect(url_for('create'))

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _foto.filename != '':
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)

    sql = "INSERT INTO empleados (nombre, correo, foto) VALUES (%s, %s, %s);"
    datos = (_nombre, _correo, nuevoNombreFoto)

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    cursor.close()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
