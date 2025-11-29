const chatSocket = new WebSocket(
  'ws://' + window.location.host + '/ws/mensajeria/' + roomName + '/'
);

chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  const log = document.querySelector('#chat-log');
  log.innerHTML += `<p><b>${data.remitente}:</b> ${data.mensaje}</p>`;
  log.scrollTop = log.scrollHeight;
};

chatSocket.onclose = function (e) {
  console.error('Socket cerrado inesperadamente');
};

document.querySelector('#chat-message-submit').onclick = function () {
  const input = document.querySelector('#chat-message-input');
  const message = input.value.trim();

  if (message) {
    chatSocket.send(JSON.stringify({
      mensaje: message,
      conversacion_id: roomName,
      destinatario: otroUsuarioUsername
    }));

    input.value = '';
  }
};
