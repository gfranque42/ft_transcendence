// recevoir le nom de la room en json au moment ou on lance la page
const roomSocket = new WebSocket(
	'ws://'
	+ window.location.host
	+ '/ws/pong/'
	+ ''
)