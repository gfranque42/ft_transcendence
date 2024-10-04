import {myGame} from "../js/index.js"
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
		this.dir = 0;
	};

	update(paddlecx, paddlecy, paddlesx, paddlesy, paddledy)
	{
		this.pos.update(paddlecx, paddlecy);
		this.size.update(paddlesx, paddlesy);
		this.dir = paddledy;
	};

	draw(canvas, ctx, color, frameTime)
	{
		var width = canvas.width;
		var height = canvas.height;
		ctx.fillStyle = color;
		const posy = this.pos.y + this.dir * (frameTime / (1 / 20));
		ctx.fillRect(this.pos.x / 100 * width, posy / 100 * height, this.size.x / 100 * width, this.size.y / 100 * height);
	};
}

export class ball
{
	constructor(pos, size, dir)
	{
		this.pos = pos;
		this.size = size;
		this.dir = dir;
	};

	update(ballcx, ballcy, ballsx, ballsy, balldx, balldy)
	{
		this.pos.update(ballcx + ballsx / 2, ballcy + ballsy / 2);
		this.size.update(ballsx, ballsy);
		this.dir.update(balldx, balldy);
	};

	draw(canvas, ctx, color, frameTime)
	{
		var width = canvas.width;
		var height = canvas.height;
		const frame = frameTime / (1 / 20);
		const posx = this.pos.x + this.dir.x * frame;
		const posy = this.pos.y + this.dir.y * frame;
		ctx.beginPath();
		ctx.arc(posx / 100 * width, posy / 100 * height, this.size.x / 100 * height, 0, Math.PI * 2);
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
		this.startTime = Date.now();
	};

	update(paddleLcx, paddleLcy, paddleLsx, paddleLsy, paddleLdy, paddleRcx, paddleRcy, paddleRsx, paddleRsy, paddleRdy, ballcx, ballcy, ballsx, ballsy, balldx, balldy, frameTime)
	{
		this.paddleL.update(paddleLcx, paddleLcy, paddleLsx, paddleLsy, paddleLdy);
		this.paddleR.update(paddleRcx, paddleRcy, paddleRsx, paddleRsy, paddleRdy);
		this.ball.update(ballcx, ballcy, ballsx, ballsy, balldx, balldy);
		this.frameTime = frameTime;
	};

	draw(canvas, ctx, frameTime)
	{
		ctx.clearRect(0, 0, canvas.width, canvas.height);
		this.paddleL.draw(canvas, ctx, "#FFFBFC", frameTime);
		this.paddleR.draw(canvas, ctx, "#FFFBFC", frameTime);
		this.ball.draw(canvas, ctx, "#FFFBFC", frameTime);
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
	game.update(data.paddleLcx, data.paddleLcy, data.paddleLsx, data.paddleLsy, data.paddleLdy, data.paddleRcx, data.paddleRcy, data.paddleRsx, data.paddleRsy, data.paddleRdy, data.ballcx, data.ballcy, data.ballsx, data.ballsy, data.balldx, data.balldy, Date.now());
	console.log('game updated');
}

function gameDraw(game, canvas, ctx)
{
	game.draw(canvas, ctx);
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

keyPressed['w'] = false;
keyPressed['s'] = false;
keyPressed[38] = false;
keyPressed[40] = false;

window.addEventListener('keydown', function(e){
	keyPressed[e.keyCode] = true;
	console.log("Key pressed: ", keyPressed[e.keyCode]);
})

window.addEventListener('keyup', function(e){
	keyPressed[e.keyCode] = false;
})

export async function waitForSocketConnection(roomSocket)
{
	setTimeout(
		async function () {
			if (roomSocket.readyState === 1)
			{
				console.log("Connection is made")
				const me = await testToken(roomSocket);
				return me;
			}
			else
			{
				console.log("wait for connection...")
				await waitForSocketConnection(roomSocket);
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
	console.log(UserInformation.ID);
	roomSocket.send(JSON.stringify({
		'type': "username",
		'id': UserInformation.ID,
		'username': UserInformation.Username
	}));
	return {username:UserInformation.Username, id:UserInformation.ID};
}

export async function wsonmessage(data, roomSocket, canvas, ctx)
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
		console.log('game loading', data);
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
		console.log("mon json en preparation!!",keyPressed['w']);
		roomSocket.send(JSON.stringify({
			'type': "ping",
			'w': keyPressed['w'],
			's': keyPressed['s'],
			'up': keyPressed[38],
			'down': keyPressed[40],
		}));
		myGame.gameState = "playing";
	}
	else if (data.type === "gameUpdate")
	{
		console.log("data.message: ", data.message);
		if (data.message === "update")
		{
			console.log(data);
			gameUpdate(data, myGame);
			
			// gameDraw(game, canvas, ctx);
			document.getElementById('player1Score').innerHTML = data.scoreL;
			document.getElementById('player2Score').innerHTML = data.scoreR;
		
			roomSocket.send(JSON.stringify({
				'type': "ping",
				'w': keyPressed['w'],
				's': keyPressed['s'],
				'up': keyPressed[38],
				'down': keyPressed[40],
			}));
			myGame.gameState = "playing";
		}
		else if (data.message === "finish")
		{
			ctx.clearRect(0, 0, canvas.width, canvas.height);
			document.getElementById('player1Score').textContent = data.scoreL;
			document.getElementById('player2Score').textContent = data.scoreR;
			console.log(username);
			console.log(data.scoreL);
			console.log(data.scoreR);
			console.log(data.player1Name);
			console.log(data.player2Name);
			// if (data.scoreL === 5 && data.player1Name === me.username)
			// {
			// 	const	result = document.getElementById("win");
			// 	result.style.display = "flex";
			// }
			// else if (data.scoreR === 5 && data.player2Name === me.username)
			// {
			// 	const	result = document.getElementById("win");
			// 	result.style.display = "flex";
			// }
			// else
			{
				const	result = document.getElementById("loose");
				result.style.display = "flex";
			}
			myGame.gameState = "end";
			const pourStan = {
				"player one" : data.player1id,
				"player two": data.player2id,
				"score one": scoreL,
				"score two": scoreR,
				"winner": 1,// ou 2 player id du winner
				"game": "pong"
			};
			// const link = document.createElement('a');
			// link.href = '/pong/';
			// link.setAttribute('data-link', '');
			// document.body.appendChild(link);
			// console.log(link);
			// link.click();
			// document.body.removeChild(link);
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
