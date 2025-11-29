document.addEventListener("DOMContentLoaded", function() {
    const chatBox = document.getElementById("chat-box");
    const formMensaje = document.getElementById("form-mensaje");
    const inputMensaje = document.getElementById("texto");

    if (!chatBox || !formMensaje || !inputMensaje) {
        console.error("No se encontró el DOM necesario para el chat.");
        return;
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie("csrftoken");

    function agregarMensaje(m) {
        const div = document.createElement("div");
        div.className = m.remitente === window.USUARIO_ACTUAL ? "mensaje-yo" : "mensaje-otro";

        // m.fecha debe ser ISO (ej: 2025-11-26T02:40:21...)
        const fecha = new Date(m.fecha);
        const hora = fecha.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

        div.innerHTML = `
            <div class="msg-text">${m.texto}</div>
            <div class="msg-time">${m.remitente} • ${hora}</div>
        `;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function cargarHistorial() {
        const url = window.CHAT_TIPO === "privado"
            ? `/mensajeria/ajax/mensajes/${window.CONVO_ID}/`
            : `/mensajeria/grupo/ajax/mensajes/${window.GRUPO_ID}/`;

        try {
            const res = await fetch(url);
            if (!res.ok) {
                console.error("Error al cargar historial:", res.status);
                return;
            }
            const data = await res.json();
            chatBox.innerHTML = "";

            if (data.mensajes && data.mensajes.length > 0) {
                data.mensajes.forEach(m => agregarMensaje(m));
            } else {
                chatBox.innerHTML = `<p class="text-muted text-center">No hay mensajes aún.</p>`;
            }
        } catch (err) {
            console.error("Error cargando historial:", err);
        }
    }

    cargarHistorial();

    formMensaje.addEventListener("submit", async function(e) {
        e.preventDefault();
        const texto = inputMensaje.value.trim();
        if (!texto) return;

        const url = window.CHAT_TIPO === "privado"
            ? `/mensajeria/ajax/enviar/${window.CONVO_ID}/`
            : `/mensajeria/grupo/ajax/enviar/${window.GRUPO_ID}/`;

        try {
            const res = await fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: `texto=${encodeURIComponent(texto)}`
            });
            const data = await res.json();
            if (data.status === "ok") {
                // agregar mensaje retornado por el servidor
                agregarMensaje({
                    texto: data.mensaje.texto,
                    remitente: data.mensaje.remitente,
                    fecha: data.mensaje.fecha
                });
            } else {
                console.error("Error enviando mensaje:", data.msg);
            }
        } catch (err) {
            console.error("Error enviando mensaje:", err);
        }

        inputMensaje.value = "";
    });

    // refrescar cada 5 segundos
    setInterval(cargarHistorial, 5000);
});
