import os
from flask import Flask, render_template, request, redirect, url_for, Blueprint, jsonify, send_from_directory,session
from werkzeug.utils import secure_filename
from firebase import firebase
import binascii

# Generar una cadena aleatoria de bytes
secret_key = binascii.hexlify(os.urandom(24)).decode()

print("Secret Key generada:", secret_key)




app = Flask(__name__, template_folder='logeo/templates', static_folder='static')

app.secret_key = 'tu_clave_secreta_generada'



admin_app = Blueprint('admin_app', __name__, template_folder='admin/templates')

firebase = firebase.FirebaseApplication("https://base-20e8f-default-rtdb.firebaseio.com/", None)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/terminos_condiciones')
def terminos_condiciones():
    return render_template('terminos_condiciones.html')

@app.route('/avisos_privacidad')
def avisos_privacidad():
    return render_template('avisos_privacidad.html')




def obtener_user_id_de_la_sesion():

    return "user_id_ficticio"

@app.route('/descargar_pdf/<string:proyecto_id>', methods=['GET'])
def descargar_pdf(proyecto_id):
    proyecto = firebase.get('/Proyectos', proyecto_id)
    
    if proyecto:
        nombre_archivo_pdf = proyecto.get('nombre_del_archivo_pdf')
        
        if nombre_archivo_pdf:
            return send_from_directory(app.config['UPLOAD_FOLDER'], nombre_archivo_pdf)
    
    return jsonify({"message": "El archivo PDF no existe"}), 404

def obtener_usuarios():
    usuarios = firebase.get('/Usuarios', None)
    return [{**usuario, 'id': usuario_id} for usuario_id, usuario in usuarios.items()] if usuarios else []

def obtener_proyectos():
    proyectos = firebase.get('/Proyectos', None)
    return [{**proyecto, 'id': proyecto_id} for proyecto_id, proyecto in proyectos.items()] if proyectos else []

@admin_app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        ocupacion = request.form['ocupacion']
        institucion = request.form['institucion']
        edad = request.form['edad']
        nombre_completo = request.form['nombre_completo']
        
        if email and contraseña and ocupacion and institucion and edad and nombre_completo:
            datos_usuario = {
                'email': email,
                'contraseña': contraseña,
                'ocupacion': ocupacion,
                'institucion': institucion,
                'edad': edad,
                'nombre_completo': nombre_completo
            }
            firebase.post('/Usuarios', datos_usuario)
            return redirect(url_for('admin_app.usuarios'))
    
    lista_usuarios = obtener_usuarios()
    lista_proyectos = obtener_proyectos()
    
    return render_template('admin_index.html', usuarios=lista_usuarios, proyectos=lista_proyectos)

@admin_app.route('/editar_usuario/<string:usuario_id>', methods=['POST'])
def editar_usuario(usuario_id):
    usuario = firebase.get('/Usuarios', usuario_id)
    if request.method == 'POST' and usuario:
        email = request.json.get('email', usuario.get('email'))
        ocupacion = request.json.get('ocupacion', usuario.get('ocupacion'))
        institucion = request.json.get('institucion', usuario.get('institucion'))
        edad = request.json.get('edad', usuario.get('edad'))
        nombre_completo = request.json.get('nombre_completo', usuario.get('nombre_completo'))
        
        datos_usuario = {}
        if email:
            datos_usuario['email'] = email
        if ocupacion:
            datos_usuario['ocupacion'] = ocupacion
        if institucion:
            datos_usuario['institucion'] = institucion
        if edad:
            datos_usuario['edad'] = edad
        if nombre_completo:
            datos_usuario['nombre_completo'] = nombre_completo
        
        if datos_usuario:
            firebase.put('/Usuarios', usuario_id, datos_usuario)
            return jsonify({"message": "Usuario actualizado correctamente"})
    
    return jsonify({"message": "Error al actualizar usuario"})

@admin_app.route('/proyectos', methods=['GET', 'POST'])
def proyectos():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        autor = request.form['autor']
        fecha_publicacion = request.form['fecha_publicacion']
        palabras_clave = request.form['palabras_clave']
        
        if titulo and descripcion and autor and fecha_publicacion and palabras_clave:
            datos_proyecto = {
                'titulo': titulo,
                'descripcion': descripcion,
                'autor': autor,
                'fecha_publicacion': fecha_publicacion,
                'palabras_clave': palabras_clave
            }
            firebase.post('/Proyectos', datos_proyecto)
            return redirect(url_for('admin_app.proyectos'))
    
    lista_proyectos = obtener_proyectos()
    lista_usuarios = obtener_usuarios()
    
    return render_template('admin_index.html', proyectos=lista_proyectos, usuarios=lista_usuarios)

