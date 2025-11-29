(function() {
    'use strict';

    const CONFIG = {
        campoId: 'id_ubicacion',
        timeoutGPS: 8000,
        userAgent: 'DjangoApp/1.0',
        ipAPIs: [
            'https://ipapi.co/json/',
            'https://ip-api.com/json/',
            'https://ipinfo.io/json'
        ]
    };

    function setUbicacion(texto, metodo = 'desconocido') {
        const campo = document.getElementById(CONFIG.campoId);
        if (!campo) return false;
        campo.value = texto;
        const event = new CustomEvent('ubicacionEstablecida', { detail: { ubicacion: texto, metodo, timestamp: new Date().toISOString() }});
        document.dispatchEvent(event);
        return true;
    }

    async function obtenerPorIP() {
        for (const apiUrl of CONFIG.ipAPIs) {
            try {
                const resp = await fetch(apiUrl, { signal: AbortSignal.timeout(5000) });
                if (!resp.ok) continue;
                const data = await resp.json();
                const ciudad = data.city || data.city_name || data.region;
                if (ciudad) return setUbicacion(ciudad, 'IP');
            } catch(e) { continue; }
        }
        return setUbicacion('Ubicación no disponible', 'fallback');
    }

    async function obtenerCiudadDesdeGPS(lat, lon) {
        try {
            const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`;
            const resp = await fetch(url, { headers: {'User-Agent': CONFIG.userAgent}, signal: AbortSignal.timeout(5000) });
            if (!resp.ok) throw new Error();
            const data = await resp.json();
            const ciudad = data.address?.city || data.address?.town || data.address?.village || data.address?.municipality || data.address?.county;
            if (ciudad) return setUbicacion(ciudad, 'GPS');
            return false;
        } catch(e) {
            return false;
        }
    }

    async function obtenerPorGPS() {
        return new Promise((resolve, reject) => {
            if (!navigator.geolocation) return reject(new Error('Geolocalización no soportada'));
            navigator.geolocation.getCurrentPosition(
                async pos => {
                    const { latitude: lat, longitude: lon } = pos.coords;
                    const exito = await obtenerCiudadDesdeGPS(lat, lon);
                    exito ? resolve(true) : reject(new Error('No se pudo obtener ciudad desde GPS'));
                },
                err => reject(new Error(err.message)),
                { enableHighAccuracy: true, timeout: CONFIG.timeoutGPS, maximumAge: 0 }
            );
        });
    }

    async function obtenerUbicacion(forzar = false) {
        const campo = document.getElementById(CONFIG.campoId);
        if (!campo) return false;
        if (!forzar && campo.value.trim() !== '') return true;
        try { await obtenerPorGPS(); return true; } 
        catch(e) { return await obtenerPorIP(); }
    }

    function inicializarGeolocalizacion() { return obtenerUbicacion(false); }
    function forzarGeolocalizacion() { return obtenerUbicacion(true); }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => setTimeout(inicializarGeolocalizacion, 100));
    } else {
        setTimeout(inicializarGeolocalizacion, 100);
    }

    window.inicializarGeolocalizacion = inicializarGeolocalizacion;
    window.forzarGeolocalizacion = forzarGeolocalizacion;
})();
