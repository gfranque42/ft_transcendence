import math

class	Vec2:
	def	__init__(self, x, y):
		self.x = x
		self.y = y

class	Ball:
	def	__init__(self, coor, size, direction, velocity):
		self.coor = coor
		self.size = size
		self.dir = direction
		self.vel = velocity
		self.start = coor
		self.startdir = direction
		self.startvel = velocity
	def	update(self):
		self.coor.x += self.dir.x
		self.coor.y += self.dir.y
	def	reset(self):
		self.coor = self.start
		self.dir = self.startdir
		self.vel = self.startvel
	def	velUpdate(self):
		self.vel.x += self.vel.y
	def	getXMin(self):
		return (self.coor.x)
	def	getXMax(self):
		return (self.coor.x + self.size.x)
	def getSizeX(self):
		return (self.size.x)
	def getSizeY(self):
		return (self.size.y)
	def	getYMin(self):
		return (self.coor.y)
	def	getYMax(self):
		return (self.coor.y + self.size.y)
	def	getXDir(self):
		return (self.dir.x)
	def	getYDir(self):
		return (self.dir.y)
	def	getXVel(self):
		return (self.vel.x)
	def	getYVel(self):
		return (self.vel.y)
	def	setXMin(self, x):
		self.coor.x = x
	def	setYMin(self, y):
		self.coor.y = y
	def	setXSize(self, x):
		self.size.x = x
	def	setYSize(self, y):
		self.size.y = y
	def	setXDir(self, x):
		self.dir.x = x
	def	setYDir(self, y):
		self.dir.y = y
	def setXVel(self, x):
		self.vel.x = x
	def setYVel(self, y):
		self.vel.y = y
	def	getMiddleHeight(self):
		return (self.coor.y + self.size.y / 2)

class	Paddle:
	def	__init__(self, coor, size, ai):
		self.coor = coor
		self.size = size
		self.ai = ai
	def	getCenter(self):
		return (Vec2(self.coor.x + self.size.x / 2,
		  			self.coor.y + self.size.y / 2))
	def	getXMin(self):
		return (self.coor.x)
	def	getXMax(self):
		return (self.coor.x + self.size.x)
	def	getYMin(self):
		return (self.coor.y)
	def	getYMax(self):
		return (self.coor.y + self.size.y)
	def getSizeX(self):
		return (self.size.x)
	def getSizeY(self):
		return (self.size.y)
	def	getAi(self):
		return (self.ai)
	def	setXMin(self, x):
		self.coor.x = x
	def	setYMin(self, y):
		self.coor.y = y
	def	setXSize(self, x):
		self.size.x = x
	def	setYSize(self, y):
		self.size.y = y
	def	setAi(self, ai):
		self.ai = ai
	def	getMiddleHeight(self):
		return (self.coor.y + self.size.y / 2)
	def	getHitZone(self, ball):
		a = (ball.getMiddleHeight() - self.getYMin()) / self.size.y	* 100
		if (a < 0 or a > 100):
			return (0)
		return (a % 50)

def	angleCalculation(c):
	a = -1.0
	b = 0.0
	d = 50.0
	e = 90.0
	r = (e * (c - a) + b * (a  - d)) / (d - a)
	return (r)

def	checkCollisionBallWithPaddle(ball, paddle):
	if ((ball.getXMin() <= paddle.getXMax()) or (ball.getXMax() >= paddle.getXMin())):
		if ((ball.getYMax() >= paddle.getYMin()) and (ball.getYMin() <= paddle.getYMax())):
			x = paddle.getHitZone(ball)
			if (ball.getMiddleHeight() == paddle.getMiddleHeight()):
				angle = 90.0
			else:
				angle = angleCalculation(x)
			ball.velUpdate()
			ball.setXDir(math.sin(math.radians(angle)) * ball.getXVel())
			ball.setYDir(math.cos(math.radians(angle)) * ball.getXVel())
			if (ball.getMiddleHeight() < paddle.getMiddleHeight()):
				ball.setYDir(ball.getYDir() * -1)

def checkCollisionOfPaddleWithEdge(paddle):
	if (paddle.coor.y < 2):
		paddle.coor.y = 2
	if (paddle.coor.y + paddle.size.y > 98):
		paddle.coor.y = 98 - paddle.size.y

def	checkCollisionBallWithEdge(ball):
	if (ball.coor.y <= 2 or ball.coor.y + ball.size.y >= 98):
		ball.vel.y *= -1

def checkScore(ball, paddleL, paddleR, scoreL, scoreR):
	if ((ball.getXMin() <= paddleL.getXMax()) and ((ball.getYMax() < paddleL.getYMin()) or (ball.getYMin() > paddleL.getYMax()))):
		scoreR += 1
		ball.reset()
	elif ((ball.getXMax() <= paddleR.getXMin()) and ((ball.getYMax() < paddleR.getYMin()) or (ball.getYMin() > paddleR.getYMax()))):
		scoreL += 1
		ball.reset()

def gameUpdate(paddleL, paddleR, ball, scoreL, scoreR):
	ball.update()
	checkCollisionOfPaddleWithEdge(paddleL)
	checkCollisionOfPaddleWithEdge(paddleR)
	checkCollisionBallWithEdge(ball)
	checkCollisionBallWithPaddle(ball, paddleL)
	checkCollisionBallWithPaddle(ball, paddleR)
	checkScore(ball, paddleL, paddleR, scoreL, scoreR)
	return paddleL, paddleR, ball, scoreL, scoreR
