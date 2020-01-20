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
    var m = document.createElement('li');
    var name = document.createElement('li');

    name.innerHTML = data['name'];
    m.innerHTML = data['message'];
    m.classList.add('message');

    messages.appendChild(name);
    messages.appendChild(m);
    return false;
  });
});
