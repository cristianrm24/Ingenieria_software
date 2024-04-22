# Importar los módulos necesarios
from flask import Flask, render_template, request, redirect, url_for, Blueprint, jsonify
from firebase import firebase

# Inicializar la aplicación Flask
app = Flask(__name__, template_folder='logeo/templates')
admin_app = Blueprint('admin_app', __name__, template_folder='admin/templates')  # Blueprint for admin section

# Configurar la conexión con Firebase
firebase = firebase.FirebaseApplication("https://base-20e8f-default-rtdb.firebaseio.com/", None)

# Función para obtener la lista de usuarios desde Firebase
def obtener_usuarios():
    usuarios = firebase.get('/Usuarios', None)
    if usuarios:
        return [usuario for usuario_id, usuario in usuarios.items()]
    else:
        return []

# Función para obtener la lista de proyectos desde Firebase
def obtener_proyectos():
    proyectos = firebase.get('/Proyectos', None)
    if proyectos:
        return [proyecto for proyecto_id, proyecto in proyectos.items()]
    else:
        return []

# Ruta para el CRUD de usuarios en admin_index.html
@admin_app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    if request.method == 'POST':
        # Obtener los datos del formulario
        email = request.form['email']
        contraseña = request.form['contraseña']
        ocupacion = request.form['ocupacion']
        institucion = request.form['institucion']
        edad = request.form['edad']
        nombre_completo = request.form['nombre_completo']
        
        # Verificar que los datos del formulario no estén vacíos
        if email and contraseña and ocupacion and institucion and edad and nombre_completo:
            # Guardar los datos en la base de datos Firebase
            datos_usuario = {
                'email': email,
                'contraseña': contraseña,
                'ocupacion': ocupacion,
                'institucion': institucion,
                'edad': edad,
                'nombre_completo': nombre_completo
            }
            firebase.post('/Usuarios', datos_usuario)
            
            # Redirigir al usuario a la misma página después de la inserción exitosa
            return redirect(url_for('admin_app.usuarios'))
    
    # Obtener la lista de todos los usuarios existentes
    lista_usuarios = obtener_usuarios()
    
    # Obtener la lista de todos los proyectos existentes
    lista_proyectos = obtener_proyectos()
    
    # Renderizar el formulario de inserción y las listas de usuarios y proyectos
    return render_template('admin_index.html', usuarios=lista_usuarios, proyectos=lista_proyectos)


# Ruta para el CRUD de proyectos en admin_index.html
@admin_app.route('/proyectos', methods=['GET', 'POST'])
def proyectos():
    if request.method == 'POST':
        # Obtener los datos del formulario
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        autor = request.form['autor']
        fecha_publicacion = request.form['fecha_publicacion']
        palabras_clave = request.form['palabras_clave']
        
        # Verificar que los datos del formulario no estén vacíos
        if titulo and descripcion and autor and fecha_publicacion and palabras_clave:
            # Guardar los datos en la base de datos Firebase
            datos_proyecto = {
                'titulo': titulo,
                'descripcion': descripcion,
                'autor': autor,
                'fecha_publicacion': fecha_publicacion,
                'palabras_clave': palabras_clave
            }
            firebase.post('/Proyectos', datos_proyecto)
            
            # Redirigir al usuario a la misma página después de la inserción exitosa
            return redirect(url_for('admin_app.proyectos'))
    
    # Obtener la lista de todos los proyectos existentes
    lista_proyectos = obtener_proyectos()
    
    # Obtener la lista de todos los usuarios existentes
    lista_usuarios = obtener_usuarios()
    
    # Renderizar el formulario de inserción y las listas de usuarios y proyectos
    return render_template('admin_index.html', proyectos=lista_proyectos, usuarios=lista_usuarios)


# Rutas para editar y eliminar usuarios
@admin_app.route('/usuarios/editar/<usuario_id>', methods=['POST'])
def editar_usuario(usuario_id):
    if request.method == 'POST':
        # Obtener datos del formulario
        email = request.form['email']
        contraseña = request.form['contraseña']
        ocupacion = request.form['ocupacion']
        institucion = request.form['institucion']
        edad = request.form['edad']
        nombre_completo = request.form['nombre_completo']
        
        # Actualizar los datos en la base de datos Firebase
        firebase.put('/Usuarios', usuario_id, {
            'email': email,
            'contraseña': contraseña,
            'ocupacion': ocupacion,
            'institucion': institucion,
            'edad': edad,
            'nombre_completo': nombre_completo
        })
        
        # Redirigir al usuario después de la actualización exitosa
        return redirect(url_for('admin_app.usuarios'))

    # Lógica para obtener datos del usuario a editar y renderizar formulario de edición
    usuario = firebase.get('/Usuarios', usuario_id)
    return render_template('editar_usuario.html', usuario=usuario)


@admin_app.route('/usuarios/eliminar/<usuario_id>', methods=['POST'])
def eliminar_usuario(usuario_id):
    # Eliminar usuario de la base de datos Firebase
    firebase.delete('/Usuarios', usuario_id)
    return jsonify({'message': 'El usuario ha sido eliminado correctamente'})


# Rutas para editar y eliminar proyectos
@admin_app.route('/proyectos/editar/<proyecto_id>', methods=['POST'])
def editar_proyecto(proyecto_id):
    if request.method == 'POST':
        # Obtener datos del formulario
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        autor = request.form['autor']
        fecha_publicacion = request.form['fecha_publicacion']
        palabras_clave = request.form['palabras_clave']
        
        # Actualizar los datos en la base de datos Firebase
        firebase.put('/Proyectos', proyecto_id, {
            'titulo': titulo,
            'descripcion': descripcion,
            'autor': autor,
            'fecha_publicacion': fecha_publicacion,
            'palabras_clave': palabras_clave
        })
        
        # Redirigir al usuario después de la actualización exitosa
        return redirect(url_for('admin_app.proyectos'))

@admin_app.route('/proyectos/eliminar/<proyecto_id>', methods=['POST'])
def eliminar_proyecto(proyecto_id):
    # Eliminar proyecto de la base de datos Firebase
    firebase.delete('/Proyectos', proyecto_id)
    return redirect(url_for('admin_app.proyectos'))


# Registrar el Blueprint en la aplicación Flask
app.register_blueprint(admin_app)

# Ruta para el registro de usuarios
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Obtener los datos del formulario
        email = request.form['email']
        contraseña = request.form['contraseña']
        
        # Verificar que los datos cumplen con los requisitos (puedes agregar validaciones aquí)
        if email and contraseña:
            # Guardar los datos en la base de datos Firebase
            datos_usuario = {
                'email': email,
                'contraseña': contraseña
            }
            firebase.post('/Usuarios', datos_usuario)
            
            # Redirigir al usuario al login después del registro exitoso
            return redirect(url_for('login'))
    
    # Renderizar el formulario de registro si la solicitud es GET o si hay errores en la solicitud POST
    return render_template('registro.html')

# Ruta para el login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        
        # Verificar si las credenciales coinciden con el usuario administrador
        if email == 'admin@gmail.com' and contraseña == '123':
            # Si coincide, redirigir a la página de administrador
            return redirect(url_for('admin_app.usuarios'))  # Redirect to admin users through blueprint
        
        # Si no coincide, verificar en la base de datos Firebase
        usuario_en_db = firebase.get('/Usuarios', email)
        if usuario_en_db and usuario_en_db.get('contraseña') == contraseña:
            # Redirigir a la página de usuario normal (aquí deberías definir la ruta correspondiente)
            return redirect(url_for('pagina_normal'))

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
