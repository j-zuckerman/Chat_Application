document.addEventListener('DOMContentLoaded', () => {
  // Connect to websocket
  var socket = io.connect(
    location.protocol + '//' + document.domain + ':' + location.port
  );

  socket.on('connect', () => {
    document.querySelectorAll('button').forEach(button => {
      button.onclick = () => {
        const name = document.getElementById('channelName').value;
        document.getElementById('channelName').value = '';
        socket.emit('create channel', { id: 0, name: name });
        return false;
      };
    });
  });
});
