
```javascript
var protocol_one = document.location.protocol == 'http:' ? 'ws' : 'wss',
    port = document.location.port,
    url_one = protocol_one + "://" + document.location.hostname + (port ? ":" + port : "") + "/ws",
    socket = window['MozWebSocket'] ? new MozWebSocket(url_one) : new WebSocket(url_one);

socket.onopen = function() {this.send('open-{user_id}')};

socket.onmessage = function(e) {
    console.log(e.data);
};
```
