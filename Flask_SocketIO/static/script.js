var socket = io.connect('https://127.0.0.1:5000');

socket.on('connect', function(){
    socket.send('I am connected !!!');
});