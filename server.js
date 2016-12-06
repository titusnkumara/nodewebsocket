#!/usr/bin/env node
var WebSocketServer = require('websocket').server;
var http = require('http');

var connection1;
var connection2;

var currentDataString = "";
 
var server = http.createServer(function(request, response) {
    console.log((new Date()) + ' Received request for ' + request.url);
    response.writeHead(404);
    response.end();
});

var server2 = http.createServer(function(request, response) {
    console.log((new Date()) + ' Received request for ' + request.url);
    response.writeHead(404);
    response.end();
});


server.listen(8080, function() {
    console.log((new Date()) + ' Server is listening on port 8080');
});

server2.listen(8081, function() {
    console.log((new Date()) + ' Server2 is listening on port 8081');
});


 
wsServer = new WebSocketServer({
    httpServer: server,
    // You should not use autoAcceptConnections for production 
    // applications, as it defeats all standard cross-origin protection 
    // facilities built into the protocol and the browser.  You should 
    // *always* verify the connection's origin and decide whether or not 
    // to accept it. 
    autoAcceptConnections: false
});

wsServer2 = new WebSocketServer({
    httpServer: server2,
    // You should not use autoAcceptConnections for production
    // applications, as it defeats all standard cross-origin protection
    // facilities built into the protocol and the browser.  You should
    // *always* verify the connection's origin and decide whether or not
    // to accept it.
    autoAcceptConnections: false
});

 
function originIsAllowed(origin) {
  // put logic here to detect whether the specified origin is allowed. 
  return true;
}
 
wsServer.on('request', function(request) {
    if (!originIsAllowed(request.origin)) {
      // Make sure we only accept requests from an allowed origin 
      request.reject();
      console.log((new Date()) + ' Connection from origin ' + request.origin + ' rejected.');
      return;
    }
    
    connection1 = request.accept('echo-protocol', request.origin);
    console.log((new Date()) + ' Connection accepted.');
    connection1.on('message', function(message) {
        if (message.type === 'utf8') {
            //console.log('Received Message: ' + message.utf8Data);
            //connection.sendUTF(message.utf8Data);
	    currentDataString = message.utf8Data;
	    if(connection2){
	    		connection2.sendUTF(currentDataString);
		}
        }
	/*
        else if (message.type === 'binary') {
            console.log('Received Binary Message of ' + message.binaryData.length + ' bytes');
            connection.sendBytes(message.binaryData);
        }*/
    });
    connection1.on('close', function(reasonCode, description) {
        console.log((new Date()) + ' Peer ' + connection1.remoteAddress + ' disconnected.');
    });
});


wsServer2.on('request', function(request) {
    if (!originIsAllowed(request.origin)) {
      // Make sure we only accept requests from an allowed origin
      request.reject();
      console.log((new Date()) + ' Connection from origin ' + request.origin + ' rejected.');
      return;
    }

    connection2 = request.accept('echo-protocol',request.origin);
    console.log((new Date()) + ' Connection accepted.');
	
    connection2.on('message', function(message) {
       /* if (message.type === 'utf8') {
            console.log('Received Message: ' + message.utf8Data);
            connection2.sendUTF(message.utf8Data);
        }
        else if (message.type === 'binary') {
            console.log('Received Binary Message of ' + message.binaryData.length + ' bytes');
            connection2.sendBytes(message.binaryData);
        }*/
    });
    connection2.on('close', function(reasonCode, description) {
        console.log((new Date()) + ' Peer ' + connection2.remoteAddress + ' disconnected.');
    });
});