@admin_app.route('/editar_proyecto/<string:proyecto_id>', methods=['POST'])
def editar_proyecto(proyecto_id):
    proyecto = firebase.get('/Proyectos', proyecto_id)
    if request.method == 'POST' and proyecto:
        titulo = request.json.get('titulo', proyecto.get('titulo'))
        descripcion = request.json.get('descripcion', proyecto.get('descripcion'))
        autor = request.json.get('autor', proyecto.get('autor'))
        fecha_publicacion = request.json.get('fecha_publicacion', proyecto.get('fecha_publicacion'))
        palabras_clave = request.json.get('palabras_clave', proyecto.get('palabras_clave'))
        
        datos_proyecto = {}
        if titulo:
            datos_proyecto['titulo'] = titulo
        if descripcion:
            datos_proyecto['descripcion'] = descripcion
        if autor:
            datos_proyecto['autor'] = autor
        if fecha_publicacion:
            datos_proyecto['fecha_publicacion'] = fecha_publicacion
        if palabras_clave:
            datos_proyecto['palabras_clave'] = palabras_clave
        
        if datos_proyecto:
            firebase.put('/Proyectos', proyecto_id, datos_proyecto)
            return jsonify({"message": "Proyecto actualizado correctamente"})
    
    return jsonify({"message": "Error al actualizar proyecto"})
@admin_app.route('/eliminar_usuario/<string:usuario_id>', methods=['DELETE'])
def eliminar_usuario(usuario_id):
    firebase.delete('/Usuarios', usuario_id)
    return jsonify({"message": "Usuario eliminado correctamente"})

@admin_app.route('/eliminar_proyecto/<string:proyecto_id>', methods=['DELETE'])
def eliminar_proyecto(proyecto_id):
    proyecto = firebase.get('/Proyectos', proyecto_id)
    if proyecto:
        nombre_archivo_pdf = proyecto.get('nombre_del_archivo_pdf')
        if nombre_archivo_pdf:
            ruta_pdf = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo_pdf)
            if os.path.exists(ruta_pdf):
                os.remove(ruta_pdf)
        
        firebase.delete('/Proyectos', proyecto_id)
        return jsonify({"message": "Proyecto eliminado correctamente"})
    
    return jsonify({"message": "Proyecto no encontrado"})


@admin_app.route('/subir_pdf/<string:proyecto_id>', methods=['POST'])
def subir_pdf(proyecto_id):
    archivo_pdf = request.files['archivo_pdf']
    
    if archivo_pdf.filename == '':
        return jsonify({"message": "No se seleccionó ningún archivo PDF"}), 400
    
    if archivo_pdf:
        nombre_archivo_pdf = secure_filename(archivo_pdf.filename)
        ruta_guardado = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo_pdf)
        archivo_pdf.save(ruta_guardado)
        
        proyecto = firebase.get('/Proyectos', proyecto_id)
        if proyecto:
            proyecto['nombre_del_archivo_pdf'] = nombre_archivo_pdf
            firebase.put('/Proyectos', proyecto_id, proyecto)
            return jsonify({"message": "Archivo PDF subido correctamente"}), 200
    
    return jsonify({"message": "Error al subir archivo PDF"}), 500

app.register_blueprint(admin_app)

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    resultados = None
    
    if request.method == 'POST':
        consulta = request.form['consulta']
        resultados = obtener_resultados_simple(consulta)
    elif request.method == 'GET':
        titulo = request.args.get('titulo')
        autor = request.args.get('autor')
        palabras_clave = request.args.get('palabras_clave')
        resultados = obtener_resultados_avanzados(titulo, autor, palabras_clave)
    
    return render_template('search_index.html', resultados=resultados)

def obtener_resultados_simple(consulta):
    proyectos = firebase.get('/Proyectos', None)
    resultados = []
    if proyectos:
        for proyecto_id, proyecto in proyectos.items():
            nombre_archivo_pdf = proyecto.get('nombre_del_archivo_pdf', '')
            if nombre_archivo_pdf and consulta.lower() in nombre_archivo_pdf.lower():
                resultados.append({
                    'titulo': proyecto.get('titulo', ''),
                    'autor': proyecto.get('autor', ''),
                    'palabras_clave': proyecto.get('palabras_clave', ''),
                    'nombre_archivo_pdf': nombre_archivo_pdf
                })
    return resultados

def obtener_resultados_avanzados(titulo, autor, palabras_clave):
    proyectos = firebase.get('/Proyectos', None)
    resultados = []
    if proyectos:
        for proyecto_id, proyecto in proyectos.items():
            if (not titulo or titulo.lower() in proyecto.get('titulo', '').lower()) and \
               (not autor or autor.lower() in proyecto.get('autor', '').lower()) and \
               (not palabras_clave or palabras_clave.lower() in proyecto.get('palabras_clave', '').lower()):
                resultados.append({
                    'id': proyecto_id,
                    'titulo': proyecto.get('titulo', ''),
                    'autor': proyecto.get('autor', ''),
                    'palabras_clave': proyecto.get('palabras_clave', '')
                })
    return resultados


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Eliminar la sesión del usuario
    session.clear()
    # Redirigir a la página de inicio de sesión
    return redirect(url_for('login'))

