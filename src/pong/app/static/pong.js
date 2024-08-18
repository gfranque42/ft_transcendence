const roomSocket = new WebSocket(
	'ws://'
	+ window.location.host
	+ '/ws'
	+ window.location.pathname
);
roomSocket.onmessage = function(e) {
	const data = JSON.parse(e.data);
	console.log('data.message: ', data.message);
};

roomSocket.onclose = function(e) {
	console.error('Chat socket closed unexpectedly');
};