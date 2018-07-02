const io = require('socket.io')();
const http = require('http');

let server = http.createServer();

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
console.log('Socket Server running at 8888 port.')
