// =============================================================================
// VARIABLES GLOBALES
// =============================================================================
let currentModalType = null; // 'crear' o 'editar'
let currentOfertaId = null;

// =============================================================================
// GEOLOCALIZACIÓN EN MODALES
// =============================================================================
function inicializarGeolocalizacionEnModal() {
    console.log("🔄 Inicializando geolocalización en modal...");
    
    setTimeout(() => {
        if (typeof window.inicializarGeolocalizacion === 'function') {
            const success = window.inicializarGeolocalizacion();
            if (success) console.log("✅ Geolocalización inicializada en modal");
            else console.log("❌ No se pudo inicializar geolocalización en modal");
        } else {
            console.log("❌ Función de geolocalización no disponible");
        }
    }, 300);
}

function forzarGeolocalizacionEnModal() {
    console.log("🔄 Forzando geolocalización en modal...");
    
    setTimeout(() => {
        if (typeof window.forzarGeolocalizacion === 'function') {
            const success = window.forzarGeolocalizacion();
            if (success) console.log("✅ Geolocalización forzada en modal");
            else console.log("❌ No se pudo forzar geolocalización en modal");
        } else {
            console.log("❌ Función de geolocalización forzada no disponible");
        }
    }, 300);
}

// =============================================================================
// FUNCIONES PARA CREAR OFERTAS USANDO MODAL
// =============================================================================
function abrirModalCreacion() {
    console.log('Abriendo modal de creación...');
    currentModalType = 'crear';
    currentOfertaId = null;
    
    document.getElementById('crearOfertaModalBody').innerHTML = `
        <div class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
            </div>
            <p class="mt-2">Cargando formulario...</p>
        </div>
    `;
    
    const modalElement = document.getElementById('crearOfertaModal');
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
    
    modalElement.addEventListener('shown.bs.modal', () => {
        console.log('Modal de creación mostrado - configurando geolocalización');
        setTimeout(inicializarGeolocalizacionEnModal, 500);
    });

    fetch('/ofertas/obtener-formulario-creacion/')
        .then(response => {
            if (!response.ok) throw new Error('Error en la respuesta del servidor');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                document.getElementById('crearOfertaModalBody').innerHTML = data.form_html;
                console.log('Formulario de creación cargado correctamente');
                setTimeout(inicializarGeolocalizacionEnModal, 100);
            } else {
                document.getElementById('crearOfertaModalBody').innerHTML = `
                    <div class="alert alert-danger">
                        <h6>Error</h6>
                        <p>${data.error}</p>
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error('Error al cargar formulario de creación:', error);
            document.getElementById('crearOfertaModalBody').innerHTML = `
                <div class="alert alert-danger">
                    <h6>Error de conexión</h6>
                    <p>No se pudo cargar el formulario. Intente nuevamente.</p>
                </div>
            `;
        });
}

function guardarCreacion() {
    const form = document.querySelector('#form-crear-oferta');
    if (!form) return Swal.fire('Error', 'No se encontró el formulario', 'error');
    
    const formData = new FormData(form);
    const submitBtn = document.querySelector('#crearOfertaModal .btn-primary');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Creando...';
    submitBtn.disabled = true;
    
    fetch('/ofertas/guardar-creacion/', {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            bootstrap.Modal.getInstance(document.getElementById('crearOfertaModal')).hide();
            Swal.fire('¡Creado!', data.message, 'success').then(() => window.location.reload());
        } else {
            if (data.form_html) document.getElementById('crearOfertaModalBody').innerHTML = data.form_html;
            Swal.fire('Error', data.error, 'error');
        }
    })
    .catch(() => Swal.fire('Error', 'Error de conexión al crear', 'error'))
    .finally(() => {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    });
}

// =============================================================================
// FUNCIONES PARA EDITAR OFERTAS EN MODAL
// =============================================================================
function abrirModalEdicion(ofertaId) {
    console.log('Abriendo modal de edición para oferta ID:', ofertaId);
    currentModalType = 'editar';
    currentOfertaId = ofertaId;
    
    document.getElementById('editarOfertaModal').setAttribute('data-current-id', ofertaId);
    
    document.getElementById('editarOfertaModalBody').innerHTML = `
        <div class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
            </div>
            <p class="mt-2">Cargando formulario...</p>
        </div>
    `;
    
    const modalElement = document.getElementById('editarOfertaModal');
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
    
    modalElement.addEventListener('shown.bs.modal', () => {
        console.log('Modal de edición mostrado - configurando geolocalización');
        setTimeout(inicializarGeolocalizacionEnModal, 500);
    });
    
    fetch(`obtener-formulario-edicion/${ofertaId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('editarOfertaModalBody').innerHTML = data.form_html;
                document.getElementById('editarOfertaModalLabel').textContent = `Editar: ${data.titulo}`;
                console.log('Formulario de edición cargado correctamente');
                setTimeout(inicializarGeolocalizacionEnModal, 100);
            } else {
                document.getElementById('editarOfertaModalBody').innerHTML = `
                    <div class="alert alert-danger">
                        <h6>Error</h6>
                        <p>${data.error}</p>
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error('Error al cargar formulario de edición:', error);
            document.getElementById('editarOfertaModalBody').innerHTML = `
                <div class="alert alert-danger">
                    <h6>Error de conexión</h6>
                    <p>No se pudo cargar el formulario. Intente nuevamente.</p>
                </div>
            `;
        });
}

function guardarEdicion() {
    console.log('Guardando edición... ID actual:', currentOfertaId);
    const form = document.querySelector('#form-editar-oferta');
    if (!form) return Swal.fire('Error', 'No se encontró el formulario', 'error');
    
    const ofertaId = document.getElementById('editarOfertaModal')?.getAttribute('data-current-id') || currentOfertaId;
    if (!ofertaId) return Swal.fire('Error', 'No se pudo identificar la oferta', 'error');
    
    const formData = new FormData(form);
    const submitBtn = document.querySelector('#editarOfertaModal .btn-primary');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Guardando...';
    submitBtn.disabled = true;
    
    fetch(`guardar-edicion/${ofertaId}/`, {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            bootstrap.Modal.getInstance(document.getElementById('editarOfertaModal')).hide();
            Swal.fire('¡Guardado!', data.message, 'success').then(() => window.location.reload());
        } else {
            if (data.form_html) document.getElementById('editarOfertaModalBody').innerHTML = data.form_html;
            Swal.fire('Error', data.error, 'error');
        }
    })
    .catch(() => Swal.fire('Error', 'Error de conexión al guardar', 'error'))
    .finally(() => {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    });
}
