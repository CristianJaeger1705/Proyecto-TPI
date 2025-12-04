// Custom JS for Proyecto-TPI
document.addEventListener('DOMContentLoaded', function () {
  try {
    // Inicializar tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (el) { 
      new bootstrap.Tooltip(el); 
    });
  } catch (e) {}
});




  // -------------------------------
  // Inicializar mensajes tipo Toast
  // -------------------------------
  try {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    toastElList.forEach(function (toastEl) {
      var toast = new bootstrap.Toast(toastEl, {
        delay: 3500,
        autohide: true
      });
      toast.show();
    });
  } catch (e) {}


//Funciones para el boton de favoritos  
//Funciones para el boton de favoritos  
class FavoritosManager {
    constructor() {
        this.basePath = '/ofertas';
        this.init();
    }
    
    init() {
        // Botones favoritos
        document.querySelectorAll('.favorito-btn, .favorito-btn-detalle').forEach(btn => {
            btn.onclick = (e) => this.toggleFavorito(e);
        });
        
        // Transferir favoritos automáticamente
        this.autoTransferirFavoritos();
        
        // Actualizar UI inicial
        this.updateInitialUI();
    }
    
    async toggleFavorito(e) {
        e.preventDefault();
        const btn = e.currentTarget;
        const id = btn.dataset.id;
        
        btn.disabled = true;
        
        try {
            const csrf = this.getCsrfToken();
            const res = await fetch(`${this.basePath}/toggle/${id}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrf,
                    'Content-Type': 'application/json'
                }
            });
            
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            
            const data = await res.json();
            
            if (data.success) {
                // ACTUALIZACIÓN: Sin confirmación de login
                // Los usuarios no autenticados guardan en cookies sin interrupción
                
                // Actualizar botón clickeado
                this.updateButtonUI(btn, data.agregado);
                
                // Sincronizar todos los botones con mismo ID
                this.syncAllButtons(id, data.agregado);
                
                // Actualizar UI con el total devuelto por el servidor
                this.updateFavoritosUI(data.total);
                
            } else {
                alert('Error: ' + (data.error || 'Error al guardar favorito'));
            }
            
        } catch(err) {
            console.error('Error:', err);
            alert('Error de conexión');
        } finally {
            btn.disabled = false;
        }
    }
    
    // Actualizar UI inicial desde badge existente
    updateInitialUI() {
        // Leer el total inicial del badge existente (si hay)
        const initialBadge = document.getElementById('favoritos-badge-desktop') || 
                            document.getElementById('favoritos-badge-mobile');
        
        if (initialBadge) {
            const initialCount = parseInt(initialBadge.textContent) || 0;
            console.log('Count inicial del badge:', initialCount);
            this.updateFavoritosUI(initialCount);
        } else {
            // Fallback: contar botones activos
            const savedButtons = document.querySelectorAll('.favorito-btn.btn-warning, .favorito-btn-detalle.btn-warning');
            const count = savedButtons.length;
            this.updateFavoritosUI(count);
        }
    }
    
    // Actualizar TODA la UI (badges + bloques)
    updateFavoritosUI(count) {
        console.log('Actualizando favoritos UI con count:', count);
        
        // 1. Actualizar TODOS los badges (desktop y mobile)
        this.updateBadges(count);
        
        // 2. Mostrar/ocultar TODOS los bloques
        this.updateBlocksVisibility(count);
    }
    
    // Método específico para badges
    updateBadges(count) {
        // Buscar TODOS los badges (desktop y mobile)
        const badges = [
            document.getElementById('favoritos-badge-desktop'),
            document.getElementById('favoritos-badge-mobile')
        ].filter(badge => badge !== null);
        
        badges.forEach(badge => {
            badge.textContent = count;
            if (count > 0) {
                badge.className = 'badge bg-success rounded-pill';
                badge.style.display = 'inline-block';
            } else {
                badge.className = 'badge bg-danger rounded-pill';
                badge.style.display = 'none';
            }
            console.log('Badge actualizado:', badge.id, '->', count);
        });
    }
    
    // Método específico para bloques
    updateBlocksVisibility(count) {
        // Buscar TODOS los bloques (desktop y mobile)
        const blocks = [
            document.getElementById('favoritos-block-desktop'),
            document.getElementById('favoritos-block-mobile')
        ].filter(block => block !== null);
        
        if (blocks.length === 0) return;
        
        // Verificar si el usuario es candidato
        const isCandidato = this.checkIfUserIsCandidato();
        
        console.log('Mostrar bloques?', { count, isCandidato, blocks: blocks.length });
        
        // REGLA: Mostrar si tiene favoritos O es candidato
        blocks.forEach(block => {
            if (count > 0 || isCandidato) {
                block.style.display = 'block';
                console.log('Mostrando bloque:', block.id);
            } else {
                block.style.display = 'none';
                console.log('Ocultando bloque:', block.id);
            }
        });
    }
    
    checkIfUserIsCandidato() {
        // Buscar cualquier enlace de favoritos
        const link = document.getElementById('favoritos-link-desktop') || 
                     document.getElementById('favoritos-link-mobile');
        
        if (link) {
            const href = link.getAttribute('href');
            return href !== '#';
        }
        
        return false;
    }
    
    syncAllButtons(ofertaId, isSaved) {
        const allButtons = document.querySelectorAll(`[data-id="${ofertaId}"]`);
        
        allButtons.forEach(btn => {
            if (!btn.disabled) {
                this.updateButtonUI(btn, isSaved);
            }
        });
    }
    
    updateButtonUI(button, isSaved) {
        const icon = button.querySelector('i');
        const textSpan = button.querySelector('span');
        
        if (isSaved) {
            button.classList.replace('btn-outline-warning', 'btn-warning');
            if (icon) icon.classList.replace('bi-star', 'bi-star-fill');
            if (textSpan) textSpan.textContent = 'Guardado';
        } else {
            button.classList.replace('btn-warning', 'btn-outline-warning');
            if (icon) icon.classList.replace('bi-star-fill', 'bi-star');
            if (textSpan) textSpan.textContent = 'Guardar';
        }
    }
    
    getCsrfToken() {
        // Buscar en formularios
        const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfTokenElement) {
            return csrfTokenElement.value;
        }
        
        // Buscar en cookies
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    async autoTransferirFavoritos() {
        // ... (mantén tu código de transferencia) ...
    }
}

// Función global para click en enlace de favoritos
function handleFavoritosClick(event) {
    event.preventDefault();
    
    // Obtener el total actual del primer badge que encontremos
    const badge = document.getElementById('favoritos-badge-desktop') || 
                  document.getElementById('favoritos-badge-mobile');
    
    let count = 0;
    if (badge && badge.textContent) {
        count = parseInt(badge.textContent) || 0;
    }
    
    if (count === 0) {
        alert('No tienes favoritos guardados. Primero guarda algunas ofertas como favoritas.');
    } else {
        window.location.href = `/usuarios/login/?next=/ofertas/mis-favoritos/`;
    }
}

// Inicializar
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new FavoritosManager());
} else {
    new FavoritosManager();
}