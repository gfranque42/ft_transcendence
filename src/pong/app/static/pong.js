// recevoir le nom de la room en json au moment ou on lance la page
const roomSocket = new WebSocket(
	'wss://'
	+ window.location.host
	+ '/ws'
	+ window.location.pathname
);

const bob = 'wss://'
	+ window.location.host
	+ '/ws'
	+ window.location.pathname;
console.log(bob);

roomSocket.onmessage = function(e) {
	const data = JSON.parse(e.data);
	console.log('data.message: ', data.message);
};

roomSocket.onclose = function() {
	console.error('Room socket closed unexpectedly');
};

ping = function() {
	const	message = "ping";

	roomSocket.send(JSON.stringify({
		'message': message
	}))
};

ping();
