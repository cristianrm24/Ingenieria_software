function subirPDF(proyectoId) {
    var formData = new FormData(document.getElementById('form_pdf_' + proyectoId));
    var xhr = new XMLHttpRequest();
    xhr.open('POST', document.getElementById('form_pdf_' + proyectoId).action, true);
    xhr.onload = function() {
        if (xhr.status === 200) {
            var mensaje = document.createElement('p');
            mensaje.textContent = JSON.parse(xhr.responseText).message;
            document.body.appendChild(mensaje);
            setTimeout(function() {
                mensaje.remove();
                document.getElementById('form_pdf_' + proyectoId).reset();
                window.location.reload();
            }, 3000);
        } else {
            alert("Error al subir el archivo PDF.");
        }
    };
    xhr.send(formData);
}

function editarUsuario(usuarioId) {
    document.getElementById('editar_usuario_' + usuarioId).style.display = 'table-row';
}

function cancelarEdicionUsuario(usuarioId) {
    document.getElementById('editar_usuario_' + usuarioId).style.display = 'none';
}

function guardarCambiosUsuario(usuarioId) {
    var email = document.getElementById('email_' + usuarioId).value;
    var ocupacion = document.getElementById('ocupacion_' + usuarioId).value;
    var institucion = document.getElementById('institucion_' + usuarioId).value;
    var edad = document.getElementById('edad_' + usuarioId).value;
    var nombre_completo = document.getElementById('nombre_completo_' + usuarioId).value;

    fetch("/editar_usuario/" + usuarioId, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            ocupacion: ocupacion,
            institucion: institucion,
            edad: edad,
            nombre_completo: nombre_completo
        })
    }).then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            console.error("Error al guardar cambios de usuario");
        }
    });

    return false; // Para evitar el envío del formulario
}

function editarProyecto(proyectoId) {
    document.getElementById('editar_proyecto_' + proyectoId).style.display = 'table-row';
}

function cancelarEdicionProyecto(proyectoId) {
    document.getElementById('editar_proyecto_' + proyectoId).style.display = 'none';
}

function guardarCambiosProyecto(proyectoId) {
    var titulo = document.getElementById('titulo_' + proyectoId).value;
    var descripcion = document.getElementById('descripcion_' + proyectoId).value;
    var autor = document.getElementById('autor_' + proyectoId).value;
    var fecha_publicacion = document.getElementById('fecha_publicacion_' + proyectoId).value;
    var palabras_clave = document.getElementById('palabras_clave_' + proyectoId).value;

    fetch("/editar_proyecto/" + proyectoId, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            titulo: titulo,
            descripcion: descripcion,
            autor: autor,
            fecha_publicacion: fecha_publicacion,
            palabras_clave: palabras_clave
        })
    }).then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            console.error("Error al guardar cambios de proyecto");
        }
    });

    return false; // Para evitar el envío del formulario
}

function eliminarUsuario(usuarioId) {
    if (confirm("¿Estás seguro de que quieres eliminar este usuario?")) {
        fetch("/eliminar_usuario/" + usuarioId, {
            method: "DELETE"
        }).then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                console.error("Error al eliminar usuario");
            }
        });
    }
}

function eliminarProyecto(proyectoId) {
    if (confirm("¿Estás seguro de que quieres eliminar este proyecto?")) {
        fetch("/eliminar_proyecto/" + proyectoId, {
            method: "DELETE"
        }).then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                console.error("Error al eliminar proyecto");
            }
        });
    }
}
// JavaScript para manejar el menú responsivo
const nav = document.querySelector('#nav');
const abrir = document.querySelector('#abrir');
const cerrar = document.querySelector('#cerrar');

// JavaScript para mostrar y ocultar la barra lateral
const sidebar = document.getElementById('sidebar');
const content = document.getElementById('content');

document.getElementById('abrir-menu').addEventListener('click', function() {
    sidebar.classList.toggle('open');
    content.classList.toggle('shifted');
});

document.getElementById('content').addEventListener('click', function() {
    sidebar.classList.remove('open');
    content.classList.remove('shifted');
});

abrir.addEventListener("click", () => {
    nav.classList.add('visible');
});

cerrar.addEventListener("click", () => {
    nav.classList.remove('visible');
});

function mostrarFormularioSubida(proyectoId) {
    var form = document.getElementById('form_pdf');
    form.action = "{{ url_for('admin_app.subir_pdf', proyecto_id='') }}" + proyectoId;
    document.getElementById('modal-subida').style.display = 'flex';
}

function subirPDF() {
    var form = document.getElementById('form_pdf');
    form.submit();
}

function cerrarModal() {
    document.getElementById('modal-subida').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function () {
    const abrirMenuBtn = document.getElementById('abrir-menu');
    const cerrarMenuBtn = document.getElementById('cerrar-menu');

    abrirMenuBtn.addEventListener('click', function () {
        sidebar.classList.add('visible');
        content.classList.add('shifted');
    });

    cerrarMenuBtn.addEventListener('click', function () {
        sidebar.classList.remove('visible');
        content.classList.remove('shifted');
    });
});

function mostrarFormulario(formularioId) {
    const secciones = document.querySelectorAll('main section');
    secciones.forEach(section => {
        section.style.display = 'none';
    });
    document.getElementById(formularioId).style.display = 'block';
}
