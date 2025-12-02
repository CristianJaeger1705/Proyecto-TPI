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


// static/js/favoritos.js - VERSIÓN CON AMARILLO Y ESTRELLA
// static/js/favoritos.js - VERSIÓN COMPLETA
// static/js/favoritos.js - VERSIÓN CON SINCRONIZACIÓN
class FavoritosManager {
    constructor() {
        this.basePath = '/ofertas';
        this.init();
    }
    
    init() {
        // Botones normales (lista)
        document.querySelectorAll('.favorito-btn').forEach(btn => {
            btn.onclick = (e) => this.toggleFavorito(e);
        });
        
        // Botones en detalle
        document.querySelectorAll('.favorito-btn-detalle').forEach(btn => {
            btn.onclick = (e) => this.toggleFavorito(e);
        });
        
        // Enlace de favoritos
        const favoritosLink = document.getElementById('favoritos-link');
        if (favoritosLink && favoritosLink.getAttribute('href') === '#') {
            favoritosLink.onclick = (e) => this.handleFavoritosLink(e);
        }
        
        this.updateCounterFromButtons();
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
                // 1. Actualizar el botón clickeado
                this.updateButtonUI(btn, data.agregado);
                
                // 2. Actualizar TODOS los botones con el mismo data-id (sincronización)
                this.syncAllButtons(id, data.agregado);
                
                // 3. Actualizar contador
                this.updateFavoritosCount(data.total);
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
    
    syncAllButtons(ofertaId, isSaved) {
        // Encontrar TODOS los botones con este ID (en lista y detalle)
        const allButtons = document.querySelectorAll(`[data-id="${ofertaId}"]`);
        
        allButtons.forEach(btn => {
            // Solo actualizar si no es el botón que ya actualizamos
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
    
    updateCounterFromButtons() {
        const savedButtons = document.querySelectorAll('.favorito-btn.btn-warning, .favorito-btn-detalle.btn-warning');
        const count = savedButtons.length;
        this.updateFavoritosCount(count);
    }
    
    updateFavoritosCount(count) {
        const badge = document.getElementById('favoritos-badge');
        if (badge) {
            badge.textContent = count;
            badge.style.display = count > 0 ? 'inline-block' : 'none';
        }
        
        const sidebarBlock = document.getElementById('favoritos-sidebar-block');
        if (sidebarBlock) {
            sidebarBlock.style.display = count > 0 ? 'block' : 'none';
        }
    }
    
    handleFavoritosLink(e) {
        e.preventDefault();
        
        const badge = document.getElementById('favoritos-badge');
        const count = badge ? parseInt(badge.textContent) : 0;
        
        if (count === 0) {
            alert('No tienes favoritos guardados');
            return;
        }
        
        window.location.href = `/usuarios/login/?next=${this.basePath}/mis-favoritos/`;
    }
    
    getCsrfToken() {
        const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfInput && csrfInput.value) return csrfInput.value;
        
        const metaTag = document.querySelector('meta[name="csrfmiddlewaretoken"]');
        if (metaTag && metaTag.content) return metaTag.content;
        
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith('csrftoken=')) {
                return cookie.substring('csrftoken='.length);
            }
        }
        
        return '';
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new FavoritosManager());
} else {
    new FavoritosManager();
}