from flask import redirect

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Obtener los datos del formulario de registro
        email = request.form['email']
        contraseña = request.form['contraseña']
        
        if email and contraseña:
            # Guardar los datos de correo electrónico y contraseña en la base de datos Firebase
            datos_usuario = {
                'email': email,
                'contraseña': contraseña
            }
            # Registrar al usuario y obtener su ID único generado por Firebase
            nuevo_usuario = firebase.post('/Usuarios', datos_usuario)
            # Obtener el ID único generado para este usuario
            user_id = nuevo_usuario['name']
            
            # Redirigir a la página para completar los datos personales
            return redirect(url_for('datos', user_id=user_id))
    
    return render_template('registro.html')


@app.route('/perfil/<string:user_id>', methods=['GET', 'POST'])
def perfil(user_id):
    # Obtener los datos del usuario desde Firebase
    datos_usuario = firebase.get('/Usuarios', user_id)

    if request.method == 'POST':
        # Obtener los datos actualizados del formulario
        nombre = request.form['nombre']
        edad = request.form['edad']
        ocupacion = request.form['ocupacion']
        institucion = request.form['institucion']

        # Actualizar los datos del usuario en Firebase, excluyendo correo y contraseña
        firebase.put('/Usuarios', user_id, {
            'nombre_completo': nombre,
            'edad': edad,
            'ocupacion': ocupacion,
            'institucion': institucion,
            'email': datos_usuario['email'],  # Mantener el correo electrónico sin cambios
            'contraseña': datos_usuario['contraseña']  # Mantener la contraseña sin cambios
        })

        # Redirigir a la página de perfil
        return redirect(url_for('perfil', user_id=user_id))

    return render_template('perfil.html', user_id=user_id, datos=datos_usuario)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        
        if email == 'admin@gmail.com' and contraseña == '123':
            return redirect(url_for('admin_app.usuarios'))
        
        # Obtener todos los usuarios de la base de datos
        usuarios = obtener_usuarios()
        
        # Buscar el usuario por correo electrónico
        usuario = next((u for u in usuarios if u.get('email') == email), None)
        
        # Verificar si se encontró el usuario y si la contraseña coincide
        if usuario and usuario.get('contraseña') == contraseña:
         # Establecer el ID del usuario en la sesión para mantenerla
            session['user_id'] = usuario['id']
            return redirect(url_for('buscar'))  # Redirigir al usuario a la página de búsqueda
        else:
        # Si el usuario no se encuentra o la contraseña no coincide, mostrar una alerta
            mensaje = "Correo electrónico o contraseña incorrectos. Inténtalo de nuevo."
            return render_template('login.html', error=mensaje)


        #return "Correo electrónico o contraseña incorrectos. Inténtalo de nuevo."

    return render_template('login.html')


@app.route('/datos/<string:user_id>', methods=['GET', 'POST'])
def datos(user_id):
    if request.method == 'POST':
        # Obtener los datos del formulario de datos
        nombre = request.form['nombre']
        edad = request.form['edad']
        ocupacion = request.form['ocupacion']
        institucion = request.form['institucion']

        if user_id:
            # Obtener los datos actuales del usuario
            usuario = firebase.get('/Usuarios', user_id)
            
            # Actualizar los datos del usuario en Firebase
            datos_usuario = {
                'email': usuario.get('email'),
                'contraseña': usuario.get('contraseña'),
                'nombre_completo': nombre,
                'edad': edad,
                'ocupacion': ocupacion,
                'institucion': institucion
            }
            
            firebase.put('/Usuarios', user_id, datos_usuario)
            
            # Redirigir a la página de perfil
            return redirect(url_for('perfil', user_id=user_id))

    return render_template('datos.html', user_id=user_id)

@app.route('/recuperar_contraseña', methods=['GET', 'POST'])
def recuperar_contraseña():
    if request.method == 'POST':
        correo = request.form['correo']
        usuario = next((u for u in obtener_usuarios() if u['email'] == correo), None)
        
        if usuario:
            # Aquí puedes implementar el envío de un correo electrónico con un enlace para restablecer la contraseña.
            # Para propósitos de demostración, simplemente mostraremos un mensaje.
            return jsonify({"message": f"Se ha enviado un correo de recuperación a {correo}"})
        else:
            return jsonify({"message": "Correo electrónico no encontrado"}), 404
    
    return render_template('recuperar_contraseña.html')


if __name__ == '__main__':
    app.run(debug=True) 