

var WebSocketServer = require('ws').Server;

var wss1 = new WebSocketServer({host:'0.0.0.0', port: 8080 });
var wss2 = new WebSocketServer({host:'0.0.0.0', port: 8081 });

var connection2;
 
wss1.on('connection', function connection(ws1) {
  ws1.on('message', function incoming(message) {
    console.log('received: %s', message);
    console.log('connection2 is '+connection2);
    if(connection2){
	connection2.send(message);
	}
  });
  ws1.on('close', function(reasonCode, description) {
        console.log((new Date()) + ' Peer ' + ws1.remoteAddress + ' disconnected');
    });


});

wss2.on('connection', function connection(ws2) {
  connection2=ws2;
  ws2.on('close', function(reasonCode, description) {
        console.log((new Date()) + ' Peer ' + connection2.remoteAddress + ' disconnected');
	connection2=0;
    });

});

