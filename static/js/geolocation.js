//------------------------------------------IMPORTANTE----------------------------------------------
//##################################################################################################
//CODIGO GEOLOCALIZACION OPTIMIZADO Y MEJORADO, AL HACER MERGE ES NECESARIO REEMPLAZAR
//TODO EL CODIGO ANTERIOR POR ESTE NUEVO CODIGO, SI MANTIENEN AMBOS HABRA CONFLICTO
//ACTUALIZACION NO AFECTA A MAS CAMBIOS - CODIGO ANTERIOR TENIA ERRORES
//PARA MAYOR PRECISION ACTIVAR GPS DEL DISPOSITIVO MOVIL O LAPTOP
//##################################################################################################

(function() {
    'use strict';

    // Configuración
    const CONFIG = {
        campoId: 'id_ubicacion',
        timeoutGPS: 8000,
        userAgent: 'DjangoApp/1.0',
        // APIs de geolocalización por IP (se prueban en orden)
        ipAPIs: [
            'https://ipapi.co/json/',
            'https://ip-api.com/json/',
            'https://ipinfo.io/json'
        ]
    };

    /**
     * Establece la ubicación en el campo del formulario
     */
    function setUbicacion(texto, metodo = 'desconocido') {
        const campo = document.getElementById(CONFIG.campoId);
        
        if (!campo) {
            console.error(`Campo ${CONFIG.campoId} no encontrado`);
            return false;
        }

        campo.value = texto;
       // console.log(`Ubicación establecida: "${texto}" (método: ${metodo})`);
        
        // Disparar evento personalizado
        const event = new CustomEvent('ubicacionEstablecida', { 
            detail: { 
                ubicacion: texto,
                metodo: metodo,
                timestamp: new Date().toISOString()
            } 
        });
        document.dispatchEvent(event);
        
        return true;
    }

    /**
     * Obtiene ubicación por IP usando múltiples APIs como fallback
     */
    async function obtenerPorIP() {

        for (const apiUrl of CONFIG.ipAPIs) {
            try {
         //       console.log(`   Probando: ${apiUrl}`);
                const resp = await fetch(apiUrl, { 
                    signal: AbortSignal.timeout(5000) // Timeout de 5 segundos
                });

                if (!resp.ok) {
                    console.warn(`Respuesta no OK: ${resp.status}`);
                    continue;
                }

                const data = await resp.json();
                
                // Extraer ciudad según el formato de cada API
                let ciudad = null;
                
                if (data.city) {
                    ciudad = data.city; // ipapi.co, ip-api.com
                } else if (data.city_name) {
                    ciudad = data.city_name; // ipinfo.io a veces usa esto
                } else if (data.region) {
                    ciudad = data.region; // Fallback a región
                }

                if (ciudad) {
                    //console.log(`Ciudad obtenida: ${ciudad}`);
                    setUbicacion(ciudad, 'IP');
                    return true;
                }

            } catch (error) {
                console.warn(`Error con ${apiUrl}:`, error.message);
                continue; // Intentar con la siguiente API
            }
        }

        // Si todas las APIs fallaron
        console.error('Todas las APIs de IP fallaron');
        setUbicacion('Ubicación no disponible', 'fallback');
        return false;
    }

    /**
     * Obtiene ciudad desde coordenadas GPS usando Nominatim
     */
    async function obtenerCiudadDesdeGPS(lat, lon) {
        try {
            const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`;
           // console.log(`   Consultando Nominatim: ${url}`);

            const resp = await fetch(url, {
                headers: {
                    'User-Agent': CONFIG.userAgent
                },
                signal: AbortSignal.timeout(5000)
            });

            if (!resp.ok) {
                throw new Error(`HTTP ${resp.status}`);
            }

            const data = await resp.json();
            //console.log('   Datos de Nominatim:', data);

            // Buscar ciudad en orden de prioridad
            const ciudad = 
                data.address?.city ||
                data.address?.town ||
                data.address?.village ||
                data.address?.municipality ||
                data.address?.county ||
                null;

            if (ciudad) {
              //  console.log(`Ciudad encontrada: ${ciudad}`);
                setUbicacion(ciudad, 'GPS');
                return true;
            } else {
                console.warn('No se encontró ciudad en los datos');
                return false;
            }

        } catch (error) {
            console.error('Error consultando Nominatim:', error.message);
            return false;
        }
    }

    /**
     * Obtiene ubicación por GPS del navegador
     */
    async function obtenerPorGPS() {
        return new Promise((resolve, reject) => {
            if (!navigator.geolocation) {
                console.warn('⚠️ Geolocalización no soportada por el navegador');
                reject(new Error('Geolocalización no soportada'));
                return;
            }

           // console.log('📍 Solicitando permiso de GPS...');

            navigator.geolocation.getCurrentPosition(
                async function(pos) {
                    const { latitude: lat, longitude: lon } = pos.coords;

                    const exito = await obtenerCiudadDesdeGPS(lat, lon);
                    
                    if (exito) {
                        resolve(true);
                    } else {
                        reject(new Error('No se pudo obtener ciudad desde GPS'));
                    }
                },
                function(error) {
                    const mensajes = {
                        1: 'Usuario denegó el permiso de ubicación',
                        2: 'Ubicación no disponible',
                        3: 'Timeout esperando GPS'
                    };
                    
                    const mensaje = mensajes[error.code] || `Error desconocido (${error.code})`;
                    console.error(` Error GPS: ${mensaje}`);
                    reject(new Error(mensaje));
                },
                {
                    enableHighAccuracy: true,
                    timeout: CONFIG.timeoutGPS,
                    maximumAge: 0
                }
            );
        });
    }

    /**
     * Función principal: Intenta GPS, luego IP
     */
    async function obtenerUbicacion(forzar = false) {
        const campo = document.getElementById(CONFIG.campoId);
        
        if (!campo) {
            console.warn(`⚠️ Campo ${CONFIG.campoId} no existe en el DOM`);
            return false;
        }

        // Si ya tiene valor y no se fuerza, no hacer nada
        if (!forzar && campo.value && campo.value.trim() !== '') {
            return true;
        }

        //console.log('─'.repeat(50));

        try {
            // Intentar GPS primero
            await obtenerPorGPS();
          //  console.log('─'.repeat(50));
            return true;

        } catch (errorGPS) {
            //console.log('─'.repeat(50));
            console.warn('⚠️ GPS no disponible, usando IP como fallback...');
            //console.log('─'.repeat(50));

            // Fallback a IP
            const exitoIP = await obtenerPorIP();
            //console.log('─'.repeat(50));
            
            if (exitoIP) {
                return true;
            } else {
                return false;
            }
        }
    }

    /**
     * Inicializa geolocalización (solo si el campo está vacío)
     */
    function inicializarGeolocalizacion() {
        return obtenerUbicacion(false);
    }

    /**
     * Fuerza geolocalización (ignora valor actual)
     */
    function forzarGeolocalizacion() {
        return obtenerUbicacion(true);
    }

    // Ejecutar automáticamente al cargar la página
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(() => inicializarGeolocalizacion(), 100); // Pequeño delay para asegurar que el campo existe
        });
    } else {
        // Si el DOM ya está cargado
        setTimeout(() => inicializarGeolocalizacion(), 100);
    }

    // Exponer funciones globalmente
    window.inicializarGeolocalizacion = inicializarGeolocalizacion;
    window.forzarGeolocalizacion = forzarGeolocalizacion;
})();