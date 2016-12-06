#!/usr/bin/env node
var WebSocketClient = require('websocket').client;
 
var client = new WebSocketClient();
 
client.on('connectFailed', function(error) {
    console.log('Connect Error: ' + error.toString());
});
 
client.on('connect', function(connection) {
    console.log('WebSocket Client Connected');
    connection.on('error', function(error) {
        console.log("Connection Error: " + error.toString());
    });
    connection.on('close', function() {
        console.log('echo-protocol Connection Closed');
    });
    connection.on('message', function(message) {
        if (message.type === 'utf8') {
            console.log("Received: '" + message.utf8Data + "'");
        }
    });
    
    function sendNumber() {
        if (connection.connected) {
            var number1 = Math.round(Math.random() * 100);
            var number2 = Math.round(Math.random()*100);
	    var speedObj = {"l":number1,"r":number2,"d":"f"};
            connection.sendUTF(JSON.stringify(speedObj));
	    console.log(JSON.stringify(speedObj));
            setTimeout(sendNumber, 100);
	
        }
    }
    sendNumber();
});
 
client.connect('ws://localhost:8080/', 'echo-protocol');
