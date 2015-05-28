var app = require('express')();
var server = require('http').Server(app);
var io = require('socket.io')(server);

server.listen(80);

app.get('/', function(req, res){
  res.sendfile(__dirname + '/index.html');
});

io.on("connection", function(socket){
  socket.emit("test", "It works!");
  socket.on("test", function(data){
    console.log("From socket: "+data);
  })
});
