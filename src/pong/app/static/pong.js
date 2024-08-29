var	roomSocket;

if (window.location.protocol === 'http')
{
	roomSocket = new WebSocket(
		'ws://'
		+ window.location.host
		+ '/ws'
		+ window.location.pathname
	);
}
else if (window.location.protocol === 'https')
{
	roomSocket = new WebSocket(
		'wss://'
		+ window.location.host
		+ '/ws'
		+ window.location.pathname
	);
}

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
	roomSocket.onmessage = function(e) {
		const data = JSON.parse(e.data);
		console.log('data.message: ', data.message);
	};
}

testToken();

roomSocket.onclose = function(e) {
	console.error('Chat socket closed unexpectedly');
};