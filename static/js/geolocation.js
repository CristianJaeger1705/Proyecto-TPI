document.addEventListener("DOMContentLoaded", async function () {

    const campo = document.getElementById("id_ubicacion");
    if (!campo) {
        console.warn("⚠ Campo id_ubicacion no existe en esta página.");
        return;
    }

    console.log("✔ Campo ubicación listo:", campo);

    // --- FUNCIÓN PARA RELLENAR UBICACIÓN ---
    function setUbicacion(texto) {
        campo.value = texto;
        console.log("📍 Ubicación establecida:", texto);
    }

    // --- FALLBACK SI FALLA EL GPS ---
    async function obtenerPorIP() {
        try {
            console.warn("🟡 Intentando obtener ciudad desde IP…");
            const resp = await fetch("https://ipapi.co/json/");
            const data = await resp.json();

            if (data && data.city) {
                setUbicacion(data.city);
            } else {
                setUbicacion("Ubicación no disponible");
            }
        } catch (e) {
            console.error("❌ Error usando fallback por IP:", e);
            setUbicacion("Ubicación no disponible");
        }
    }

    // --- INTENTO PRINCIPAL: GPS DEL NAVEGADOR ---
    if (navigator.geolocation) {

        navigator.geolocation.getCurrentPosition(
            async function (pos) {
                console.log("✔ GPS Obtenido:", pos);

                const lat = pos.coords.latitude;
                const lon = pos.coords.longitude;

                try {
                    const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`;

                    console.log("🔎 Consultando ciudad:", url);

                    const resp = await fetch(url, {
                        headers: {
                            "User-Agent": "DjangoApp/1.0"
                        }
                    });

                    const data = await resp.json();
                    console.log("📦 Datos Nominatim:", data);

                    const ciudad =
                        data.address.city ||
                        data.address.town ||
                        data.address.village ||
                        data.address.county ||
                        null;

                    if (ciudad) {
                        setUbicacion(ciudad);
                    } else {
                        console.warn("⚠ No se encontró ciudad. Usando IP...");
                        obtenerPorIP();
                    }

                } catch (err) {
                    console.error("❌ Error obteniendo ciudad por GPS:", err);
                    obtenerPorIP();
                }
            },

            function (error) {
                console.error("❌ Error al obtener GPS:", error);

                if (error.code === 1) {
                    console.warn("🔒 El usuario denegó la ubicación. Usando IP.");
                }

                obtenerPorIP();
            },

            {
                enableHighAccuracy: true,
                timeout: 8000,
                maximumAge: 0
            }
        );

    } else {
        console.warn("Geolocalización no soportada. Usando IP.");
        obtenerPorIP();
    }
});
