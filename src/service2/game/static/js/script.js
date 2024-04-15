const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth - 200;
canvas.height = window.innerHeight - 300;

//drawing in the canvas using the context and the fill method to fill a rectangle or a circle

/* {
	ctx.fillStyle = "#ffebcd";
	ctx.fillRect(0, 0, window.innerWidth, window.innerHeight);
	ctx.fillStyle = "#BBBBBB";
	ctx.fillRect(window.innerWidth / 10, window.innerHeight / 10, window.innerWidth / 10 * 8, window.innerHeight / 10 * 8);
	
	ctx.beginPath();
	ctx.arc(window.innerWidth / 2, window.innerHeight / 2, window.innerHeight / 10, 0, Math.PI * 2);
	ctx.fillStyle = "#CCCCCC";
	ctx.fill();
	ctx.stroke();
} */
//ball animation

let ballX = 200;
let ballY = 200;
let ballRadius = 50;
let ballVelocityX = 2;
let ballVelocityY = 2;

function vec2(x, y)
{
	return {x: x, y: y};
}

const	keyPressed = [];
const	KEY_UP = 38;
const	KEY_DOWN = 40;
const	KEY_W = 87;
const	KEY_S = 83;

window.addEventListener('keydown', function(e){
	keyPressed[e.keyCode] = true;
})

window.addEventListener('keyup', function(e){
	keyPressed[e.keyCode] = false;
})

function Paddle(pos, velocity, width, height, type)
{
	this.pos = pos;
	this.velocity = velocity;
	this.width = width;
	this.height = height;
	this.type = type;
	this.score = 0;

	this.update = function ()
	{
		if (this.type === 0 && keyPressed[KEY_UP] === true && this.pos.y >= 0)
			this.pos.y -= this.velocity.y;
		if (this.type === 0 && keyPressed[KEY_DOWN] === true && (this.pos.y + this.height) <= canvas.height)
			this.pos.y += this.velocity.y;
		if (this.type === 1 && keyPressed[KEY_W] === true && this.pos.y >= 0)
			this.pos.y -= this.velocity.y;
		if (this.type === 1 && keyPressed[KEY_S] === true && (this.pos.y + this.height) <= canvas.height)
			this.pos.y += this.velocity.y;
		if (this.type === 2)
			document.getElementById("player2Name").innerHTML = "AI";
	};
	
	this.draw = function ()
	{
		ctx.fillStyle = "#FFFBFC";
		ctx.fillRect(this.pos.x, this.pos.y, this.width, this.height);
	};

	this.getHalfWidth = function ()
	{
		return (this.width / 2);
	};
	
	this.getHalfHeight = function ()
	{
		return (this.height / 2);
	};

	this.getCenter = function ()
	{
		return (vec2(this.pos.x + this.getHalfWidth(), this.pos.y + this.getHalfHeight()));
	};

}

function Ball(pos, velocity, radius)
{
	this.pos = pos;
	this.velocity = velocity;
	this.radius = radius;

	this.update = function ()
	{
		this.pos.x += this.velocity.x;
		this.pos.y += this.velocity.y;
	};
	
	this.draw = function ()
	{
		ctx.beginPath();
		ctx.arc(this.pos.x, this.pos.y, this.radius, 0, Math.PI * 2);
		ctx.fillStyle = "#FFFBFC";
		ctx.strokeStyle = "#FFFBFC";
		ctx.fill();
		ctx.stroke();
	};
}

function paddleAI(ball, paddle)
{
	paddle.type = 2;
	if (ball.pos.x > paddle.pos.x && ball.velocity.x < 0)
	{
		if (ball.pos.y > paddle.getCenter().y)
		{
			paddle.pos.y += paddle.velocity.y;
		}
		if (ball.pos.y < paddle.getCenter().y)
		{
			paddle.pos.y -= paddle.velocity.y;
		}
	}
	if (ball.pos.x < paddle.pos.x && ball.velocity.x > 0)
	{
		if (ball.pos.y > paddle.getCenter().y)
		{
			paddle.pos.y += paddle.velocity.y;
		}
		if (ball.pos.y < paddle.getCenter().y)
		{
			paddle.pos.y -= paddle.velocity.y;
		}
	}
}

