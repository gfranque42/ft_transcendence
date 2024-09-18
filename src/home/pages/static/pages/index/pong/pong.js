
export class vec2
{
	constructor(x, y)
	{
		this.x = x;
		this.y = y;
	};

	update(x, y)
	{
		this.x = x;
		this.y = y;
	}
}

export class paddle
{
	constructor(pos, size)
	{
		this.pos = pos;
		this.size = size;
	};

	update(paddlecx, paddlecy, paddlesx, paddlesy)
	{
		this.pos.update(paddlecx, paddlecy);
		this.size.update(paddlesx, paddlesy);
	};

	draw(canvas, ctx, color)
	{
		var width = canvas.width;
		var height = canvas.height;
		ctx.fillStyle = color;
		ctx.fillRect(this.pos.x / 100 * width, this.pos.y / 100 * height, this.size.x / 100 * width, this.size.y / 100 * height);
	};
}

export class ball
{
	constructor(pos, size)
	{
		this.pos = pos;
		this.size = size;
	};

	update(ballcx, ballcy, ballsx, ballsy)
	{
		this.pos.update(ballcx + ballsx / 2, ballcy + ballsy / 2);
		this.size.update(ballsx, ballsy);
	};

	draw(canvas, ctx, color)
	{
		var width = canvas.width;
		var height = canvas.height;
		ctx.beginPath();
		ctx.arc(this.pos.x / 100 * width, this.pos.y / 100 * height, this.size.x / 100 * height, 0, Math.PI * 2);
		ctx.fillStyle = color;
		ctx.strokeStyle = color;
		ctx.fill();
		ctx.stroke();
		
	};
}

export class game
{
	constructor(paddleL, paddleR, ball, player1, player2)
	{
		this.paddleL = paddleL;
		this.paddleR = paddleR;
		this.ball = ball;
		this.player1 = player1;
		this.player2 = player2;
		this.gameState = "waiting";
	};

	update(paddleLcx, paddleLcy, paddleLsx, paddleLsy, paddleRcx, paddleRcy, paddleRsx, paddleRsy, ballcx, ballcy, ballsx, ballsy)
	{
		this.paddleL.update(paddleLcx, paddleLcy, paddleLsx, paddleLsy);
		this.paddleR.update(paddleRcx, paddleRcy, paddleRsx, paddleRsy);
		this.ball.update(ballcx, ballcy, ballsx, ballsy);
	};

	draw(canvas, ctx)
	{
		this.paddleL.draw(canvas, ctx, "#FFFBFC");
		this.paddleR.draw(canvas, ctx, "#FFFBFC");
		this.ball.draw(canvas, ctx, "#FFFBFC");
		console.log('I am drawing');
	};
}

function gameDisplay(p1, p2)
{
	let canvas = document.getElementById('canvas');
	let player1Score = document.getElementById('player1Score');
	let player2Score = document.getElementById('player2Score');
	let player1Name = document.getElementById('player1Name');
	let player2Name = document.getElementById('player2Name');
	let waitingForPlayers = document.getElementById('waitingForPlayers');
	let comptearebour = document.getElementById('comptearebour');
	canvas.style.display = 'block';
	player1Score.style.display = 'block';
	player2Score.style.display = 'block';
	player1Name.style.display = 'block';
	player2Name.style.display = 'block';
	comptearebour.style.display = 'block';
	waitingForPlayers.style.display = 'none';
	document.getElementById('player1Name').innerHTML = p1;
	document.getElementById('player2Name').innerHTML = p2;
}

function compteARebour(number)
{
	document.getElementById('comptearebour').innerHTML = number;
}

function gameUpdate(data, game)
{
	game.update(data.paddleLcx, data.paddleLcy, data.paddleLsx, data.paddleLsy, data.paddleRcx, data.paddleRcy, data.paddleRsx, data.paddleRsy, data.ballcx, data.ballcy, data.ballsx, data.ballsy);
	console.log('game updated');
}

function gameDraw(game, s1, s2, canvas, ctx)
{
	game.draw(canvas, ctx);
	document.getElementById('player1Score').innerHTML = s1;
	document.getElementById('player2Score').innerHTML = s2;
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

const	keyPressed = [];

window.addEventListener('keydown', function(e){
	keyPressed[e.keyCode] = true;
	console.log("Key pressed: ", keyPressed[e.keyCode]);
})

window.addEventListener('keyup', function(e){
	keyPressed[e.keyCode] = false;
})

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
	if (!response.ok)
	{
		const link = document.createElement('a');
		link.href = '/login/';
		link.setAttribute('data-link', '');
		document.body.appendChild(link);
		console.log(link);
		link.click();
		document.body.removeChild(link);
	}

	const UserInformation = await response.json();

	console.log(UserInformation);
	console.log(UserInformation.Username);
	console.log(UserInformation.id);
	roomSocket.send(JSON.stringify({
		'type': "username",
		'id': UserInformation.ID,
		'username': UserInformation.Username
	}));
}

export function wsonmessage(data, game, roomSocket, canvas, ctx)
{
	const	KEY_UP = 38;
	const	KEY_DOWN = 40;

	console.log('data onmessage: ', data.type);
	if (data.type === "connected")
	{
		console.log('player connected!');
	}
	else if (data.type === "ready for playing")
	{
		console.log('game loading');
		gameDisplay(data.player1Name, data.player2Name);
	}
	else if (data.type === "compte a rebour")
	{
		console.log(data);
		compteARebour(data.number);
	}
	else if (data.type === "fin du compte")
	{
		console.log(data);
		let comptearebour = document.getElementById('comptearebour');
		comptearebour.style.display = '';
		const move = "none";
		roomSocket.send(JSON.stringify({
			'type': "ping",
			'move': move,
		}));
	}
	else if (data.type === "game update")
	{
		console.log("data.message: ", data.message);
		if (data.message === "in playing")
		{
			console.log(data);
			gameUpdate(data, game);
			ctx.clearRect(0, 0, canvas.width, canvas.height);
			gameDraw(game, data.scoreL, data.scoreR, canvas, ctx);
	
			let move = "none";
			if (keyPressed[38] == true)
				move = "up";
			if (keyPressed[40] == true)
			{
				if (move === "none")
					move = "down";
				else
					move = "none";
			}
			console.log('keypressed: ', move);
			roomSocket.send(JSON.stringify({
				'type': "ping",
				'move': move,
			}));
		}
		else if (data.message === "game is finished")
		{
			const link = document.createElement('a');
			link.href = '/pong/';
			link.setAttribute('data-link', '');
			document.body.appendChild(link);
			console.log(link);
			link.click();
			document.body.removeChild(link);
		}
	}
	else if (data.type === "end game")
	{
		console.log("serveur wants to quit");
		const link = document.createElement('a');
		link.href = '/pong/';
		link.setAttribute('data-link', '');
		document.body.appendChild(link);
		console.log(link);
		link.click();
		document.body.removeChild(link);
	}
}
