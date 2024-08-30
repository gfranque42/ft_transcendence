var socketProtocol = 'ws://';
console.log(window.location.protocol);
if (window.location.protocol === 'https:')
{
	console.log('protocol https');
	socketProtocol = 'wss://';
}

const roomSocket = new WebSocket(
	socketProtocol
	+ window.location.host
	+ '/ws'
	+ window.location.pathname
);

function getCookie(name)
{
	let cookieValue = null;
	if (document.cookie && document.cookie !== '')
	{
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++)
		{
			const cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === `${name}=`)
			{
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	console.log("cookie: ", cookieValue);
	return cookieValue;
}

function waitForSocketConnection()
{

	setTimeout(
		function () {
			if (roomSocket.readyState === 1)
			{
				console.log("Connection is made")
			}
			else
			{
				console.log("wait for connection...")
				waitForSocketConnection(roomSocket);
			}

		}, 5);
}

async function testToken()
{
	cookie = getCookie('token');

	const options = {
		method: 'GET', // HTTP method
		headers: {
			'Content-Type': 'application/json',
			'Authorization': `Token ${cookie}`
		}

	};

	const response = await fetch('https://localhost:8083/auth/test_token', options);
	const UserInformation = await response.json();

	console.log(UserInformation);
	console.log(UserInformation.Username);
	roomSocket.send(JSON.stringify({
		'type': "username",
		'username': UserInformation.Username
	}));
}

waitForSocketConnection();
testToken();

roomSocket.onmessage = function (e)
{
	const data = JSON.parse(e.data);
	console.log('data.message: ', data.message);
};

roomSocket.onclose = function (e)
{
	console.error('Chat socket closed unexpectedly');
};