function ballCollisionWithEdge(ball)
{
	if (ball.pos.y + ball.radius >= canvas.height || ball.pos.y - ball.radius <= 0)
	{
		ball.velocity.y *= -1;
	}
	// if (ball.pos.x + ball.radius >= canvas.width || ball.pos.x - ball.radius <= 0)
	// {
	// 	ball.velocity.x *= -1;
	// }
}

function paddleCollisionWithEdge(paddle)
{
	if (paddle.pos.y < 0)
	{
		paddle.pos.y = 0;
	}
	if (paddle.pos.y + paddle.height > canvas.height)
	{
		paddle.pos.y = canvas.height - paddle.height;
	}
}

function ballPaddleCollision(ball, paddle)
{
	let dx = Math.abs(ball.pos.x - paddle.getCenter().x);
	let dy = Math.abs(ball.pos.y - paddle.getCenter().y);

	if (dx <= (ball.radius + paddle.getHalfWidth()) && dy <= (ball.radius + paddle.getHalfHeight()))
	{
		ball.velocity.x *= -1;
	}
}

function respawnBall(ball)
{
	if (ball.velocity.x > 0)
	{
		ball.pos.x = canvas.width - 250;
		ball.pos.y = (Math.random() * (canvas.height - 200)) + 100;
		// ball.pos.y = canvas.height / 2;
	}
	if (ball.velocity.x > 0)
	{
		ball.pos.x = 250;
		ball.pos.y = (Math.random() * (canvas.height - 200)) + 100;
		// ball.pos.y = canvas.height / 2;
	}
	ball.velocity.x *= -1;
	ball.velocity.y *= -1;
}

function increaseScore(ball, paddle1, paddle2)
{
	if (ball.pos.x <= -ball.radius)
	{
		paddle2.score += 1;
		document.getElementById("player2Score").innerHTML = paddle2.score;
		respawnBall(ball);
	}
	if (ball.pos.x >= canvas.width + ball.radius)
	{
		paddle1.score += 1;
		document.getElementById("player1Score").innerHTML = paddle1.score;
		respawnBall(ball);
	}
}

const ball = new Ball(vec2(200, 200), vec2(13, 11), 20);

const player1 = new Paddle(vec2(10, 100), vec2(0, 10), 10, 60, 0);

const player2 = new Paddle(vec2(window.innerWidth - 40, 100), vec2(0, 10), 10, 60, 1);

function gameUpdate()
{
	ball.update();
	player1.update();
	player2.update();
	paddleAI(ball, player2);
	// paddleAI(ball, player1);
	ballCollisionWithEdge(ball);
	paddleCollisionWithEdge(player1);
	paddleCollisionWithEdge(player2);
	ballPaddleCollision(ball, player1);
	ballPaddleCollision(ball, player2);
	increaseScore(ball, player1, player2);
	// const bob = getElementById('canvas');
	// canvas.width = bob.width;
	// canvas.height = bob.height;
	canvas.width = window.innerWidth;
	canvas.height = window.innerHeight;
}
////////////////////////////////faire le pong avec le vieux dvd !!!!!!!!!!!!!
////////////////////////////////faire un mode 2 vs 2 !!!!!!!!!!!!!!!!!!!!!!!!
function gameDraw()
{
	ball.draw();
	player1.draw();
	player2.draw();
	ctx.fillStyle = "#ffebcd";
	ctx.fillRect(250, 0, 1, window.innerHeight);
	ctx.fillRect(canvas.width - 250, 0, 1, window.innerHeight);
}

function gameLoop()
{
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	/* /* ctx.fillStyle = "#DDDDDD";
	ctx.fillRect (0, 0, canvas.width, canvas.height); */
	window.requestAnimationFrame(gameLoop);

	gameUpdate();
	gameDraw();
}

let p1s = document.getElementById('player1Score');
let p2s = document.getElementById('player2Score');
let p1n = document.getElementById('player1Name');
let p2n = document.getElementById('player2Name');
let button = document.getElementById('button');
function startGame()
{
	gameStarted = 1;
	// const cnv = getElementById('canvas');
	canvas.style.display = 'block';
	p1s.style.display = 'block';
	p2s.style.display = 'block';
	p1n.style.display = 'block';
	p2n.style.display = 'block';
	button.style.display = 'none';
	gameLoop();
}
