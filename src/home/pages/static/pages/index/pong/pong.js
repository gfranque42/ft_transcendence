import {myGame} from "../js/index.js"
import {DNS} from "../js/dns.js";
import { sendGameResults } from "./sendGameResults.js";

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

	reset()
	{
		this.pos.x = -5;
		this.pos.y = -5;
		this.size.x = 2;
		this.size.y = 2;
		this.dir = 0;
	}

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
		const frame = frameTime / (1/20);
		const posy = this.pos.y + this.dir * frame;
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

	reset()
	{
		this.pos.x = -5;
		this.pos.y = -5;
		this.size.x = 2;
		this.size.y = 2;
		this.dir.x = 0;
		this.dir.y = 0;
	}

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

	reset()
	{
		this.gameState = "waiting";
		this.startTime = Date.now();
		this.paddleL.reset();
		this.paddleR.reset();
		this.ball.reset();
	}

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
	game.update(data.paddleLcx, data.paddleLcy, data.paddleLsx, data.paddleLsy, data.paddleLd, data.paddleRcx, data.paddleRcy, data.paddleRsx, data.paddleRsy, data.paddleRd, data.ballcx, data.ballcy, data.ballsx, data.ballsy, data.balldx, data.balldy, Date.now());
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
	return cookieValue;
}

const	keyPressed = [];

keyPressed[87] = false;
keyPressed[83] = false;
keyPressed[38] = false;
keyPressed[40] = false;

window.addEventListener('keydown', function(e){
	keyPressed[e.keyCode] = true;
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
				const me = await testToken(roomSocket);
				return me;
			}
			else
			{
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

	const response = await fetch('https://'+DNS+':8083/auth/test_token?request_by=Home', options);
	if (!response.ok)
	{
		navigateToInstead("/login/");
	}

	const UserInformation = await response.json();

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

	if (data.type === "connected")
	{
		myGame.gameState = "waiting";
	}
	else if (data.type === "ready for playing")
	{
		gameDisplay(data.player1Name, data.player2Name);
	}
	else if (data.type === "compte a rebour")
	{
		compteARebour(data.number);
	}
	else if (data.type === "fin du compte")
	{
		let comptearebour = document.getElementById('comptearebour');
		comptearebour.style.display = '';
		roomSocket.send(JSON.stringify({
			'type': "ping",
			'w': keyPressed[87],
			's': keyPressed[83],
			'up': keyPressed[38],
			'down': keyPressed[40],
		}));
		myGame.gameState = "playing";
	}
	else if (data.type === "matchmaking")
	{
		document.getElementById('comptearebour').innerHTML = data.player1+' vs '+data.player2;
	}
	else if (data.type === "gameUpdate" || data.type === "tournamentUpdate")
	{
		if (data.type === "tournamentUpdate" && data.message === "ready for playing")
		{
			gameDisplay(data.player1Name, data.player2Name);
		}
		else if (data.message == "update")
		{
			gameUpdate(data, myGame);
			
			// gameDraw(game, canvas, ctx);
			document.getElementById('player1Score').innerHTML = data.scoreL;
			document.getElementById('player2Score').innerHTML = data.scoreR;
		
			roomSocket.send(JSON.stringify({
				'type': "ping",
				'w': keyPressed[87],
				's': keyPressed[83],
				'up': keyPressed[38],
				'down': keyPressed[40],
			}));
			myGame.gameState = "playing";
		}
		else if (data.message == "finish")
		{
			ctx.clearRect(0, 0, canvas.width, canvas.height);
			document.getElementById('player1Score').textContent = data.scoreL;
			document.getElementById('player2Score').textContent = data.scoreR;
			let back = document.getElementById('backtopong');
			if ((data.partyType == 0 || data.partyType == 5) && data.scoreL === 3 && data.player1Name === data.username)
			{
				const	result = document.getElementById("result");
				result.textContent = "You win !";
				result.style.display = "flex";
				back.textContent = data.buttonwin
				back.href = data.urlwin
				if (data.partyType == 0)
				{
					back.textContent = data.buttonloose
					back.href = data.urlloose
				}
				sendGameResults(data.player1Id, data.player2Id, data.scoreL, data.scoreR);
			}
			else if ((data.partyType == 0 || data.partyType == 5) && data.scoreR === 3 && data.player2Name === data.username)
			{
				const	result = document.getElementById("result");
				result.textContent = "You win !";
				result.style.display = "flex";
				back.textContent = data.buttonwin
				back.href = data.urlwin
				if (data.partyType == 0)
				{
					back.textContent = data.buttonloose
					back.href = data.urlloose
				}
				sendGameResults(data.player2Id, data.player1Id, data.scoreL, data.scoreR);
			}
			else if (data.partyType == 0 || data.partyType == 5)
			{
				const	result = document.getElementById("result");
				result.textContent = "You loose !";
				result.style.display = "flex";
				back.textContent = data.buttonloose
				back.href = data.urlloose
			}
			else
			{
				const	result = document.getElementById("result");
				if (data.scoreL == 3)
				{
					result.textContent = data.player1Name + " win !";
				}
				else
				{
					result.textContent = data.player2Name + " win !";
				}
				result.style.display = "flex";
				back.textContent = data.buttonloose
				back.href = data.urlloose
			}
			back.style.display = 'block';
			myGame.gameState = "end";
			const	result = document.getElementById("result");
			if (data.partyType == 5 && result.textContent == "You win !" && data.urlwin == "Next round")
			{
				back.href = "pong/SbDaMcGf24/";
				back.textContent = data.buttonwin
			}
			roomSocket.close(1000, "Closing at end of the game")
		}
	}
	else if (data.type == "tournament")
	{
		myGame.reset();
		const link = document.createElement('a');
		link.href = '/pong/'+data.url;
		link.setAttribute('data-link', '');
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
	}
	else if (data.type === "end game")
	{
		const link = document.createElement('a');
		link.href = '/pong/';
		link.setAttribute('data-link', '');
		document.body.appendChild(link);
		link.click();
			document.body.removeChild(link);
	}
}
