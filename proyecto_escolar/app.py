# Importar los módulos necesarios
from flask import Flask, render_template, request, redirect, url_for, Blueprint
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
            return redirect(url_for('admin_app.admin_index'))  # Redirect to admin index through blueprint
        
        # Si no coincide, verificar en la base de datos Firebase
        usuario_en_db = firebase.get('/Usuarios', email)
        if usuario_en_db and usuario_en_db.get('contraseña') == contraseña:
            # Redirigir a la página de usuario normal (aquí deberías definir la ruta correspondiente)
            return redirect(url_for('pagina_normal'))

    return render_template('login.html')

# Ruta para la página de administrador
@admin_app.route('/admin_index')
def admin_index():
    return render_template('admin_index.html')

# Función para la página de lista de usuarios
@app.route('/lista_usuarios')
def lista_usuarios():
    usuarios = obtener_usuarios()  # Obtener la lista de usuarios desde Firebase
    return render_template('lista_usuarios.html', usuarios=usuarios)

# Función para la página de lista de proyectos
@app.route('/lista_proyectos')
def lista_proyectos():
    proyectos = obtener_proyectos()  # Obtener la lista de proyectos desde Firebase
    return render_template('lista_proyectos.html', proyectos=proyectos)

# Ruta para crear un nuevo usuario
@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    # Obtener los datos del formulario
    nombre_usuario = request.form['nombre_usuario']
    contraseña = request.form['contraseña']
    correo = request.form['correo']
    rol = request.form['rol']

    # Guardar los datos en la base de datos Firebase
    datos_usuario = {
        'nombre_usuario': nombre_usuario,
        'contraseña': contraseña,
        'correo': correo,
        'rol': rol
    }
    firebase.post('/Usuarios', datos_usuario)
    
    # Redirigir a la página de lista de usuarios después de la creación exitosa
    return redirect(url_for('lista_usuarios'))

# Ruta para eliminar un usuario
@app.route('/eliminar_usuario/<usuario_id>', methods=['GET', 'POST'])
def eliminar_usuario(usuario_id):
    # Eliminar el usuario de la base de datos Firebase
    firebase.delete('/Usuarios', usuario_id)

    # Redirigir a la página de lista de usuarios después de la eliminación exitosa
    return redirect(url_for('lista_usuarios'))

# Ruta para editar un usuario
@app.route('/editar_usuario/<usuario_id>', methods=['GET', 'POST'])
def editar_usuario(usuario_id):
    if request.method == 'POST':
        # Obtener los datos actualizados del formulario
        nombre_usuario = request.form['nombre_usuario']
        contraseña = request.form['contraseña']
        correo = request.form['correo']
        rol = request.form['rol']

        # Actualizar los datos en la base de datos Firebase
        datos_actualizados = {
            'nombre_usuario': nombre_usuario,
            'contraseña': contraseña,
            'correo': correo,
            'rol': rol
        }
        firebase.put('/Usuarios', usuario_id, datos_actualizados)
        
        # Redirigir a la página de lista de usuarios después de la actualización exitosa
        return redirect(url_for('lista_usuarios'))

    # Obtener los datos del usuario a editar desde Firebase
    usuario = firebase.get('/Usuarios', usuario_id)
    return render_template('editar_usuario.html', usuario=usuario)

# Ruta para crear un nuevo proyecto
@app.route('/crear_proyecto', methods=['POST'])
def crear_proyecto():
    # Obtener los datos del formulario
    titulo = request.form['titulo']
    autor = request.form['autor']
    descripcion = request.form['descripcion']
    palabras_clave = request.form['palabras_clave']
    fecha_publicacion = request.form['fecha_publicacion']

    # Guardar los datos en la base de datos Firebase
    datos_proyecto = {
        'titulo': titulo,
        'autor': autor,
        'descripcion': descripcion,
        'palabras_clave': palabras_clave,
        'fecha_publicacion': fecha_publicacion
    }
    firebase.post('/Proyectos', datos_proyecto)
    
    # Redirigir a la página de lista de proyectos después de la creación exitosa
    return redirect(url_for('lista_proyectos'))

# Ruta para eliminar un proyecto
@app.route('/eliminar_proyecto/<proyecto_id>', methods=['GET', 'POST'])
def eliminar_proyecto(proyecto_id):
    # Eliminar el proyecto de la base de datos Firebase
    firebase.delete('/Proyectos', proyecto_id)

    # Redirigir a la página de lista de proyectos después de la eliminación exitosa
    return redirect(url_for('lista_proyectos'))

# Ruta para editar un proyecto
@app.route('/editar_proyecto/<proyecto_id>', methods=['GET', 'POST'])
def editar_proyecto(proyecto_id):
    if request.method == 'POST':
        # Obtener los datos actualizados del formulario
        titulo = request.form['titulo']
        autor = request.form['autor']
        descripcion = request.form['descripcion']
        palabras_clave = request.form['palabras_clave']
        fecha_publicacion = request.form['fecha_publicacion']

        # Actualizar los datos en la base de datos Firebase
        datos_actualizados = {
            'titulo': titulo,
            'autor': autor,
            'descripcion': descripcion,
            'palabras_clave': palabras_clave,
            'fecha_publicacion': fecha_publicacion
        }
        firebase.put('/Proyectos', proyecto_id, datos_actualizados)
        
        # Redirigir a la página de lista de proyectos después de la actualización exitosa
        return redirect(url_for('lista_proyectos'))

    # Obtener los datos del proyecto a editar desde Firebase
    proyecto = firebase.get('/Proyectos', proyecto_id)
    return render_template('editar_proyecto.html', proyecto=proyecto)

# Register blueprint for admin section
app.register_blueprint(admin_app)

if __name__ == '__main__':
    app.run(debug=True)
