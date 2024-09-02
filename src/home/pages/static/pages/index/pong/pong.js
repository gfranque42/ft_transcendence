
export class vec2
{
	constructor(x, y)
	{
		x = x;
		y = y;
	};
}

export class paddle
{
	constructor(pos, size)
	{
		this.pos = pos;
		this.size = size;
	};

	update(pos, size)
	{
		this.pos = pos;
		this.size = size;
	};
}

export class ball
{
	constructor(pos, size)
	{
		this.pos = pos;
		this.size = size;
	};

	update(pos, size)
	{
		this.pos = pos;
		this.size = size;
	};
}

export class game
{
	constructor(paddle1, paddle2, ball, player1, player2)
	{
		this.paddle1 = paddle1;
		this.paddle2 = paddle2;
		this.ball = ball;
		this.player1 = player1;
		this.player2 = player2;
		this.gameState = "waiting";
	};

	update(paddle1, paddle2, ball)
	{
		this.paddle1.update(paddle1.pos, paddle1.size);
		this.paddle2.update(paddle2.pos, paddle2.size);
		this.ball.update(ball.pos, ball.size);
	};
}

export function getCookie(name)
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

export function waitForSocketConnection(roomSocket)
{

	setTimeout(
		function () {
			if (roomSocket.readyState === 1)
			{
				console.log("Connection is made")
				testToken(roomSocket);
			}
			else
			{
				console.log("wait for connection...")
				waitForSocketConnection(roomSocket);
			}

		}, 5);
}

export async function testToken(roomSocket)
{
	const cookie = getCookie('token');

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
export function wsonmessage(data)
{
	console.log('data onmessage: ', data.type);
	if (data.type === "connected")
	{
		console.log('player connected!');
	}
	else if (data.type === "ready for playing")
		console.log('game loading');
}

