// JavaScript para manejar el menú responsivo
const nav= document.querySelector('#nav');
const abrir = document.querySelector('#abrir');
const cerrar = document.querySelector('#cerrar');
// JavaScript para mostrar y ocultar la barra lateral
document.getElementById('abrir-menu').addEventListener('click', function() {
    document.getElementById('sidebar').classList.toggle('open');
});

document.getElementById('content').addEventListener('click', function() {
    document.getElementById('sidebar').classList.remove('open');
});
abrir.addEventListener("click", () => {
    nav.classList.add('visible');
})

cerrar.addEventListener("click", () => {
    nav.classList.remove('visible');
})

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


