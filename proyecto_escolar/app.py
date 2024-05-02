from flask import Flask, render_template, request, redirect, url_for, Blueprint, jsonify
from firebase import firebase

#app = Flask(__name__, template_folder='logeo/templates')
app = Flask(__name__, template_folder='logeo/templates', static_folder='static')


admin_app = Blueprint('admin_app', __name__, template_folder='admin/templates')
firebase = firebase.FirebaseApplication("https://base-20e8f-default-rtdb.firebaseio.com/", None)

# Funciones de ayuda para obtener usuarios y proyectos
def obtener_usuarios():
    usuarios = firebase.get('/Usuarios', None)
    if usuarios:
        return [{**usuario, 'id': usuario_id} for usuario_id, usuario in usuarios.items()]
    else:
        return []

def obtener_proyectos():
    proyectos = firebase.get('/Proyectos', None)
    if proyectos:
        return [{**proyecto, 'id': proyecto_id} for proyecto_id, proyecto in proyectos.items()]
    else:
        return []

# Rutas para administrar usuarios
@admin_app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    if request.method == 'POST':
        # Obtener datos del formulario
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
        # Obtener datos del formulario
        email = request.json.get('email', usuario.get('email'))
        ocupacion = request.json.get('ocupacion', usuario.get('ocupacion'))
        institucion = request.json.get('institucion', usuario.get('institucion'))
        edad = request.json.get('edad', usuario.get('edad'))
        nombre_completo = request.json.get('nombre_completo', usuario.get('nombre_completo'))
        
        # Actualizar solo los campos que no son vacíos
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
        
        # Verificar si hay al menos un campo no vacío para actualizar
        if datos_usuario:
            # Actualizar datos en la base de datos Firebase
            firebase.put('/Usuarios', usuario_id, datos_usuario)
            return jsonify({"message": "Usuario actualizado correctamente"})
    
    return jsonify({"message": "Error al actualizar usuario"})

# Rutas para administrar proyectos
@admin_app.route('/proyectos', methods=['GET', 'POST'])
def proyectos():
    if request.method == 'POST':
        # Obtener datos del formulario
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
        # Obtener datos del formulario
        titulo = request.json.get('titulo', proyecto.get('titulo'))
        descripcion = request.json.get('descripcion', proyecto.get('descripcion'))
        autor = request.json.get('autor', proyecto.get('autor'))
        fecha_publicacion = request.json.get('fecha_publicacion', proyecto.get('fecha_publicacion'))
        palabras_clave = request.json.get('palabras_clave', proyecto.get('palabras_clave'))
        
        # Actualizar solo los campos que no son vacíos
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
        
        # Verificar si hay al menos un campo no vacío para actualizar
        if datos_proyecto:
            # Actualizar datos en la base de datos Firebase
            firebase.put('/Proyectos', proyecto_id, datos_proyecto)
            return jsonify({"message": "Proyecto actualizado correctamente"})
    
    return jsonify({"message": "Error al actualizar proyecto"})

@admin_app.route('/eliminar_usuario/<string:usuario_id>', methods=['DELETE'])
def eliminar_usuario(usuario_id):
    firebase.delete('/Usuarios', usuario_id)
    return jsonify({"message": "Usuario eliminado correctamente"})

@admin_app.route('/eliminar_proyecto/<string:proyecto_id>', methods=['DELETE'])
def eliminar_proyecto(proyecto_id):
    firebase.delete('/Proyectos', proyecto_id)
    return jsonify({"message": "Proyecto eliminado correctamente"})


# Registrar el Blueprint en la aplicación Flask
app.register_blueprint(admin_app)

# Ruta para el registro de usuarios
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Obtener los datos del formulario
        email = request.form['email']
        contraseña = request.form['contraseña']
        
        if email and contraseña:
            # Guardar los datos en la base de datos Firebase
            datos_usuario = {
                'email': email,
                'contraseña': contraseña
            }
            firebase.post('/Usuarios', datos_usuario)
            
            return redirect(url_for('login'))
    
    return render_template('registro.html')

# Ruta para el login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        
        if email == 'admin@gmail.com' and contraseña == '123':
            return redirect(url_for('admin_app.usuarios'))
        
        usuario_en_db = firebase.get('/Usuarios', email)
        if usuario_en_db and usuario_en_db.get('contraseña') == contraseña:
            return redirect(url_for('pagina_normal'))

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
