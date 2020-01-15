document.addEventListener('DOMContentLoaded', () => {
  // Connect to websocket
  var socket = io.connect(
    location.protocol + '//' + document.domain + ':' + location.port
  );

  socket.on('connect', () => {
    document.querySelectorAll('button').forEach(button => {
      button.onclick = () => {
        const name = document.getElementById('channel_name').value;
        document.getElementById('channel_name').value = '';
        socket.emit('create channel', { name: name });
        return false;
      };
    });
  });

  socket.on('channel created', data => {
    console.log(data);
    var channels = document.getElementById('channels');
    var li = document.createElement('li');
    var link = document.createElement('a');
    link.innerHTML = data['name'];
    link.setAttribute('href', 'channel/' + data['id']);
    li.appendChild(link);
    li.classList.add('collection-item');
    channels.appendChild(li);

    return false;
  });
});
