document.addEventListener('DOMContentLoaded', () => {
  // Connect to websocket
  var socket = io.connect(
    location.protocol + '//' + document.domain + ':' + location.port
  );

  socket.on('connect', () => {
    console.log('connected');
    document.querySelectorAll('button').forEach(button => {
      button.onclick = () => {
        const message = document.getElementById('message').value;
        const id = window.location.pathname.split('/').pop();
        document.getElementById('message').value = '';
        socket.emit('send message', { message: message, id: id });
        return false;
      };
    });
  });

  socket.on('message received', data => {
    console.log(data);
    var messages = document.getElementById('messages');
    var li = document.createElement('li');
    li.innerHTML = data['message'] + '- ' + data['name'];

    li.classList.add('collection-item');
    messages.appendChild(li);

    return false;
  });
});
