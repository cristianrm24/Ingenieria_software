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
