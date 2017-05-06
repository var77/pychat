const io = require('socket.io')();
const http = require('http');

let server = http.createServer();
let nsp = io.of('/my-namespace');

io.on('connection', socket => {
 console.log(socket.id, 'connected');
 socket.on('join_room', roomId => {
    console.log(roomId);
    socket.join(roomId)
 });

 socket.on('new_message', data => {
    console.log(data);
    io.to(data.room).emit('get_message', data);
 });
});

io.listen(server);
server.listen(8888);
